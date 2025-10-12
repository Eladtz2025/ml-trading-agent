import { promises as fs } from 'fs';
import path from 'path';

async function main() {
  const sourcePath = path.resolve('.', 'app.js');
  const source = await fs.readFile(sourcePath, 'utf8');

  const requiredAnchors = [
    '📈 Overview',
    '🧠 Model Insights',
    '🧪 Backtest / Live Run Analysis',
    '⚠️ Risk Monitor',
    '📊 Data & Label QA',
    '⚙️ Config & Ops',
    '🤖 Phoenix Agent'
  ];

  const missing = requiredAnchors.filter((label) => !source.includes(label));

  if (missing.length) {
    console.error('Validation failed. Missing sections:', missing.join(', '));
    process.exit(1);
  }

  console.log('Validation passed. All dashboard sections are defined.');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
