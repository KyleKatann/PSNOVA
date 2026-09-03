const fs = require('fs');
const path = require('path');
const { test, expect } = require('@playwright/test');

const ROOT = path.resolve(__dirname, '../..');
const DOCS = path.join(ROOT, 'docs');
const LOCAL_ORIGIN = 'http://127.0.0.1:4173';
const CRITICAL_RESOURCE_TYPES = new Set(['document', 'stylesheet', 'script', 'image']);

function publicRoutes() {
  const sitemap = fs.readFileSync(path.join(DOCS, 'sitemap.xml'), 'utf8');
  const routes = [...sitemap.matchAll(/<loc>https:\/\/kylekatann\.github\.io\/PSNOVA\/([^<]*)<\/loc>/g)]
    .map((match) => `/PSNOVA/${match[1] || 'index.html'}`);

  const weaponDir = path.join(DOCS, 'pages', 'weapon');
  for (const filename of fs.readdirSync(weaponDir)) {
    if (filename.endsWith('.html')) {
      routes.push(`/PSNOVA/pages/weapon/${filename}`);
    }
  }

  return [...new Set(routes)].sort();
}

async function routePublishedAssetsToLocalServer(page) {
  await page.route('https://kylekatann.github.io/PSNOVA/**', async (route) => {
    const published = new URL(route.request().url());
    const localUrl = `${LOCAL_ORIGIN}${published.pathname}${published.search}`;
    const response = await route.fetch({ url: localUrl });
    await route.fulfill({ response });
  });
}

async function forceImagesToLoad(page) {
  await page.evaluate(async () => {
    const images = Array.from(document.images);
    for (const image of images) {
      image.loading = 'eager';
    }

    await Promise.all(images.map((image) => {
      if (image.complete) return Promise.resolve();
      return new Promise((resolve) => {
        image.addEventListener('load', resolve, { once: true });
        image.addEventListener('error', resolve, { once: true });
      });
    }));
  });
}

