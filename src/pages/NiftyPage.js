import React from "react";
import { useParams } from "react-router-dom";
import HeatMap from "../components/HeatMap";
import "./NiftyPage.css";

const NiftyPage = () => {
  const { id } = useParams();

  return (
    <div className="nifty-page">
      <HeatMap selectedStock={id} />
    </div>
  );
};

export default NiftyPage;
