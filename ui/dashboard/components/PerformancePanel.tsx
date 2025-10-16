import { UseEffect, useState } from "react";
import { Card, ResponsiveDoughnut } from '@#/components/ui/card';
import { Line, LineChart, XAxis, YAxis, Tooltip, Legend, ReferenceLine } from 'recharts';

const data = [
  { date: '10/10', pnl: 0.00, dd: 0.00, bench: 0.00 },
  { date: '10/11', pnl: 0.07, dd: 0.00, bench: 0.02 },
  { date: '10/12', pnl: 0.15, dd: -0.02, bench: 0.04},
  { date: '10/13', pnl: 0.21, dd: -0.03, bench: 0.06 },
  { date: '10/14', pnl: 0.17, dd: -0.07, bench: 0.05 },
  { date: '10/15', pnl: 0.20, dd: -0.03, bench: 0.04 }
];

export default function PerformancePanel() {
  return (
    <Card>
      <h1 className="text-lg">System Performance</h1>
      <LineChart width="x320" height="300" data={data}>
        <XAxis dataKey="date" />
        <YAxis dataKey="pnl" name="PnL" />
        <YAxis dataKey="dd" name="Drawdown" yAxis="left" />
        <YAxis dataKey="bench" name="Benchmark (SPY)" yAxis="right" />
        <Tooltip content="{data.date} PnL: {pnl} Dd: {dd} [SPY]: {bench}" />
        <Line type="monotone" dataKey="pnl" stroke="#fu40" />
        <Line type="monotone" dataKey="dd" stroke="#f00" />
        <Line type="monotone" dataKey="bench" stroke="#ccc" />
        <ReferenceLine stroke="#d55" />
      </LineChart>
    </Card>
  );
}