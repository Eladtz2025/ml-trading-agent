import specData from './dashboardSpecData.json';

export type ComponentKind =
  | 'chart'
  | 'stat'
  | 'table'
  | 'timeline'
  | 'control'
  | 'distribution'
  | 'text'
  | 'gauge';

export type ComponentActionType = 'link' | 'vercel' | 'action';

export interface ComponentCTA {
  label: string;
  href?: string;
  target?: '_blank' | '_self';
  type?: ComponentActionType;
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

interface DashboardSpecData extends DashboardSpec {
  componentCatalog: Record<string, DashboardComponent>;
}

const data = specData as DashboardSpecData;

export const componentCatalog: Record<string, DashboardComponent> = data.componentCatalog;

export const dashboardSpec: DashboardSpec = {
  heroTitle: data.heroTitle,
  heroSubtitle: data.heroSubtitle,
  sections: data.sections,
};

export const getComponentDetails = (componentId: string): DashboardComponent => {
  const component = componentCatalog[componentId];

  if (!component) {
    throw new Error(`Component ${componentId} is not defined in the catalog`);
  }

  return component;
};
