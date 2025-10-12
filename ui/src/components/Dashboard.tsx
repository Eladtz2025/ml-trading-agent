import React from 'react';
import { ComponentKind, dashboardSpec, getComponentDetails } from '../data/dashboardSpec';

type KindLabelMap = Record<ComponentKind, string> & Record<string, string>;

const kindToLabel: KindLabelMap = {
  chart: 'Chart',
  stat: 'Metric',
  table: 'Table',
  timeline: 'Timeline',
  control: 'Control',
  distribution: 'Distribution',
  text: 'Viewer',
  gauge: 'Gauge'
};

const Dashboard: React.FC = () => {
  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Phoenix</p>
          <h1>{dashboardSpec.heroTitle}</h1>
          <p className="subtitle">{dashboardSpec.heroSubtitle}</p>
        </div>
        <nav aria-label="Section navigation" className="hero-nav">
          {dashboardSpec.sections.map((section) => (
            <a key={section.id} href={`#${section.id}`} className="hero-nav__link">
              {section.title}
            </a>
          ))}
        </nav>
      </header>

      <main>
        {dashboardSpec.sections.map((section) => (
          <section key={section.id} id={section.id} className="dashboard-section">
            <div className="section-header">
              <div>
                <h2>{section.title}</h2>
                <p>{section.description}</p>
              </div>
              <span className="section-count" aria-label={`${section.components.length} components`}>
                {section.components.length}
              </span>
            </div>
            <div className="component-grid">
              {section.components.map((componentId) => {
                const component = getComponentDetails(componentId);
                const kindLabel = kindToLabel[component.kind] ?? 'Component';

                return (
                  <article key={component.id} className={`component-card component-card--${component.kind}`}>
                    <header>
                      <span className="component-kind">{kindLabel}</span>
                      <h3>{component.title}</h3>
                    </header>
                    <p>{component.description}</p>
                    <footer>
                      <button
                        type="button"
                        className="component-action"
                        aria-label={`Open ${component.title}`}
                      >
                        Open {component.title}
                      </button>
                    </footer>
                  </article>
                );
              })}
            </div>
          </section>
        ))}
      </main>

      <footer className="app-footer">
        <p>Last refreshed just now · Data sources: Live OMS, Feature Store, Backtest Engine</p>
      </footer>
    </div>
  );
};

export default Dashboard;
