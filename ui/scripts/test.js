import assert from 'assert';
import { dashboardSpec, getComponentDetails } from '../src/dashboardSpec.js';
import { buildDashboardMarkup } from '../src/app.js';

const tests = [
  {
    name: 'every section exposes at least one component',
    run: () => {
      assert.ok(dashboardSpec.sections.length > 0, 'dashboard must include sections');
      for (const section of dashboardSpec.sections) {
        assert.ok(section.components.length > 0, `${section.id} must include components`);
      }
    }
  },
  {
    name: 'component catalog resolves all referenced component ids',
    run: () => {
      const seen = new Set();
      for (const section of dashboardSpec.sections) {
        for (const componentId of section.components) {
          const component = getComponentDetails(componentId);
          assert.ok(component, `${componentId} should resolve to a component`);
          seen.add(componentId);
        }
      }
      assert.ok(seen.size > 0, 'at least one component must be referenced');
    }
  },
  {
    name: 'section identifiers are unique',
    run: () => {
      const ids = dashboardSpec.sections.map((section) => section.id);
      const unique = new Set(ids);
      assert.strictEqual(unique.size, ids.length, 'section ids must be unique');
    }
  },
  {
    name: 'rendered markup contains navigation and hero copy',
    run: () => {
      const markup = buildDashboardMarkup();
      assert.ok(markup.includes('Phoenix ML Trading Command Center'), 'hero title should be present');
      for (const section of dashboardSpec.sections) {
        assert.ok(markup.includes(`href="#${section.id}"`), `nav link for ${section.id} missing`);
      }
    }
  }
];

let failures = 0;
for (const test of tests) {
  try {
    test.run();
    console.log(`✔ ${test.name}`);
  } catch (error) {
    failures += 1;
    console.error(`✘ ${test.name}`);
    console.error(error instanceof Error ? error.message : error);
  }
}

if (failures > 0) {
  process.exitCode = 1;
  console.error(`\n${failures} test(s) failed.`);
} else {
  console.log(`\nAll ${tests.length} tests passed.`);
}
