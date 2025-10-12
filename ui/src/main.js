import { mountDashboard } from './app.js';
import './styles.css';

const root = document.getElementById('root');
if (root) {
  mountDashboard(root);
}
