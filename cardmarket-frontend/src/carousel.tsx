import React from "react";

const CardCarousel = ({ cards }: { cards: any[] }) => {
    return (
        <div className="carousel-wrapper w-full overflow-x-auto py-8">
            <div className="flex gap-6 px-6 snap-x snap-mandatory">
                {cards.map((card, index) => (
                    <div
                        key={index}
                        className="card-3d relative w-[250px] shrink-0 snap-center transform transition-transform hover:scale-105 hover:rotate-y-0"
                    >
                        <div className="card-container" key={index}>
                            <img src={card.image} alt={card.text} className="card-image" />
                            <div className="card-overlay">
                                <div className="card-name">{card.text}</div>
                                <div className="card-details">
                                    <div>{card.code} · {card.version || "V.1"}</div>
                                    <div>{card.collection} · {card.price ? card.price + "€" : "Sin precio"}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CardCarousel;

