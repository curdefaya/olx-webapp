import { useState } from 'react';
import './App.css'; // Importujemy dedykowane style CSS

export default function App() {
  const [activeTab, setActiveTab] = useState('profile');
  const [Olx_url, setOlx_url] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // if(!Olx_url.trim()) return;
    console.log("zatwierdzenie linku:", Olx_url);
    
    // Wywołanie funkcji w Rust lub Python
  };

  return (
    <div className="dashboard-container">
      {/* --- SIDEBAR --- */}
      <aside className="sidebar">
        <h2 className="logo">
          Olx scraper (miejsce na logo)
        </h2>

        <button 
          className={`tab-button ${activeTab === 'link_scraping' ? 'active' : ''}`} 
          onClick={() => setActiveTab('link_scraping')}
        >
          Analizuj po linku
        </button>
        <button className="tab-button">
          Szukaj w aplikacji
        </button>
        <button className="tab-button">
          Zapisane wyszukiwania
        </button>
        <button className="tab-button">
          Ustawienia
        </button>
      </aside>

      {/* --- MAIN DASHBOARD ELEMENTS --- */}
      <main className="main-content">
        {activeTab === 'profile' && (
          <section>
            <h2>prof 1</h2>
          </section>
        )}

        {activeTab === 'link_scraping' && (
          <section>
            <h3>Podaj link poniżej</h3>
            <form onSubmit={handleSubmit}>
              <label>
                podaj link
                <input 
                  type="text" 
                  value={Olx_url} 
                  onChange={(e) => setOlx_url(e.target.value)} 
                />
              </label>
              <button type="submit">Wyślij</button>
            </form>
            <h2>
              [pobrane ogłoszenia]
            </h2>
            <h2>
              sortowanie po wskaźniku opłacalności
            </h2>
            <h2>
              lista ogłoszeń wraz z linkami do otwarcia
            </h2>
          </section>
        )}
      </main>
    </div>
  );
}