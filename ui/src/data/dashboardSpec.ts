export type ComponentKind =
  | 'chart'
  | 'stat'
  | 'table'
  | 'timeline'
  | 'control'
  | 'distribution'
  | 'text'
  | 'gauge';

export interface ComponentCTA {
  label: string;
  href?: string;
  target?: '_blank' | '_self';
  type?: 'link' | 'vercel';
}

export interface DashboardComponent {
  id: string;
  title: string;
  description: string;
  kind: ComponentKind;
  cta?: ComponentCTA;
}

export interface DashboardSection {
  id: string;
  title: string;
  description: string;
  components: string[];
}

export interface DashboardSpec {
  heroTitle: string;
  heroSubtitle: string;
  sections: DashboardSection[];
}

export const componentCatalog: Record<string, DashboardComponent> = {
  equity_curve: {
    id: 'equity_curve',
    title: 'Equity Curve',
    description: 'Tracks cumulative strategy returns with annotations for major inflection points.',
    kind: 'chart'
  },
  daily_pnl: {
    id: 'daily_pnl',
    title: 'Daily P&L',
    description: 'Bar breakdown of daily profit and loss including overnight carry.',
    kind: 'distribution'
  },
  sharpe_metrics: {
    id: 'sharpe_metrics',
    title: 'Sharpe Metrics',
    description: 'Live, trailing-30, and trailing-90 Sharpe ratios with thresholds.',
    kind: 'stat'
  },
  exposure_map: {
    id: 'exposure_map',
    title: 'Exposure Map',
    description: 'Heatmap of gross and net exposure by asset class and region.',
    kind: 'chart'
  },
  alerts_summary: {
    id: 'alerts_summary',
    title: 'Alerts Summary',
    description: 'Recent alerts grouped by severity and resolution state.',
    kind: 'timeline'
  },
  hit_rate: {
    id: 'hit_rate',
    title: 'Hit Rate',
    description: 'Win/loss ratio across time buckets and signal strength bands.',
    kind: 'stat'
  },
  shap_top_features: {
    id: 'shap_top_features',
    title: 'Top SHAP Features',
    description: 'Ranked list of the most influential features driving predictions.',
    kind: 'table'
  },
  feature_drift_chart: {
    id: 'feature_drift_chart',
    title: 'Feature Drift',
    description: 'Distribution drift score for critical features versus the training baseline.',
    kind: 'chart'
  },
  target_distribution: {
    id: 'target_distribution',
    title: 'Target Distribution',
    description: 'Histogram of realized labels versus forecasted probabilities.',
    kind: 'distribution'
  },
  challenger_vs_champion: {
    id: 'challenger_vs_champion',
    title: 'Challenger vs Champion',
    description: 'Side-by-side comparison of candidate and production model lift.',
    kind: 'chart'
  },
  trade_list_table: {
    id: 'trade_list_table',
    title: 'Trade List',
    description: 'Detailed ledger of executed trades with P&L attribution.',
    kind: 'table'
  },
  price_chart_with_signals: {
    id: 'price_chart_with_signals',
    title: 'Price Chart + Signals',
    description: 'Asset price history annotated with entry and exit signals.',
    kind: 'chart'
  },
  holding_period_dist: {
    id: 'holding_period_dist',
    title: 'Holding Period Distribution',
    description: 'Distribution of holding periods segmented by strategy.',
    kind: 'distribution'
  },
  performance_metrics_table: {
    id: 'performance_metrics_table',
    title: 'Performance Metrics',
    description: 'Summary statistics including CAGR, max drawdown, and volatility.',
    kind: 'table'
  },
  monte_carlo_scenarios: {
    id: 'monte_carlo_scenarios',
    title: 'Monte Carlo Scenarios',
    description: 'Simulated equity curves with percentile bands.',
    kind: 'chart'
  },
  live_drawdown: {
    id: 'live_drawdown',
    title: 'Live Drawdown',
    description: 'Current drawdown versus max allowable drawdown with trend.',
    kind: 'chart'
  },
  leverage_gauge: {
    id: 'leverage_gauge',
    title: 'Leverage Gauge',
    description: 'Current leverage ratio with alarm thresholds.',
    kind: 'gauge'
  },
  exposure_by_asset: {
    id: 'exposure_by_asset',
    title: 'Exposure by Asset',
    description: 'Allocation pie chart by symbol, sector, and direction.',
    kind: 'chart'
  },
  risk_alerts_log: {
    id: 'risk_alerts_log',
    title: 'Risk Alerts Log',
    description: 'Chronological log of risk alerts, owners, and remediation steps.',
    kind: 'timeline'
  },
  stop_trigger_events: {
    id: 'stop_trigger_events',
    title: 'Stop Trigger Events',
    description: 'Recent stop-loss and circuit breaker activations.',
    kind: 'timeline'
  },
  anomaly_timeline: {
    id: 'anomaly_timeline',
    title: 'Anomaly Timeline',
    description: 'Time series of detected data anomalies and severity.',
    kind: 'timeline'
  },
  missing_data_table: {
    id: 'missing_data_table',
    title: 'Missing Data Table',
    description: 'Tabular review of missing features by dataset and partition.',
    kind: 'table'
  },
  triple_barrier_distribution: {
    id: 'triple_barrier_distribution',
    title: 'Triple Barrier Distribution',
    description: 'Distribution of barrier outcomes and label latency.',
    kind: 'distribution'
  },
  feature_coverage_map: {
    id: 'feature_coverage_map',
    title: 'Feature Coverage Map',
    description: 'Heatmap of feature availability across exchanges and sessions.',
    kind: 'chart'
  },
  current_config_viewer: {
    id: 'current_config_viewer',
    title: 'Current Config Viewer',
    description: 'Rendered view of the active deployment config with diff highlighting.',
    kind: 'text'
  },
  config_selector_launcher: {
    id: 'config_selector_launcher',
    title: 'Config Selector Launcher',
    description: 'Control panel to swap configs, roll back, or schedule changes.',
    kind: 'control'
  },
  vercel_deploy: {
    id: 'vercel_deploy',
    title: 'Deploy to Vercel',
    description: 'Launch a guided deployment of this dashboard to Vercel without leaving the command center.',
    kind: 'control',
    cta: {
      label: 'Deploy to Vercel',
      href: 'https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fmltradingai%2Fml-trading-agent',
      target: '_blank',
      type: 'vercel'
    }
  },
  artifacts_browser: {
    id: 'artifacts_browser',
    title: 'Artifacts Browser',
    description: 'File browser for checkpoints, logs, charts, and run metadata.',
    kind: 'text'
  },
  logs_panel: {
    id: 'logs_panel',
    title: 'Logs Panel',
    description: 'Streaming operational logs with filter presets.',
    kind: 'timeline'
  },
  run_status_indicator: {
    id: 'run_status_indicator',
    title: 'Run Status Indicator',
    description: 'Live status of orchestrations, jobs, and active monitors.',
    kind: 'stat'
  },
  prompt_input_box: {
    id: 'prompt_input_box',
    title: 'Prompt Input',
    description: 'Interface to provide Phoenix Agent with context or instructions.',
    kind: 'control'
  },
  response_output_box: {
    id: 'response_output_box',
    title: 'Agent Response',
    description: 'Streaming agent responses with highlighting for actions and decisions.',
    kind: 'text'
  },
  learning_log_viewer: {
    id: 'learning_log_viewer',
    title: 'Learning Log',
    description: 'Chronological view of insights the agent has learned or bookmarked.',
    kind: 'timeline'
  },
  drift_graphs: {
    id: 'drift_graphs',
    title: 'Model Drift Graphs',
    description: 'Feature and prediction drift monitors with alert overlays.',
    kind: 'chart'
  },
  shap_dynamics_chart: {
    id: 'shap_dynamics_chart',
    title: 'SHAP Dynamics',
    description: 'Temporal dynamics of SHAP value distributions by feature family.',
    kind: 'chart'
  },
  agent_timeline: {
    id: 'agent_timeline',
    title: 'Agent Timeline',
    description: 'Timeline of agent prompts, actions, and escalations.',
    kind: 'timeline'
  }
};

