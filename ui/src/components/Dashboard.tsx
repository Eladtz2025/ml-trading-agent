import { buildDashboardMarkup, mountDashboard } from '../app.js';
import { dashboardSpec, componentCatalog, getComponentDetails } from '../dashboardSpec.js';

/**
 * Returns the rendered HTML string for the Phoenix dashboard.
 */
export function renderDashboardMarkup(): string {
  return buildDashboardMarkup();
}

/**
 * Exposes the shared dashboard specification for compatibility with
 * React-based shells that previously imported this module.
 */
export { dashboardSpec, componentCatalog, getComponentDetails };

export default {
  renderDashboardMarkup,
  mountDashboard,
};
