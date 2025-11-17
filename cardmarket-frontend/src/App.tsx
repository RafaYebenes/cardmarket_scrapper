import { useState, useEffect } from "react";
import { Search, Sparkles, Anchor, Compass } from "lucide-react";

const loadingMessages = [
  "🌊 Navegando por el Grand Line...",
  "⚔️ Cardmarket no lo pone fácil, pero somos persistentes",
  "💎 Buscando el tesoro más valioso...",
  "🏴‍☠️ Los Piratas de Sombrero de Paja están en ello",
  "⛵ Esto tarda más que encontrar el One Piece",
  "🗺️ Zoro se perdió, pero seguimos buscando..."
];

export interface Card {
  image: string;
  text: string;
  code: string;
  version?: string;
  collection: string;
  price?: number;
}

export default function CardSearchPremium() {
  const [code, setCode] = useState("");
  const [cards, setCards] = useState<Card[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);
  const [hoveredCard, setHoveredCard] = useState<number | null>(null);
  const url = "https://opchecker.duckdns.org/api/search_cards"
  const test_url = "http://127.0.0.1:5000/api/search_cards"

  const loadingGifs = [
    "https://img.wattpad.com/289854af8ed62b0da17cb6469f8b629bc4a5d1d1/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f365538505a324635425a4d5630673d3d2d38312e313462656138363065363934663365373730333639353638303135362e676966",
    "https://media.tenor.com/ZHlhQbghsBUAAAAM/monkey-d-luffy-one-piece-monkey-d-luffy.gif",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJvd2p5YXIyMGtydzJyeTZrYmJiemR6NHZ1dXRtcTJ2cGZ4dzNocSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/DSxKEQoQix9hC/giphy.gif",
    "https://giffiles.alphacoders.com/221/221581.gif"
  ];

  const [currentGif, setCurrentGif] = useState(loadingGifs[0]);

  useEffect(() => {
    if (!loading) return;

    const interval = setInterval(() => {
      setLoadingMessageIndex((prev) => (prev + 1) % loadingMessages.length);
      setCurrentGif(loadingGifs[Math.floor(Math.random() * loadingGifs.length)]);
    }, 4000);

    return () => clearInterval(interval);
  }, [loading]);

  const searchCards = async () => {
    if (!code.trim()) {
      setError("⚠️ Por favor, introduce un código de carta");
      return;
    }

    setError("");
    setLoading(true);
    setCards([]);
    setLoadingMessageIndex(0);

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code.trim() })
      });

      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        setError(data.error || "❌ Error al buscar las cartas");
        return;
      }

      if (data.length === 0) {
        setError("🔍 No se encontraron cartas con ese código");
      }

      setCards(data);
    } catch (err) {
      console.error("Error:", err);
      setError("🔌 Error de conexión con el servidor");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950">
        {/* Animated waves */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute bottom-0 left-0 right-0 h-96 bg-gradient-to-t from-blue-600/30 to-transparent animate-pulse"></div>
        </div>
        
        {/* Stars effect */}
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(2px 2px at 20% 30%, white, transparent),
                           radial-gradient(2px 2px at 60% 70%, white, transparent),
                           radial-gradient(1px 1px at 50% 50%, white, transparent),
                           radial-gradient(1px 1px at 80% 10%, white, transparent),
                           radial-gradient(2px 2px at 90% 60%, white, transparent),
                           radial-gradient(1px 1px at 33% 80%, white, transparent)`,
          backgroundSize: '200% 200%',
          animation: 'twinkle 8s ease-in-out infinite'
        }}></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-8 sm:py-12">
        {/* Floating Header */}
        <div className="text-center mb-8 sm:mb-12 space-y-4 sm:space-y-6">
          <div className="relative inline-block group">
            {/* Glow effect */}
            <div className="absolute -inset-4 bg-gradient-to-r from-yellow-600 via-red-600 to-yellow-600 rounded-3xl blur-2xl opacity-60 group-hover:opacity-100 transition-opacity duration-500 animate-pulse"></div>
            
            <div className="relative">
              <div className="flex items-center justify-center gap-3 mb-2">
                <Anchor className="w-8 h-8 sm:w-12 sm:h-12 text-yellow-400 animate-bounce" />
                <h1 className="text-4xl sm:text-7xl font-black tracking-tight">
                  <span className="bg-gradient-to-r from-yellow-400 via-red-500 to-orange-600 bg-clip-text text-transparent drop-shadow-2xl">
                    ONE PIECE
                  </span>
                </h1>
                <Sparkles className="w-8 h-8 sm:w-12 sm:h-12 text-yellow-400 animate-pulse" />
              </div>
              
              <div className="flex items-center justify-center gap-2 mb-3">
                <div className="h-px w-16 sm:w-24 bg-gradient-to-r from-transparent to-yellow-400"></div>
                <p className="text-lg sm:text-2xl font-bold text-blue-300 tracking-widest">
                  CARD GAME
                </p>
                <div className="h-px w-16 sm:w-24 bg-gradient-to-l from-transparent to-yellow-400"></div>
              </div>
            </div>
          </div>

          <div className="max-w-xl mx-auto px-4">
            <div className="bg-slate-900/70 backdrop-blur-xl rounded-2xl p-4 border border-yellow-500/30 shadow-2xl">
              <p className="text-slate-300 text-sm sm:text-base">
                🔎 Busca tus cartas favoritas · 💰 Precios mínimos España
              </p>
            </div>
          </div>
        </div>

        {/* Premium Search Card */}
        <div className="max-w-3xl mx-auto mb-8 sm:mb-12 px-4">
          <div className="relative group">
            {/* Outer glow */}
            <div className="absolute -inset-1 bg-gradient-to-r from-yellow-600 via-red-600 to-orange-600 rounded-3xl blur-xl opacity-75 group-hover:opacity-100 transition-all duration-500"></div>
            
            <div className="relative bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl shadow-2xl border border-yellow-500/20 overflow-hidden">
              {/* Top accent line */}
              <div className="h-1 bg-gradient-to-r from-yellow-500 via-red-500 to-orange-500"></div>
              
              <div className="p-6 sm:p-8">
                <div className="flex flex-col sm:flex-row gap-3">
                  <div className="relative flex-1">
                    <div className="absolute inset-0 bg-gradient-to-r from-yellow-500/10 to-red-500/10 rounded-2xl blur"></div>
                    <input
                      type="text"
                      value={code}
                      onChange={(e) => setCode(e.target.value.toUpperCase())}
                      onKeyPress={(e) => e.key === "Enter" && searchCards()}
                      placeholder="🎴 Código de carta (ej: OP01-001)"
                      className="relative w-full px-6 py-4 sm:py-5 bg-slate-950/80 border-2 border-yellow-500/30 rounded-2xl text-white placeholder-slate-500 focus:outline-none focus:border-yellow-500 focus:ring-4 focus:ring-yellow-500/20 transition-all duration-300 text-base sm:text-lg font-medium"
                    />
                    <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-yellow-500 w-5 h-5 sm:w-6 sm:h-6" />
                  </div>
                  
                  <button
                    onClick={searchCards}
                    disabled={loading}
                    className="relative group/btn px-6 sm:px-10 py-4 sm:py-5 bg-gradient-to-r from-yellow-500 via-orange-500 to-red-600 hover:from-yellow-600 hover:via-orange-600 hover:to-red-700 rounded-2xl font-black text-base sm:text-lg text-slate-900 shadow-2xl hover:shadow-yellow-500/50 transform hover:scale-105 active:scale-95 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
                  >
                    <span className="relative z-10 flex items-center gap-2 justify-center">
                      {loading ? "Buscando..." : "¡BUSCAR!"}
                      <Compass className="w-5 h-5 group-hover/btn:rotate-180 transition-transform duration-500" />
                    </span>
                    
                    {/* Button shine effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover/btn:translate-x-full transition-transform duration-1000"></div>
                  </button>
                </div>

                {error && (
                  <div className="mt-4 p-4 bg-red-900/50 backdrop-blur-sm border-2 border-red-500/50 rounded-2xl text-red-200 text-sm sm:text-base animate-shake">
                    {error}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Premium Loading State */}
        {loading && (
          <div className="max-w-2xl mx-auto mb-12 px-4">
            <div className="relative">
              <div className="absolute -inset-4 bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 rounded-3xl blur-2xl opacity-50 animate-pulse"></div>
              
              <div className="relative bg-slate-900/90 backdrop-blur-xl rounded-3xl p-6 sm:p-10 shadow-2xl border border-blue-500/30">
                <div className="flex flex-col items-center space-y-6">
                  <div className="relative">
                    <div className="absolute -inset-4 bg-gradient-to-r from-yellow-500 via-red-500 to-yellow-500 rounded-3xl blur-2xl opacity-60 animate-spin-slow"></div>
                    <img
                      src={currentGif}
                      alt="Loading"
                      className="relative w-48 h-48 sm:w-72 sm:h-72 object-cover rounded-3xl shadow-2xl border-4 border-yellow-500/50"
                    />
                  </div>
                  
                  <div className="text-center space-y-3">
                    <p className="text-xl sm:text-2xl font-bold text-yellow-400 animate-pulse">
                      {loadingMessages[loadingMessageIndex]}
                    </p>
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Premium Results Grid */}
        {cards.length > 0 && (
          <div className="px-4">
            <div className="mb-6 sm:mb-8 text-center">
              <div className="inline-block bg-slate-900/70 backdrop-blur-xl rounded-2xl px-6 py-3 border border-yellow-500/30">
                <p className="text-lg sm:text-xl font-bold text-yellow-400">
                  ⚡ {cards.length} {cards.length === 1 ? 'Carta encontrada' : 'Cartas encontradas'}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
              {cards.map((card, idx) => (
                <div
                  key={idx}
                  onMouseEnter={() => setHoveredCard(idx)}
                  onMouseLeave={() => setHoveredCard(null)}
                  className="group relative"
                >
                  {/* Card glow effect */}
                  <div className={`absolute -inset-2 bg-gradient-to-r from-yellow-600 via-red-600 to-orange-600 rounded-3xl blur-xl opacity-0 group-hover:opacity-60 transition-all duration-500 ${hoveredCard === idx ? 'animate-pulse' : ''}`}></div>
                  
                  <div className="relative bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl overflow-hidden shadow-2xl border-2 border-slate-700 group-hover:border-yellow-500/50 transition-all duration-500 transform group-hover:-translate-y-3 group-hover:scale-105">
                    {/* Shine effect overlay */}
                    <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                    
                    {/* Card Image */}
                    <div className="relative aspect-[2.5/3.5] overflow-hidden">
                      <img
                        src={card.image}
                        alt={card.text}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                      />
                      
                      {/* Gradient overlay */}
                      <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/50 to-transparent"></div>
                      
                      {/* Price badge with shine */}
                      {card.price !== undefined && (
                        <div className="absolute top-3 right-3 z-10">
                          <div className="relative group/price">
                            <div className="absolute inset-0 bg-green-400 rounded-full blur-md opacity-75 group-hover/price:opacity-100 transition-opacity"></div>
                            <div className="relative bg-gradient-to-r from-green-500 to-emerald-600 text-white px-4 py-2 rounded-full font-black shadow-2xl text-sm sm:text-base">
                              {card.price.toFixed(2)}€
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {/* Sparkle effect */}
                      {hoveredCard === idx && (
                        <Sparkles className="absolute top-3 left-3 w-6 h-6 text-yellow-400 animate-pulse z-10" />
                      )}
                    </div>

                    {/* Card Info */}
                    <div className="p-4 sm:p-5 space-y-3">
                      <h4 className="font-bold text-base sm:text-lg line-clamp-2 text-yellow-400 group-hover:text-yellow-300 transition-colors">
                        {card.text}
                      </h4>
                      
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="font-mono text-xs sm:text-sm bg-slate-950/80 px-3 py-1.5 rounded-lg text-yellow-400 border border-yellow-500/30">
                            {card.code}
                          </span>
                          <span className="text-xs sm:text-sm text-slate-400 font-medium">
                            {card.version || "V.1"}
                          </span>
                        </div>
                        
                        <div className="text-xs sm:text-sm text-slate-400 truncate">
                          📦 {card.collection}
                        </div>
                      </div>
                    </div>

                    {/* Bottom accent */}
                    <div className="h-1 bg-gradient-to-r from-yellow-500 via-red-500 to-orange-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && cards.length === 0 && !error && (
          <div className="text-center py-12 sm:py-20 px-4">
            <div className="inline-block p-8 sm:p-12 bg-slate-900/70 backdrop-blur-xl rounded-3xl border border-slate-700 shadow-2xl">
              <Compass className="w-16 h-16 sm:w-24 sm:h-24 text-yellow-500/50 mx-auto mb-4 sm:mb-6 animate-spin-slow" />
              <p className="text-xl sm:text-2xl font-bold text-slate-300 mb-2">
                ¡Comienza tu búsqueda!
              </p>
              <p className="text-sm sm:text-base text-slate-500">
                Introduce un código de carta para navegar por el Grand Line
              </p>
            </div>
          </div>
        )}
      </div>

      <style>{`
        @keyframes twinkle {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 1; }
        }
        
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        
        .animate-spin-slow {
          animation: spin 8s linear infinite;
        }
        
        .animate-shake {
          animation: shake 0.5s ease-in-out;
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}