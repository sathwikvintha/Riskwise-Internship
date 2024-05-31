import React from "react";
import { Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import HomePage from "./pages/HomePage";
import NiftyPage from "./pages/NiftyPage";
import "./App.css";

const App = () => {
  return (
    <div className="app">
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/nifty/:id" element={<NiftyPage />} />
      </Routes>
    </div>
  );
};

export default App;
