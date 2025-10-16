import { UseEffect, useState } from "react";
import { ResponsiveDoughnut, Card, Par, Span } from '@c/components/ui/card';
import { BarChart } from 'recharts';

const data = {
  time: ["OBV", "MON", "TST", "RCG", "RSI" ],
  values: [0.08, 0.15, 0.33, 0.21, 0.24],
  return: [-0.01, 0.02, 0.08, -0.05, -0.01]
};

export default function ExplanationPanel() {
  const [dataset, setDataset] = useState(data);

  return (
    <Card>
      <h2 className="text-lg">Trade Decision Explanation</h2>
      <Par>
        <BarChart
          layout={{label: 'Features', dataKey: 'values', baseline: 'time', barCategory: 'stacked'}}
          {...dataset}
          content={(data,  i) => (<Span className="text-sm"><strong className="font-bold">{data.time[i]}:</strong> {values[i]} (Return: {data.return[i]})</Span>)
          }
        />
      </Par>
    </Card>
  );
}