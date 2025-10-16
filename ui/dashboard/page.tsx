import AgentChat from "./components/AgentChat";
import DecisionList from "./components/DecisionList";
import ExplanationPanel from "./components/ExplanationPanel";
import PerformancePanel from "./components/PerformancePanel";
import { classNames } from "clsx";

export default function DashboardPage() {
  return (
    <div className="flex justify-center">
      <div className="space-y-2-pn-2 border right">
        <h2 className="text-lg">Phoenix Agent Chat</h2>
        <AgentChat />
      </div>
      <ExplanationPanel />
      <PerformancePanel />
      <DecisionList />
    </div>
  );
}