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
  type ComponentActionState = {
    status: 'idle' | 'launching' | 'complete' | 'error';
    message?: string;
    artifacts?: string[];
  };

  const [actionStatus, setActionStatus] = React.useState<Record<string, ComponentActionState>>({});

  const updateStatus = React.useCallback(
    (componentId: string, state: ComponentActionState) => {
      setActionStatus((prev) => ({ ...prev, [componentId]: state }));
    },
    []
  );

  const handleComponentAction = async (component: DashboardComponent) => {
    const actionType = component.cta?.type ?? 'action';

    if (actionType === 'vercel') {
      updateStatus(component.id, { status: 'launching' });

      if (typeof window !== 'undefined') {
        const href = component.cta?.href ?? 'https://vercel.com/new';
        const openWindow = () => {
          const newWindow = window.open(href, '_blank', 'noopener,noreferrer');
          setTimeout(() => {
            updateStatus(component.id, {
              status: newWindow ? 'complete' : 'idle',
              message: newWindow ? 'Deployment flow opened in a new tab.' : undefined
            });
          }, 300);
        };

        try {
          openWindow();
        } catch (error) {
          updateStatus(component.id, { status: 'idle' });
          console.error('Failed to open Vercel deployment window', error);
        }
      } else {
        updateStatus(component.id, { status: 'idle' });
      }

      return;
    }

    if (actionType === 'link') {
      if (component.cta?.href && typeof window !== 'undefined') {
        window.open(component.cta.href, component.cta.target ?? '_self', 'noopener,noreferrer');
      }
      return;
    }

    try {
      updateStatus(component.id, { status: 'launching' });
      const response = await fetch(`/api/actions/${component.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });

      if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(errorBody || 'Failed to trigger action');
      }

      const payload = (await response.json()) as {
        message?: string;
        artifacts?: string[];
      };

      updateStatus(component.id, {
        status: 'complete',
        message: payload.message ?? 'Action completed successfully.',
        artifacts: payload.artifacts ?? []
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Action failed to execute.';
      updateStatus(component.id, { status: 'error', message });
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
                const status = actionStatus[component.id] ?? { status: 'idle' };
                const actionLabel = component.cta?.label ?? `Trigger ${component.title}`;
                const isActionDisabled = status.status === 'launching';

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
                        {status.status === 'launching' ? 'Working…' : actionLabel}
                      </button>
                      {status.status === 'complete' && (
                        <div className="component-status" role="status">
                          <p>{status.message}</p>
                          {status.artifacts && status.artifacts.length > 0 && (
                            <ul className="component-status__artifacts">
                              {status.artifacts.map((artifact) => (
                                <li key={artifact}>
                                  <code>{artifact}</code>
                                </li>
                              ))}
                            </ul>
                          )}
                        </div>
                      )}
                      {status.status === 'error' && (
                        <p className="component-status component-status--error" role="status">
                          {status.message}
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
