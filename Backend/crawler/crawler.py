import asyncio
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
import pandas as pd
from crawlee import Request
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

scraped_data = []

START_URL = "https://www.olx.pl/elektronika/komputery/komputery-stacjonarne/q-Dell%20OptiPlex%20Micro/?min_id=1102699770&reason=observed_search&search%5Bfilter_enum_ramtype_desktops%5D%5B0%5D=ddr4"

MAX_PAGES = 5


def get_next_page_url(current_url: str, target_page: int) -> str:
    """Modyfikuje lub dodaje parametr page=N do adresu URL, zachowując filtry."""
    parsed = urlparse(current_url)
    query_params = parse_qs(parsed.query, keep_blank_values=True)

    query_params["page"] = [str(target_page)]

    # Rekonstrukcja URL-a z zachowaniem filtrów
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )
    return new_url


def get_current_page_number(url: str) -> int:
    """Pobiera numer bieżącej strony z URL."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    if "page" in query_params:
        try:
            return int(query_params["page"][0])
        except Exception:
            return 1
    return 1


async def main():
    crawler = PlaywrightCrawler(
        headless=True,
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        page = context.page
        url = context.request.url

        # Blokowanie obrazków i stylów (dla prędkości i ograniczenia bana)
        await page.route(
            "**/*",
            lambda route: route.abort()
            if route.request.resource_type in ["image", "stylesheet", "font"]
            else route.continue_(),
        )

        # CASE 1: STRONA OGŁOSZENIA

        if "/d/oferta/" in url:
            desc_elem = page.locator('div[data-testid="ad_description"]')
            description = (
                await desc_elem.inner_text()
                if await desc_elem.count() > 0
                else "Brak opisu"
            )

            user_data = context.request.user_data
            user_data["Opis"] = description.strip()

            scraped_data.append(user_data)
            context.log.info(
                f"Pobrano opis [{len(scraped_data)}]: {user_data.get('Tytuł', '')[:30]}..."
            )


        # CASE 2: STRONA LISTY OGŁOSZEŃ (WYSZUKIWANIA)

        else:
            current_page_num = get_current_page_number(url)
            context.log.info(
                f"Scrapowanie listy (Strona {current_page_num}/{MAX_PAGES}): {url}"
            )

            await page.wait_for_selector('div[data-cy="l-card"]', timeout=10000)

            cards = await page.locator('div[data-cy="l-card"]').all()
            context.log.info(
                f"Znaleziono {len(cards)} kart ogłoszeń na stronie {current_page_num}."
            )

            requests_to_add = []

            # 1. Pobieranie ogłoszeń z bieżącej strony
            for card in cards:
                try:
                    title_elem = card.locator("h6, h4").first
                    title = (
                        await title_elem.inner_text()
                        if await title_elem.count() > 0
                        else None
                    )

                    link_elem = card.locator("a").first
                    href = (
                        await link_elem.get_attribute("href")
                        if await link_elem.count() > 0
                        else None
                    )

                    price_elem = card.locator('p[data-testid="ad-price"]').first
                    price = (
                        await price_elem.inner_text()
                        if await price_elem.count() > 0
                        else "Brak ceny"
                    )

                    if href and title:
                        full_link = (
                            f"https://www.olx.pl{href}"
                            if href.startswith("/")
                            else href
                        )

                        if "/d/oferta/" in full_link:
                            req = Request.from_url(
                                url=full_link,
                                user_data={
                                    "Tytuł": title.strip(),
                                    "Cena": price.strip(),
                                    "Link": full_link,
                                },
                            )
                            requests_to_add.append(req)
                except Exception as e:
                    context.log.error(f"Błąd odczytu karty: {e}")

            # 2. DODAWANIE STRONY NR 2, 3, 4... (zachowując pełne filtry z URL)
            if current_page_num == 1 and MAX_PAGES > 1:
                for next_p in range(2, MAX_PAGES + 1):
                    next_url_with_filters = get_next_page_url(START_URL, next_p)
                    context.log.info(
                        f"Dodawanie do kolejki strony {next_p} z filtrami: {next_url_with_filters}"
                    )
                    requests_to_add.append(
                        Request.from_url(url=next_url_with_filters)
                    )

            if requests_to_add:
                await context.add_requests(requests_to_add)

    # Uruchomienie crawlera
    await crawler.run([START_URL])

    # Zapis wyników do pliku CSV
    if scraped_data:
        df = pd.DataFrame(scraped_data)
        df.to_csv("crawler_results.csv", index=False, encoding="utf-8-sig")
        print(
            f"\nSukces! Zapisano {len(df)} ogłoszeń do pliku 'crawler_results.csv'."
        )
    else:
        print("\nNie znaleziono żadnych danych.")


if __name__ == "__main__":
    asyncio.run(main())
