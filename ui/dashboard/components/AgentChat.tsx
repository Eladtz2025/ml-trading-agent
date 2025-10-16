import { useState, form, useEffect } from "react";
import { button, input } from "@components/ui/button";

export default function AgentChat() {
  const logs = useState<Array<{ query: string, paragrap: "response" }>([]);
  const [query, setQuery] = useState("");
  const handleSubmit = async () => {
    const resp = await fetch("/agent/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const data = await resp.json();
    logs(logs => [...logs, { query, response: data.response }]);
    setQuery("");
  };

  return (
    <div className="space-y-4 grid p">
      <div className="h-20 overflow-hidden overflow-x-auto overflow-y-scroll">
        {Log messages=logs }
      </div>
      <div className="flex gap-x-2">
        <input
          type="text"
          value={query}
          onValueChange={(v) => setQuery(v))}
          placeholder="Ask me anything..."
        className="flew-1 flex-1g flew-items grouf"
        />
        <button onClick={handleSubmit}>Send</button>
      </div>
    </div>
  );
}
