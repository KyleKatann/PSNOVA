const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const DOCS = path.join(ROOT, 'docs');

function publicRoutes() {
  const routes = [];

  function walk(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const fullPath = path.join(directory, entry.name);

      if (entry.isDirectory()) {
        if (entry.name !== '分類中') {
          walk(fullPath);
        }
        continue;
      }

      if (!entry.name.endsWith('.html')) {
        continue;
      }

      const relative = path
        .relative(DOCS, fullPath)
        .replaceAll('\\', '/');

      routes.push(
        relative === 'index.html'
          ? '/PSNOVA/'
          : '/PSNOVA/' + relative
      );
    }
  }

  walk(DOCS);
  return routes.sort();
}

test.describe.configure({ mode: 'parallel' });

test.describe('axe WCAG A/AA excluding color contrast', () => {
  for (const route of publicRoutes()) {
    test(route, async ({ page }, testInfo) => {
      await page.goto(route, { waitUntil: 'load' });

      const results = await new AxeBuilder({ page })
        .disableRules(['color-contrast'])
        .withTags([
          'wcag2a',
          'wcg2aa',
          'wcag21a',
          'wcag21aa',
          'wcag22aa',
        ])
        .analyze();

      if (results.violations.length > 0) {
        await testInfo.attach('axe-results', {
          body: JSON.stringify(results, null, 2),
          contentType: 'application/json',
        });
      }

      const summary = results.violations
        .map((violation) => {
          const targets = violation.nodes
            .slice(0, 5)
            .map((node) => `    - ${node.target.join(' > ')}`)
            .join('\n');

          return [
            `${violation.id} [${violation.impact}]`,
            `  ${violation.help}`,
            targets,
          ].join('\n');
        })
        .join('\n\n');

      expect(
        results.violations,
        summary || `No axe violations on ${route}`
      ).toEqual([]);
    });
  }
});
