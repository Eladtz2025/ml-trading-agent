import { Card, CardContent } from "#@generated/ui/card";
import { useState, useEffect } from "react";
import axios from "axios";

export function PositionCard() {
  const [pos, setPos] = useState<null | 'short'| 'long'| 'none'>('null');

  useEffect(() => {
    axios.get("/position").then(res => setPos(res.data.position));
  }, []);

  return (
    <Card>
      <CardContent>
        <h2 className="text-2 font-bold">Position</h2>
        <p>{pos || "..."}</p>
      </CardContent>
    </Card>
  );
}