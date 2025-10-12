import { dashboardSpec, getComponentDetails } from './dashboardSpec.js';

const kindToLabel = {
  chart: 'Chart',
  stat: 'Metric',
  table: 'Table',
  timeline: 'Timeline',
  control: 'Control',
  distribution: 'Distribution',
  text: 'Viewer',
  gauge: 'Gauge'
};

const renderComponentCard = (componentId) => {
  const component = getComponentDetails(componentId);
  const kindLabel = kindToLabel[component.kind] || 'Component';

  return `
    <article class="component-card component-card--${component.kind}" data-component-id="${component.id}">
      <header>
        <span class="component-kind">${kindLabel}</span>
        <h3>${component.title}</h3>
      </header>
      <p>${component.description}</p>
      <footer>
        <button type="button" class="component-action" aria-label="Open ${component.title}">
          Open ${component.title}
        </button>
      </footer>
    </article>
  `;
};

const renderSection = (section) => {
  const cards = section.components.map(renderComponentCard).join('\n');

  return `
    <section id="${section.id}" class="dashboard-section">
      <div class="section-header">
        <div>
          <h2>${section.title}</h2>
          <p>${section.description}</p>
        </div>
        <span class="section-count" aria-label="${section.components.length} components">
          ${section.components.length}
        </span>
      </div>
      <div class="component-grid">
        ${cards}
      </div>
    </section>
  `;
};

export const buildDashboardMarkup = () => {
  const navLinks = dashboardSpec.sections
    .map((section) => `<a href="#${section.id}" class="hero-nav__link">${section.title}</a>`)
    .join('\n');

  const sectionsMarkup = dashboardSpec.sections.map(renderSection).join('\n');

  return `
    <div class="app-shell">
      <header class="hero">
        <div>
          <p class="eyebrow">Phoenix</p>
          <h1>${dashboardSpec.heroTitle}</h1>
          <p class="subtitle">${dashboardSpec.heroSubtitle}</p>
        </div>
        <nav aria-label="Section navigation" class="hero-nav">
          ${navLinks}
        </nav>
      </header>
      <main>
        ${sectionsMarkup}
      </main>
      <footer class="app-footer">
        <p>Last refreshed just now · Data sources: Live OMS, Feature Store, Backtest Engine</p>
      </footer>
    </div>
  `;
};

export const mountDashboard = (rootElement) => {
  if (!rootElement) {
    throw new Error('Root element is required to mount the dashboard');
  }

  rootElement.innerHTML = buildDashboardMarkup();
};

if (typeof document !== 'undefined') {
  const root = document.getElementById('root');
  if (root) {
    mountDashboard(root);
  }
}
