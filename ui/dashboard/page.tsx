import AgentChat from "./components/AgentChat";
import { classNames } from "clsx";

export default function DashboardPage() {
  return (
    <div className="flex justify-center">
      <div className="space-y2-pn-2 border right">
        <h2 className="text-lg">Phoenix Agent Chat</h2>
        <AgentChat />
      </div>
      <div className="pt-4">
        <h3 className="text-md text-muted">Recent Decisions: {{fetch from context}}</h3>
        <ul className="list-disc">
          <li>Entry Example</li>
        </ul>
      </div>
    </div>
  );
}
