import assert from 'assert';
import { dashboardSpec, componentCatalog } from '../src/dashboardSpec.js';

function ensureHeroCopy() {
  assert.ok(dashboardSpec.heroTitle.trim().length > 0, 'hero title must be provided');
  assert.ok(dashboardSpec.heroSubtitle.trim().length > 0, 'hero subtitle must be provided');
}

function ensureAllComponentsAreUsed() {
  const catalogIds = new Set(Object.keys(componentCatalog));
  assert.ok(catalogIds.size > 0, 'component catalog cannot be empty');

  for (const section of dashboardSpec.sections) {
    for (const componentId of section.components) {
      if (!catalogIds.has(componentId)) {
        throw new Error(`Section ${section.id} references unknown component ${componentId}`);
      }
      catalogIds.delete(componentId);
    }
  }

  if (catalogIds.size > 0) {
    throw new Error(`Component catalog has unused entries: ${Array.from(catalogIds).join(', ')}`);
  }
}

function ensureSectionMetadata() {
  for (const section of dashboardSpec.sections) {
    if (!section.title || !section.title.trim()) {
      throw new Error(`Section ${section.id} must include a title`);
    }
    if (!section.description || !section.description.trim()) {
      throw new Error(`Section ${section.id} must include a description`);
    }
  }
}

try {
  ensureHeroCopy();
  ensureAllComponentsAreUsed();
  ensureSectionMetadata();
  console.log('Lint checks passed.');
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
}
