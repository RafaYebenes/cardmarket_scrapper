import { useState, useEffect } from "react";
import "./App.css";

const loadingMessages = [
  "Cargando...",
  "illo ya se que tarda pero cardmarket no lo pone fácil para sacar las cartas",
  "venga ahora a buscar el precio",
  "paciencia, joven nakama...",
  "esto tarda más que Luffy subiendo la torre de Enies Lobby"
];

export interface Card {
  image: string;
  text: string;
  code: string;
  version?: string;
  collection: string;
  price?: number;
}


export default function CardSearch() {
  const [code, setCode] = useState("");
  const [cards, setCards] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);

  // Lista de GIFs
  const loadingGifs = [
    "https://img.wattpad.com/289854af8ed62b0da17cb6469f8b629bc4a5d1d1/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f365538505a324635425a4d5630673d3d2d38312e313462656138363065363934663365373730333639353638303135362e676966",
    "https://media.tenor.com/ZHlhQbghsBUAAAAM/monkey-d-luffy-one-piece-monkey-d-luffy.gif",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJvd2p5YXIyMGtydzJyeTZrYmJiemR6NHZ1dXRtcTJ2cGZ4dzNocSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/DSxKEQoQix9hC/giphy.gif"
    , "https://giffiles.alphacoders.com/221/221581.gif"
    , "https://img.wattpad.com/746adb189d8903972593bd8f2be4b768cd31f673/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f57684147375548445749727369773d3d2d38312e313462656138346635616338656564393136343833383332383931332e676966"
    , 'https://img.wattpad.com/1362448cd3f8881c7d13153d3957a207ea557252/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f6e5334415258666e4b7533597a413d3d2d38312e313462656138353337636537333039353631383734333830363237322e676966'
  ];


  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;

    if (loading) {
      interval = setInterval(() => {
        setLoadingMessageIndex((prev) => (prev + 1) % loadingMessages.length);
      }, 5000);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const [gifIndex, setGifIndex] = useState(Math.floor(Math.random() * loadingGifs.length));

  useEffect(() => {
    if (!loading) return;

    const messageInterval = setInterval(() => {
      setLoadingMessageIndex((prev) => (prev + 1) % loadingMessages.length);
      setGifIndex(Math.floor(Math.random() * loadingGifs.length));
    }, 5000);

    return () => clearInterval(messageInterval);
  }, [loading]);

  const searchCards = async () => {
    setError("");
    setLoading(true);
    setCards([]);
    setLoadingMessageIndex(0);
    try {
      const res = await fetch("https://opchecker.duckdns.org/api/search_cards", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      });

      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        setError(data.error || "Error desconocido");
        return;
      }
      setCards(data);
    } catch (err) {
      console.error("❌ Error al buscar cartas", err);
      setError("Error de conexión");
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">Cardmarket search</h1>
      <h3 className="sub_title">Busca por código: OPXX-XXX. Todos los precios son minimo españa</h3>
      <div className="search-bar">
        <input
          className="input-code"
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Ej. OP01-001"
        />
        <button className="search-button" onClick={searchCards}>Buscar</button>
      </div>

      {loading && (
        <div className="loading-container">
          <img
            src={loadingGifs[gifIndex]}
            alt="Loading..."
            className="loading-gif"
          />
          <p className="loading-message">{loadingMessages[loadingMessageIndex]}</p>
        </div>
      )}
      {error && <p className="error">{error}</p>}

      <div className="card-grid" >
        {cards.map((card:Card, idx) => (
          <div className="card-container" key={idx}>
            <img src={card.image} alt={card.text} className="card-image" />
            <div className="card-overlay">
              <div className="card-name">{card.text}</div>
              <div className="card-details">
                <div>{card.code} · {card.version || "V.1"}</div>
                <div>{card.collection} · {card.price ? card.price + "€" : "Sin precio"}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}