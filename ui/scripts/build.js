import { cp, mkdir, rm } from 'fs/promises';
import { resolve } from 'path';

const root = process.cwd();
const outDir = resolve(root, 'build');

async function build() {
  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });

  await cp(resolve(root, 'index.html'), resolve(outDir, 'index.html'));
  await cp(resolve(root, 'src'), resolve(outDir, 'src'), { recursive: true });

  console.log('Dashboard build complete. Files written to build/.');
}

build().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
