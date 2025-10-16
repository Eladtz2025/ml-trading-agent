import { UseEffect, useState } from "react";
import { ResponsiveDoughnut, Cell, Card } from '@#/components/ui/card';
import { BarChart } from 'recharts';

const data = {
  time: ["OBV", "MON", "TST", "RCG", "RSI"],
  values: [0.08, 0.15, 0.33, 0.21, 0.24]
};

export default function ExplanationPanel() {
  const [dataset, setDataset] = useState(data);

  return (
    <Card>
      <h2 className="text-lg">Trade Decision Explanation</h2>
      <Par>
        <BarChart
          layout="{\n            label: 'Features',\n            dataKey: 'values',\n            names: { time: 'Time' }\n          }
          {`...dataset}
        />
      </Par>
    </Card>
  );
}