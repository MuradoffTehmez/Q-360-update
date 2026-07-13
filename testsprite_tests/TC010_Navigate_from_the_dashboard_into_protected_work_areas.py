import asyncio
import re
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None

    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()

        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",
                "--disable-dev-shm-usage",
                "--ipc=host",
                "--single-process"
            ],
        )

        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        # Wider default timeout to match the agent's DOM-stability budget;
        # auto-waiting Playwright APIs (expect, locator.wait_for) inherit this.
        context.set_default_timeout(15000)

        # Open a new page in the browser context
        page = await context.new_page()

        # Interact with the page elements to simulate user flow
        # -> navigate
        await page.goto("http://localhost:8000")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Open the 'Login' page.
        await page.goto("http://localhost:8000/accounts/login/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill 'admin' into the username field and 'password' into the password field on the login form.
        # İstifadəçi adınızı daxil edin text field
        elem = page.locator('[id="id_username"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin")
        
        # -> Fill 'admin' into the username field and 'password' into the password field on the login form.
        # Şifrənizi daxil edin password field
        elem = page.locator('[id="id_password"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("password")
        
        # -> Click the 'Daxil Ol' button to submit the login form.
        # Daxil Ol button
        elem = page.get_by_role('button', name='Daxil Ol', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'HR İdarəetməsi' sidebar entry to expand HR-related options so the Recruitment workspace link can be selected.
        # HR İdarəetməsi button
        elem = page.get_by_role('button', name='HR İdarəetməsi', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'İşə Qəbul Paneli' (Recruitment) link in the expanded 'HR İdarəetməsi' sidebar and verify the Recruitment workspace is displayed.
        # İşə Qəbul Paneli link
        elem = page.get_by_role('link', name='İşə Qəbul Paneli', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Qiymətləndirmə və Rəylər' (Evaluations) entry in the left sidebar to open the Evaluations workspace.
        # Qiymətləndirmə və Rəylər button
        elem = page.get_by_role('button', name='Qiymətləndirmə və Rəylər', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Qiymətləndirmə və Rəylər' (Evaluations) entry in the left sidebar to open the Evaluations workspace and verify the workspace is displayed.
        # Qiymətləndirmə və Rəylər button
        elem = page.get_by_role('button', name='Qiymətləndirmə və Rəylər', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Evaluations' link in the top navigation to open the Evaluations workspace.
        # Evaluations link
        elem = page.get_by_text('Platforma', exact=True).locator("xpath=ancestor-or-self::*[.//a][1]").get_by_role('link', name='Evaluations', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        # Assert: Recruitment link 'İşə Qəbul Paneli' is visible in the HR sidebar
        elem = page.locator('xpath=/html/body/div[2]/div/aside/div/nav/div[5]/div/a[15]').nth(0)
        await elem.scroll_into_view_if_needed()
        assert await elem.is_visible(), "Expected element to be visible after scrolling into view"
        # Assert: URL navigates to /evaluations/my-assignments/ after opening Evaluations
        current_url = await page.evaluate("() => window.location.href")
        assert "/evaluations/my-assignments/" in current_url, "The page should be at /evaluations/my-assignments/"
        # Assert: Page heading "Mənim Qiymətləndirmələrim" is visible on the Evaluations workspace
        elem = page.locator("text=Mənim Qiymətləndirmələrim").nth(0)
        await elem.scroll_into_view_if_needed()
        assert await elem.is_visible(), "Expected element to be visible after scrolling into view"
        # Assert: Evaluations table shows the message "Sizə təyin edilmiş qiymətləndirmə tapşırığı yoxdur"
        text = await page.locator('xpath=/html/body/div[2]/div/main/div/div[2]/div[3]/div[2]/table/tbody/tr').nth(0).text_content()
        assert 'Sizə təyin edilmiş qiymətləndirmə tapşırığı yoxdur' in text
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    