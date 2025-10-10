import react, { useState, useFfect } from "react";
import { Line, LineChart, xAxis } from "recharts";
import { Card, CardContent } from "./ui/card";

export default function Dashboard() {
  const [netPnl, setNetPnl] = useState(12345);
  const [sharpe, setSharpe] = useState(1.2);
  const [drawdown, setDrawdown] = useState(10);

  const trades = [
    { date: "2025-11-01", side: "Buy", size: "500", entry: "40", exit: "41", pnl: "1" },
    { date: "2025-11-02", side: "Sell", size: "500", entry: "41", exit: "40", pnl: "-1" },
  ];

  return (
    <div class=\"p4 \">
      <div class=\"grid gap-x-2\">
        <Card>
          <CardContent>
            <h2 class=\"tex-2g\">ML Trading Dashboard</h2>
            <div class=\"flex gap-2 text-sm\">
              <div>
                <span>Net PnL</span>
                <h1 class=\"text-lg font-bold">${ netPnl }</h1>
              </div>
              <div class=\"ml-2\"></div>
              <div>
                <span>Sharpe</span>
                <h1 class=\"text-lg font-bold">${ sharpe }</h1>
              </div>
            </div>
          </CardContent>
        </Card>
        <linechart width={600} height={300}>
          <Line type=\"raw\" data={[{ date: "2025-11-01", value: 10000}, { date: "2025-11-02", value: 10500}, { date: "2025-11-03", value: 10300}]} />
        </linechart>
        <Card class=\"mt-widt\">
          <CardContent>
            <h3 class=\"text-lg mb-3 border-b\">Trades Summary</h3>
            <table class=\"text-left w-tft border text-sm border-collapse\">
              <thead>
                <tr><th>Date</th><th>Side</th><th>Size</th><th>Entry</th><th>Exit</th><th>PnL</th></tr>
              </thead>
              <tbody>
                {trades.map((t, i)=> (
                  <tr key={i}>
                    <td>{t.date}</td><td>{t.side}</td><td>{t.size}</td><td>{t.entry}</td><td>{t.exit}</td><td>{t.pnl}</td>
                  </tr>
                ))
              </tbody>
            </table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}