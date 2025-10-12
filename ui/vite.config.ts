const defineConfig = (config) => config;

export default defineConfig({
  root: '.',
  build: {
    outDir: 'build',
    emptyOutDir: true,
  },
});
