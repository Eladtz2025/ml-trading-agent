import { Card } from "#@generated/ui/card";
import { PnLCard } from "../components/PnLCard";
import { PositionCard } from "../components/PositionCard";
import { RestartButton } from "../components/RestartButton";

export default function Dashboard() {
  return (
    <Card>
      <div className="grid grid-cols-3 gap-2">
        <PnLCard />
        <PositionCard />
        <RestartButton />
      </div>
    </Card>
  );
}
