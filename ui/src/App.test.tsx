import { describe, it, expect } from 'vitest';
import { dashboardSpec, getComponentDetails } from './data/dashboardSpec';

describe('dashboard specification', () => {
  it('exposes all sections with at least one component', () => {
    expect(dashboardSpec.sections.length).toBeGreaterThan(0);
    dashboardSpec.sections.forEach((section) => {
      expect(section.components.length).toBeGreaterThan(0);
    });
  });

  it('maps every component id to a catalog entry', () => {
    const uniqueIds = new Set<string>();
    dashboardSpec.sections.forEach((section) => {
      section.components.forEach((componentId) => {
        expect(() => getComponentDetails(componentId)).not.toThrow();
        uniqueIds.add(componentId);
      });
    });
    expect(uniqueIds.size).toBeGreaterThan(0);
  });

  it('uses unique section identifiers', () => {
    const ids = dashboardSpec.sections.map((section) => section.id);
    const unique = new Set(ids);
    expect(unique.size).toBe(ids.length);
  });
});
