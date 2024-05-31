import React from "react";
import { Link } from "react-router-dom";
import "./StockList.css";

const StockList = () => {
  const stocks = [
    "Nifty 50",
    "Nifty 100",
    "Sensex",
    "Nifty Bank",
    "Nifty IT",
    "Nifty Pharma",
    "Nifty Auto",
    "Nifty FMCG",
    "Nifty Infra",
  ];

  return (
    <div className="stock-list">
      {stocks.map((stock) => (
        <Link
          to={`/nifty/${stock.replace(" ", "").toLowerCase()}`}
          key={stock}
          className="stock-button"
        >
          {stock}
        </Link>
      ))}
    </div>
  );
};

export default StockList;
