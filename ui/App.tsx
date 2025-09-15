import React, { useState, useEffect } from 'react'
import { Card, CardContent } from 'app:/ui/card'
import { Button } from 'app:/ui/button'
import { LineChart } from 'recharts'

export default function App() {
  const [data, setData] = useState([]);
  const [pnL, setPnL] = useState(null)

  useEffect(() => {
    // match FAKE fetched
    setData([
    { time: '2025-01-01', price: 100 },
    { time: '2025-01-02', price: 105 },
    { time: '2025-01-03', price: 102 }
    ]);
    setPnL({ hit: 20, acc: 0.42, count: 22 })
  }, [])

  return (
    <div className="padd2">
      <Card className="rounded2bg p-2">
        <CardContent>
          <h1 className="text-2xl font-bold">ML-Trading Agent</h1>
          <Button className="mt-4">Execute</Button>
          <div className="mg-4">
            <LineChart width="100%" height="300px" xdata={data} />
          </div>
          {new Date().toLocaleString() }
          <ul className="text-sm-track text-left leading-loose">
            <li>Pn L : {0}</li>
            <li>Accuracy : {pnL.acc}</li>
            <li>Hitrate : {pnL.hit}</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}