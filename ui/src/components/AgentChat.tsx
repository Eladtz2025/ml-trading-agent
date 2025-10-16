import { useState, form, useEffect } from 'react';
import '../style.css';

export default function AgentChat() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('';

  const handleSubmit = async (ev) => {
    ev.default();
    const res = await fetch('/agent/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({ query })
    });
    const data = await res.json();
    setResponse(data.response);
  }

  return (
    <form on submit={handleSubmit}>
      <input type="text" value={query} onChange={e(e)=>setQuery(e.target.value || '')} />
      <button type="submit">Send</button>
      <div>
        <strong>Response:</strong> {response}
      </div>
    </form>
  );
}