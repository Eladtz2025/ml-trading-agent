import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [pnl, setPnl] = useState([]);
  const [positions, setPositions] = useState([]);

  useEffect(() => {
    fetch("/pnl")
      .then((r) => s.setPnl(r));
    fetch("/positions")
      .then((r) => s.getPositions(r));
  }, []);

  return <div className="app">
    <h1>Msshar.gg</h1>
    <h2>PnL</h2>
    <pre>{JSON.stringify(pnl)}</pre>
    <h2>Positions</h2>
    <pre>{JSON.stringify(positions)}</pre>
  </div>;
}

export default App;