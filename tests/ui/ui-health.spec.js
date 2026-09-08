const fs = require('fs');
const path = require('path');
const { test, expect } = require('@playwright/test');

const ROOT = path.resolve(__dirname, '../..');
const DOCS = path.join(ROOT, 'docs');
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

function localFileForPublishedUrl(url) {
  const published = new URL(url);
  const prefix = '/PSNOVA/';

  if (!published.pathname.startsWith(prefix)) return null;

  let relativePath = decodeURIComponent(published.pathname.slice(prefix.length));
  if (!relativePath) relativePath = 'index.html';

  const localPath = path.resolve(DOCS, relativePath);
  const relativeToDocs = path.relative(DOCS, localPath);

  if (
    relativeToDocs.startsWith('..') ||
    path.isAbsolute(relativeToDocs) ||
    !fs.existsSync(localPath) ||
    !fs.statSync(localPath).isFile()
  ) {
    return null;
  }

  return localPath;
}

async function routePublishedAssetsToLocalFiles(page) {
  await page.route('https://kylekatann.github.io/PSNOVA/**', async (route) => {
    const localPath = localFileForPublishedUrl(route.request().url());

    if (!localPath) {
      await route.fulfill({
        status: 404,
        contentType: 'text/plain',
        body: 'Not Found',
      });
      return;
    }

    await route.fulfill({ path: localPath });
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

    await routePublishedAssetsToLocalFiles(page);

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
    expect(response, 'navigationはresponseを返さなければならない').not.toBeNull();
    expect(response.ok(), `navigationに失敗: ${routePath}`).toBeTruthy();

    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('#main')).toBeVisible();
    await expect(page.locator('#main h2').first()).toBeVisible();

    const viewport = page.viewportSize();
    const mainRect = await page.locator('#main').boundingBox();
    expect(viewport).not.toBeNull();
    expect(mainRect, '#mainには描画領域が必要').not.toBeNull();
    expect(mainRect.width).toBeGreaterThan(100);
    expect(mainRect.x).toBeGreaterThanOrEqual(-1);
    expect(mainRect.x + mainRect.width).toBeLessThanOrEqual(viewport.width + 1);

    await forceImagesToLoad(page);

    const brokenImages = await page.locator('img[src]').evaluateAll((images) =>
      images
        .filter((image) => image.complete && image.naturalWidth === 0)
        .map((image) => image.getAttribute('src'))
    );
    expect(brokenImages, '壊れた画像を検出した').toEqual([]);

    const pageOverflow = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    expect(
      pageOverflow.scrollWidth,
      `ページ全体で横方向overflowを検出: ${JSON.stringify(pageOverflow)}`
    ).toBeLessThanOrEqual(pageOverflow.clientWidth + 1);

    const cssPaths = await page.evaluate(() =>
      Array.from(document.styleSheets)
        .map((sheet) => sheet.href)
        .filter(Boolean)
        .map((href) => new URL(href).pathname)
        .filter((pathname) => pathname.startsWith('/PSNOVA/css/'))
    );
    expect(cssPaths).toContain('/PSNOVA/css/style.css');
    expect(new Set(cssPaths).size, `想定外のstylesheet: ${cssPaths.join(', ')}`).toBeLessThanOrEqual(2);
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

    const tableRegionNames = await page.locator('#main .table-scroll[role="region"]').evaluateAll((regions) =>
      regions.map((region) => {
        const labelledBy = (region.getAttribute('aria-labelledby') || '').trim();
        if (labelledBy) {
          return labelledBy
            .split(/\s+/)
            .map((id) => document.getElementById(id)?.textContent?.trim() || '')
            .filter(Boolean)
            .join(' ')
            .trim();
        }
        return (region.getAttribute('aria-label') || '').trim();
      })
    );

    for (const regionName of tableRegionNames) {
      expect(regionName, 'テーブルのscroll regionにはaccessible nameが必要').not.toBe('');
    }

    if (tableRegionNames.length > 1) {
      expect(
        new Set(tableRegionNames).size,
        `テーブルregion名が重複している: ${tableRegionNames.join(' | ')}`
      ).toBe(tableRegionNames.length);
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
      expect(overlaps, 'desktopでは#mainと#subが重なってはならない').toBe(false);
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

      expect(headerBox, '武器headerは描画されなければならない').not.toBeNull();
      expect(rowBox, '武器の先頭行は描画されなければならない').not.toBeNull();
      expect(headerPosition, '武器headerは通常flowを維持しなければならない').not.toBe('sticky');
      expect(
        headerBox.y + headerBox.height,
        '武器headerは先頭data行より上に維持しなければならない'
      ).toBeLessThanOrEqual(rowBox.y + 1);
    }

    if (testInfo.project.name === 'desktop-site-touch') {
      const pointerMode = await page.evaluate(() => ({
        coarse: window.matchMedia('(pointer: coarse)').matches,
        fine: window.matchMedia('(pointer: fine)').matches,
      }));
      expect(pointerMode.coarse, 'desktop-site touch projectはcoarse pointerをemulateしなければならない').toBe(true);
      expect(pointerMode.fine, 'desktop-site touch projectはfine primary pointerをemulateしてはならない').toBe(false);

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
            overflowX: getComputedStyle(wrapper).overflowX,
            clientWidth: wrapper.clientWidth,
            scrollWidth: wrapper.scrollWidth,
          }))
        );

        for (const tableScroll of tableScrollMetrics) {
          expect(tableScroll.tableCount).toBe(1);
          expect(tableScroll.tabIndex).toBe(0);
          expect(tableScroll.role).toBe('region');
          expect(tableScroll.overflowX).toBe('auto');
          expect(tableScroll.scrollWidth).toBeGreaterThan(tableScroll.clientWidth);
        }
      }
    }

    expect(failedResources, '重要なlocal resourceの読み込みに失敗した').toEqual([]);
    expect(browserErrors, 'browser errorを検出した').toEqual([]);
  });
}
