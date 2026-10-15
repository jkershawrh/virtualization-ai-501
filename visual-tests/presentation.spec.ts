import { expect, test } from '@playwright/test'

test('opening and architecture remain visually stable', async ({ page }) => {
  test.skip(Boolean(process.env.CI), 'macOS pixel baselines are verified locally; CI runs platform-neutral browser checks')
  await page.goto('/')
  await expect(page).toHaveScreenshot('opening.png', { fullPage: true })
  await page.goto('/?act=1&scene=0')
  await expect(page).toHaveScreenshot('architecture.png', { fullPage: true })
})

test('live journey opens as a workload workspace with topology on demand', async ({ page }) => {
  test.skip(Boolean(process.env.CI), 'macOS pixel baselines are verified locally; CI runs platform-neutral browser checks')
  await page.goto('/?act=3&scene=0')
  await expect(page).toHaveScreenshot('live-journey.png', { fullPage: true })
})

test('core controls are keyboard reachable', async ({ page }) => {
  await page.goto('/?act=0&scene=0')
  await page.keyboard.press('Tab')
  await expect(page.getByRole('button', { name: 'Restart presentation' })).toBeFocused()
})

test('all seven stage scenes require no vertical scroll at both desktop sizes', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name === 'rehearsal-mobile')
  for (const url of ['/?act=0&scene=0', '/?act=1&scene=0', '/?act=2&scene=0', '/?act=3&scene=0', '/?act=4&scene=0', '/?act=5&scene=0', '/?act=6&scene=0']) {
    await page.goto(url)
    const sizes = await page.evaluate(() => {
      const stage = document.querySelector('.stage') as HTMLElement
      return { client: stage.clientHeight, content: stage.scrollHeight, bodyOverflow: getComputedStyle(document.body).overflowY }
    })
    expect(sizes.bodyOverflow, `${url} allowed document scrolling`).toBe('hidden')
    expect(sizes.content, `${url} clipped content inside the stage`).toBeLessThanOrEqual(sizes.client + 1)
  }
})

test('internal architecture and live-condition reveals fit at both desktop sizes', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name === 'rehearsal-mobile')
  const assertFit = async (label: string) => {
    const sizes = await page.evaluate(() => {
      const stage = document.querySelector('.stage') as HTMLElement
      return { client: stage.clientHeight, content: stage.scrollHeight }
    })
    expect(sizes.content, `${label} clipped inside the stage`).toBeLessThanOrEqual(sizes.client + 1)
  }

  await page.goto('/?act=1&scene=0')
  for (let index = 0; index < 4; index += 1) {
    const question = await page.locator('.architecture-question h2').innerText()
    await page.getByRole('button', { name: 'Reveal technical boundary', exact: true }).click()
    await expect(page.locator('.architecture-answer')).toBeVisible()
    await assertFit(`architecture answer ${index}`)
    await page.getByRole('button', {
      name: index === 3 ? 'Complete architecture' : 'Ask next question →', exact: true,
    }).click()
    // AnimatePresence retains the outgoing question during its exit. Do not
    // accidentally click that stale control a second time and skip a layer.
    if (index < 3) {
      await expect(page.locator('.architecture-question h2')).not.toHaveText(question)
      await expect(page.getByRole('button', { name: 'Reveal technical boundary', exact: true })).toBeVisible()
    }
  }
  await expect(page.getByRole('button', { name: 'Replay architecture' })).toBeVisible()
  await assertFit('architecture complete')

  await page.goto('/?act=3&scene=0')
  await page.getByRole('button', { name: /run qualification conditions/i }).click()
  await expect(page.locator('.source-badge', { hasText: 'rehearsal' })).toBeVisible()
  await assertFit('qualification condition 1')
  for (let index = 2; index <= 3; index += 1) {
    await page.getByRole('button', { name: /next qualification condition/i }).click()
    await expect(page.getByText(`CONDITION ${index} OF 3`)).toBeVisible()
    await assertFit(`qualification condition ${index}`)
  }
})

test('keyboard journey reaches an explicit close', async ({ page }) => {
  await page.goto('/?act=6&scene=0')
  await expect(page.getByText('A candidate is immutable before it becomes certifiable')).toBeVisible()
  await page.keyboard.press('ArrowRight')
  await expect(page.getByRole('button', { name: 'Close presentation' })).toBeVisible()
})
