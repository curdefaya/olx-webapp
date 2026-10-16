import { useState } from 'react';
import './App.css'; // Importujemy dedykowane style CSS

export default function App() {
const [activeTab, setActiveTab] = useState('profile');

// Funkcja dodawania elementu do tablicy (na razie nie potrzebna)
const addItem = (e) => {
e.preventDefault();
if (!newItemText.trim()) return;

setItems([...items, { id: Date.now(), title: newItemText }]);
setNewItemText('');
};

return (
<div className="dashboard-container">
  {/* --- SIDEBAR --- */}
  <aside className="sidebar">
    <h2 className='logo'>
      Olx scraper (miejsce na logo)
    </h2>

    <button className={`tab-button ${activeTab==='link_scraping' ? 'active' : '' }`} onClick={()=> setActiveTab('link_scraping')}
      >
      Analizuj po linku
    </button>
    <button className='tab-button'>
      Szukaj w aplikacji
    </button>
    <button className='tab-button'>
      Zapisane wyszukiwania
    </button>
  </aside>
  {/* --- MAIN DASHBOARD ELEMENTS --- */}
  <main className='main-content'>
    {activeTab === 'link_scraping' && (
      <section>
        <h3>Podaj link poniżej</h3>
      </section>
    )}

  </main>

</div>
);
}