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
