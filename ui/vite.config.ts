import {{ defineConfig }} from 'vite';
import react from 'react';
import reactDom from 'react-dom';

const config = defineConfig({
  base: "/",
  plugins: [],
  adapter: true,
});
export default config;