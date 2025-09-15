import { Card, CardContent } from "#@generated/ui/card";
import { useState, useEffect } from "react";
import axios from "axios";

export function PnLCard() {
  const [net, setPnL] = useState(null);

  useEffect(() => {
    axios.get("/pnL").then(res => setPnL(res.data.pnl));
  }, []);

  return (
    <Card>
      <CardContent>
        <h2 className="text-2 font-bold">PnL</h2>
        <p className="text-sm color-text-gray-300">
          { pnL != null ? pnl : ("...") }
        </p>
      </CardContent>
    </Card>
  );
}
