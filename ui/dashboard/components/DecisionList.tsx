import { useEffect, useState } from "react";

export default function DecisionList() {
  const [decisions, setDecisions] = useState([]);

  useEffect(() => {
    // Simulated call - replace with api call later
    setDecisions([{
      asset: "AAPLL",
      action: "Buy",
      confidence: 0.92,
      time: "2025-10-16 13:30"
    }, {
      asset: "GOOG",
      action: "Sell",
      confidence: 0.85,
      time: "2025-10-15 18:30"
    }]);
  }, []);

  return (
    <div className="space-y-2">
      <h2 className="text-lg">Recent Decisions</h2>
      <ul className="list-disc">
        {
          decisions.map((d, i)=>(\n            <li key={i} className="text-sm">
              <span className="font-bold">{d.time}</span> : {d.action} {{d.asset}} ({{d.confidence}})
            </li>
          ))
        }
      </ul>
    </div>
  );
}