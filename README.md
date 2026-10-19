# Używanie programu grozi zbanowaniem na platformie olx.pl

1. **Instalacja zależności systemowych:**
   Przed utworzeniem środowiska upewnij się, że masz zainstalowany Python oraz `pip`:
   
```bash
   sudo pacman -S python python-pip
   
```

2. **Przygotowanie środowiska wirtualnego:**
   Zalecane jest korzystanie z wirtualnego środowiska (`venv`), aby uniknąć błędów związanych z zarządzaniem pakietami przez system (`externally-managed-environment`):
   
```bash
   python -m venv venv
   source venv/bin/activate
   
```

3. **Instalacja pakietów Python:**
   Zainstaluj biblioteki `crawlee` oraz `pandas`:
   
```bash
   pip install "crawlee[playwright]" pandas
   
```

4. **Instalacja przeglądarki Chromium dla Playwright:**
   Zainstaluj silnik przeglądarki wykorzystywany przez Playwright wraz z niezbędnymi zależnościami systemowymi:
   
```bash
   playwright install --with-deps chromium
   
```

5. **Zmiana linku w kodzie według uznania** 
    W pliku crawler.py należy zmienić parametr START_URL znajdujący się w linii 9.
    *W przypadku użycia input() wklejanie linku do konsoli bywa problematyczne*

6. **Uruchomienie skryptu**
    ```bash
    python3 crawler.py
    ```