for (const routePath of publicRoutes()) {
  test(`UI health: ${routePath}`, async ({ page }, testInfo) => {
    const browserErrors = [];
    const failedResources = [];

    await routePublishedAssetsToLocalServer(page);

    page.on('pageerror', (error) => {
      browserErrors.push(`pageerror: ${error.message}`);
    });

    page.on('console', (message) => {
      const text = message.text();
      if (message.type() === 'error' && !text.startsWith('Failed to load resource:')) {
        browserErrors.push(`console: ${text}`);
      }
    });

    page.on('requestfailed', (request) => {
      const url = new URL(request.url());
      if (
        url.pathname.startsWith('/PSNOVA/') &&
        CRITICAL_RESOURCE_TYPES.has(request.resourceType())
      ) {
        failedResources.push(`${request.resourceType()}: ${url.pathname}`);
      }
    });

    page.on('response', (response) => {
      const request = response.request();
      const url = new URL(response.url());
      if (
        url.pathname.startsWith('/PSNOVA/') &&
        CRITICAL_RESOURCE_TYPES.has(request.resourceType()) &&
        response.status() >= 400
      ) {
        failedResources.push(`${response.status()} ${request.resourceType()}: ${url.pathname}`);
      }
    });

    const response = await page.goto(routePath, { waitUntil: 'load' });
    expect(response, 'navigation should return a response').not.toBeNull();
    expect(response.ok(), `navigation failed: ${routePath}`).toBeTruthy();

    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('#main')).toBeVisible();
    await expect(page.locator('#main h2').first()).toBeVisible();

    const viewport = page.viewportSize();
    const mainRect = await page.locator('#main').boundingBox();
    expect(viewport).not.toBeNull();
    expect(mainRect, '#main should have a rendered box').not.toBeNull();
    expect(mainRect.width).toBeGreaterThan(100);
    expect(mainRect.x).toBeGreaterThanOrEqual(-1);
    expect(mainRect.x + mainRect.width).toBeLessThanOrEqual(viewport.width + 1);

    await forceImagesToLoad(page);

    const brokenImages = await page.locator('img[src]').evaluateAll((images) =>
      images
        .filter((image) => image.complete && image.naturalWidth === 0)
        .map((image) => image.getAttribute('src'))
    );
    expect(brokenImages, 'broken images detected').toEqual([]);

    const pageOverflow = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    expect(
      pageOverflow.scrollWidth,
      `page-level horizontal overflow: ${JSON.stringify(pageOverflow)}`
    ).toBeLessThanOrEqual(pageOverflow.clientWidth + 1);

    const cssPaths = await page.evaluate(() =>
      Array.from(document.styleSheets)
        .map((sheet) => sheet.href)
        .filter(Boolean)
        .map((href) => new URL(href).pathname)
        .filter((pathname) => pathname.startsWith('/PSNOVA/css/'))
    );
    expect(cssPaths).toContain('/PSNOVA/css/style.css');
    expect(new Set(cssPaths).size, `unexpected stylesheets: ${cssPaths.join(', ')}`).toBeLessThanOrEqual(2);
    for (const cssPath of cssPaths) {
      expect(['/PSNOVA/css/style.css', '/PSNOVA/css/page.css']).toContain(cssPath);
    }

    const needsPageCss =
      routePath === '/PSNOVA/index.html' ||
      routePath === '/PSNOVA/pages/gigantes.html' ||
      /\/pages\/weapon(?:\.html|\/)/.test(routePath);
    if (needsPageCss) {
      expect(cssPaths).toContain('/PSNOVA/css/page.css');
    }

    if (testInfo.project.name !== 'mobile-chromium') {
      const overlaps = await page.evaluate(() => {
        const main = document.querySelector('#main')?.getBoundingClientRect();
        const sub = document.querySelector('#sub')?.getBoundingClientRect();
        if (!main || !sub || window.innerWidth <= 800) return false;
        const horizontal = Math.min(main.right, sub.right) - Math.max(main.left, sub.left);
        const vertical = Math.min(main.bottom, sub.bottom) - Math.max(main.top, sub.top);
        return horizontal > 1 && vertical > 1;
      });
      expect(overlaps, '#main and #sub should not overlap on desktop').toBe(false);
    }

    if (testInfo.project.name === 'mobile-chromium') {
      const menuButton = page.locator('#menubar_hdr');
      const sidebar = page.locator('#sub');

      await expect(menuButton).toBeVisible();
      await expect(menuButton).toHaveAttribute('aria-expanded', 'false');
      await menuButton.click();
      await expect(menuButton).toHaveAttribute('aria-expanded', 'true');
      await expect(sidebar).toHaveClass(/is-open/);
      await page.keyboard.press('Escape');
      await expect(menuButton).toHaveAttribute('aria-expanded', 'false');
      await expect(sidebar).not.toHaveClass(/is-open/);
    }

    if (/\/pages\/weapon\/[^/]+\.html$/.test(routePath)) {
      const header = page.locator('.weapon-data-table thead th').first();
      const firstRow = page.locator('.weapon-data-table tbody tr:not([hidden])').first();
      const headerBox = await header.boundingBox();
      const rowBox = await firstRow.boundingBox();
      const headerPosition = await header.evaluate((cell) => getComputedStyle(cell).position);

      expect(headerBox, 'weapon header should render').not.toBeNull();
      expect(rowBox, 'first weapon row should render').not.toBeNull();
      expect(headerPosition, 'weapon header must stay in normal flow').not.toBe('sticky');
      expect(
        headerBox.y + headerBox.height,
        'weapon header must remain above the first data row'
      ).toBeLessThanOrEqual(rowBox.y + 1);
    }

    if (testInfo.project.name === 'desktop-site-touch') {
      const pointerMode = await page.evaluate(() => ({
        coarse: window.matchMedia('(pointer: coarse)').matches,
        fine: window.matchMedia('(pointer: fine)').matches,
      }));
      expect(pointerMode.coarse, 'desktop-site touch project must emulate a coarse pointer').toBe(true);
      expect(pointerMode.fine, 'desktop-site touch project must not emulate a fine primary pointer').toBe(false);

      if (routePath === '/PSNOVA/pages/gigantes.html') {
        const gigantesTables = page.locator('.gigantes-table');
        const tableScrolls = page.locator('.gigantes-table-scroll');

        await expect(gigantesTables).toHaveCount(2);
        await expect(tableScrolls).toHaveCount(2);

        const tableScrollMetrics = await tableScrolls.evaluateAll((wrappers) =>
          wrappers.map((wrapper) => ({
            tableCount: wrapper.querySelectorAll(':scope > .gigantes-table').length,
            tabIndex: wrapper.tabIndex,
            role: wrapper.getAttribute('role'),
            ariaLabel: wrapper.getAttribute('aria-label'),
            overflowX: getComputedStyle(wrapper).overflowX,
            clientWidth: wrapper.clientWidth,
            scrollWidth: wrapper.scrollWidth,
          }))
        );

        for (const tableScroll of tableScrollMetrics) {
          expect(tableScroll.tableCount).toBe(1);
          expect(tableScroll.tabIndex).toBe(0);
          expect(tableScroll.role).toBe('region');
          expect(tableScroll.ariaLabel).toBeTruthy();
          expect(tableScroll.overflowX).toBe('auto');
          expect(tableScroll.scrollWidth).toBeGreaterThan(tableScroll.clientWidth);
        }
      }
    }

    expect(failedResources, 'critical local resources failed').toEqual([]);
    expect(browserErrors, 'browser errors detected').toEqual([]);
  });
}
