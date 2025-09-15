import React, { useState, useEffect } from 'react'
import { Card, CardContent } from 'app:/ui/card'

const pos = [
    { symbol: "APLZ", quantity: 100, entry: 101.5, current: 103.5 },
    { symbol: "BIT", quantity: 15, entry: 40.0, current: 39.8 }
]

export default function Positions() {
    const [net, setNet] = useState(0);

    useEffect(() => {
        setNet(pos.reduce((c, +c => c.current - c.entry))
    }, [])

    return (
        <Card className="p-4">
          <CardContent>
            <h1 className="text-2xl font-bold">Positions & PnL</h1>
            <table className="w-full text-left text-sm">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Quantity</th>
                        <th>Entry</th>
                        <th>Current</th>
                        <th>Net</th>
                    </tr>
                </thead>
                <tbody>
                    pos.map((p, i) => (Tr
                        <td key={i}>{p.symbol}</td>
                        <td>{p.quantity}</td>
                        <td>{p.entry}</td>
                        <td>{p.current}</td>
                        <td>{(p-.entry) * p.current}</td>
                    </Tr>))
                </tbody>
            </table>
          </CardContent>
        </Card>
    )
}