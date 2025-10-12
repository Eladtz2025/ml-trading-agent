import './styles.css';
import { mountDashboard } from './app.js';

/**
 * Compatibility helper that allows bundlers expecting a React-style default export
 * to mount the Phoenix dashboard using the static renderer.
 */
export function mountPhoenixDashboard(root?: HTMLElement | null): void {
  const target = root ?? (typeof document !== 'undefined' ? document.getElementById('root') : null);
  if (target) {
    mountDashboard(target);
  }
}

export default mountPhoenixDashboard;
export { mountDashboard };