export const dashboardSpec: DashboardSpec = {
  heroTitle: 'Phoenix ML Trading Command Center',
  heroSubtitle: 'Unified observability for live trading, experimentation, and agent collaboration.',
  sections: [
    {
      id: 'overview',
      title: '📈 Overview',
      description: 'High-level health metrics that show portfolio performance and open alerts.',
      components: ['equity_curve', 'daily_pnl', 'sharpe_metrics', 'exposure_map', 'alerts_summary']
    },
    {
      id: 'model_analysis',
      title: '🧠 Model Insights',
      description: 'Production model diagnostics, feature drift, and challenger comparisons.',
      components: ['hit_rate', 'shap_top_features', 'feature_drift_chart', 'target_distribution', 'challenger_vs_champion']
    },
    {
      id: 'backtest_review',
      title: '🧪 Backtest / Live Run Analysis',
      description: 'Investigate trade-level behavior across both historical and live runs.',
      components: ['trade_list_table', 'price_chart_with_signals', 'holding_period_dist', 'performance_metrics_table', 'monte_carlo_scenarios']
    },
    {
      id: 'risk_monitor',
      title: '⚠️ Risk Monitor',
      description: 'Risk controls, leverage, and stop trigger audit trail.',
      components: ['live_drawdown', 'leverage_gauge', 'exposure_by_asset', 'risk_alerts_log', 'stop_trigger_events']
    },
    {
      id: 'data_validation',
      title: '📊 Data & Label QA',
      description: 'Data quality checks to ensure reliable model inputs and labels.',
      components: ['anomaly_timeline', 'missing_data_table', 'triple_barrier_distribution', 'feature_coverage_map']
    },
    {
      id: 'config_ops',
      title: '⚙️ Config & Ops',
      description: 'Configuration management, run logs, and operational tooling.',
      components: [
        'current_config_viewer',
        'config_selector_launcher',
        'vercel_deploy',
        'artifacts_browser',
        'logs_panel',
        'run_status_indicator'
      ]
    },
    {
      id: 'agent_interface',
      title: '🤖 Phoenix Agent',
      description: 'Collaborate with the Phoenix agent and monitor its learning loop.',
      components: ['prompt_input_box', 'response_output_box', 'learning_log_viewer', 'drift_graphs', 'shap_dynamics_chart', 'agent_timeline']
    }
  ]
};

export const getComponentDetails = (componentId: string): DashboardComponent => {
  const component = componentCatalog[componentId];

  if (!component) {
    throw new Error(`Component ${componentId} is not defined in the catalog`);
  }

  return component;
};
