import React from 'react';
import {
  ComponentKind,
  DashboardComponent,
  dashboardSpec,
  getComponentDetails
} from '../data/dashboardSpec';

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
  const [actionStatus, setActionStatus] = React.useState<
    Record<string, 'idle' | 'launching' | 'complete'>
  >({});

  const handleComponentAction = (component: DashboardComponent) => {
    if (!component.cta) {
      return;
    }

    if (component.cta.type === 'vercel') {
      setActionStatus((prev) => ({ ...prev, [component.id]: 'launching' }));

      if (typeof window !== 'undefined') {
        const href = component.cta.href ?? 'https://vercel.com/new';
        const openWindow = () => {
          const newWindow = window.open(href, '_blank', 'noopener,noreferrer');
          setTimeout(() => {
            setActionStatus((prev) => ({
              ...prev,
              [component.id]: newWindow ? 'complete' : 'idle'
            }));
          }, 300);
        };

        try {
          openWindow();
        } catch (error) {
          setActionStatus((prev) => ({ ...prev, [component.id]: 'idle' }));
          console.error('Failed to open Vercel deployment window', error);
        }
      } else {
        setActionStatus((prev) => ({ ...prev, [component.id]: 'idle' }));
      }

      return;
    }

    if (component.cta.href && typeof window !== 'undefined') {
      window.open(component.cta.href, component.cta.target ?? '_self', 'noopener,noreferrer');
    }
  };

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
                const status = actionStatus[component.id] ?? 'idle';
                const actionLabel = component.cta?.label ?? `Open ${component.title}`;
                const isActionDisabled = component.cta?.type === 'vercel' && status === 'launching';

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
                        className={`component-action${component.cta?.type === 'vercel' ? ' component-action--primary' : ''}`}
                        onClick={() => handleComponentAction(component)}
                        disabled={isActionDisabled}
                        aria-busy={isActionDisabled}
                        aria-label={actionLabel}
                      >
                        {status === 'launching' ? 'Opening…' : actionLabel}
                      </button>
                      {component.cta?.type === 'vercel' && status === 'complete' && (
                        <p className="component-status" role="status">
                          Deployment flow opened in a new tab. Complete the steps in Vercel to finish deploying.
                        </p>
                      )}
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
