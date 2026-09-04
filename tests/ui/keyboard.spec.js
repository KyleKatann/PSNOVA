const { test, expect } = require('@playwright/test');

test('mobile navigation keeps a logical keyboard focus path', async ({ page }, testInfo) => {
  test.skip(
    testInfo.project.name !== 'mobile-chromium',
    'mobile keyboard navigation audit'
  );

  await page.goto('/PSNOVA/', { waitUntil: 'load' });

  const skipLink = page.locator('.skip-link');
  const logoLink = page.locator('header #logo a');
  const trigger = page.locator('#menubar_hdr');
  const firstMenuLink = page.locator('#sub a[href]').first();

  await expect(trigger).toBeVisible();
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');

  await page.keyboard.press('Tab');
  await expect(skipLink).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(logoLink).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(trigger).toBeFocused();

  await page.keyboard.press('Enter');
  await expect(trigger).toHaveAttribute('aria-expanded', 'true');
  await expect(firstMenuLink).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');
  await expect(trigger).toBeFocused();
});

test('mobile site search keeps input and submit button on one row', async ({ page }, testInfo) => {
  test.skip(
    testInfo.project.name !== 'mobile-chromium',
    'mobile search layout regression'
  );

  await page.goto('/PSNOVA/', { waitUntil: 'load' });

  const controls = page.locator('.site-search-controls');
  const input = page.locator('#site-data-search');
  const submit = page.getByRole('button', { name: '検索' });

  await expect(controls).toBeVisible();
  await expect(input).toBeVisible();
  await expect(submit).toBeVisible();

  const boxes = await Promise.all([
    controls.boundingBox(),
    input.boundingBox(),
    submit.boundingBox(),
  ]);
  const [controlsBox, inputBox, submitBox] = boxes;

  expect(controlsBox).not.toBeNull();
  expect(inputBox).not.toBeNull();
  expect(submitBox).not.toBeNull();
  expect(Math.abs(inputBox.y - submitBox.y)).toBeLessThanOrEqual(2);
  expect(submitBox.x).toBeGreaterThan(inputBox.x + inputBox.width - 1);
  expect(submitBox.x + submitBox.width).toBeLessThanOrEqual(
    controlsBox.x + controlsBox.width + 1
  );
});

test('site search button discovers page destinations dynamically', async ({ page }) => {
  await page.goto('/PSNOVA/', { waitUntil: 'load' });

  const input = page.locator('#site-data-search');
  const submit = page.getByRole('button', { name: '検索' });

  await input.fill('素材');
  await expect(page.locator('#site-search-results')).toBeVisible();

  await submit.click();
  await expect(page).toHaveURL(/\/PSNOVA\/pages\/material\.html$/);
});

test('site search arrows select a dynamic result and Enter activates it', async ({ page }) => {
  await page.goto('/PSNOVA/', { waitUntil: 'load' });

  const input = page.locator('#site-data-search');
  await input.fill('ソード');

  const options = page.locator('#site-search-results [role="option"]');
  await expect(options.first()).toBeVisible({ timeout: 15000 });
  await expect(options.first()).toHaveAttribute('tabindex', '-1');

  await input.press('ArrowDown');
  await expect(input).toHaveAttribute(
    'aria-activedescendant',
    'site-search-option-0'
  );
  await expect(options.nth(0)).toHaveAttribute('aria-selected', 'true');

  await input.press('Enter');
  await expect(page).toHaveURL(/\/PSNOVA\/pages\/weapon\/sword\.html$/);
});

test('site search highlights partial matches in results and destination row', async ({ page }) => {
  await page.goto('/PSNOVA/', { waitUntil: 'load' });

  const input = page.locator('#site-data-search');
  await input.fill('磁晶龍');

  const result = page
    .locator('#site-search-results [role="option"]')
    .filter({ hasText: '冷たく燃える金属結晶' })
    .first();

  await expect(result).toBeVisible({ timeout: 15000 });
  await expect(result).toContainText('素材');
  await expect(result.locator('mark.site-search-match').first()).toContainText('磁晶龍');
  await result.click();

  await expect(page).toHaveURL(/\/PSNOVA\/pages\/material\.html\?site-search=/);

  const targetRow = page.locator('[data-site-search-target="true"]');
  await expect(targetRow).toBeVisible();
  await expect(targetRow).toContainText('冷たく燃える金属結晶');
  await expect(targetRow).toContainText('目を覚ます磁晶龍H');
  await expect(targetRow.locator('[data-site-search-hit="true"]')).toContainText('目を覚ます磁晶龍H');
  await expect(targetRow.locator('mark.site-search-match').first()).toContainText('磁晶龍');
});
