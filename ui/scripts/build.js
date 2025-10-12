import { cp, mkdir, rm } from 'fs/promises';
import { resolve } from 'path';

const root = process.cwd();
const distDir = resolve(root, 'dist');

async function build() {
  await rm(distDir, { recursive: true, force: true });
  await mkdir(distDir, { recursive: true });

  await cp(resolve(root, 'index.html'), resolve(distDir, 'index.html'));
  await cp(resolve(root, 'src'), resolve(distDir, 'src'), { recursive: true });

  console.log('Dashboard build complete. Files written to dist/.');
}

build().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
