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
        
        # -> Open the Login page by navigating to the site's Login (/accounts/login/) so the provided credentials can be entered.
        await page.goto("http://localhost:8000/accounts/login/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'İstifadəçi adı və ya E-poçt' field with admin, fill the 'Şifrə' field with password, then click the 'Daxil Ol' button.
        # İstifadəçi adınızı daxil edin text field
        elem = page.locator('[id="id_username"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin")
        
        # -> Fill the 'İstifadəçi adı və ya E-poçt' field with admin, fill the 'Şifrə' field with password, then click the 'Daxil Ol' button.
        # Şifrənizi daxil edin password field
        elem = page.locator('[id="id_password"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("password")
        
        # -> Fill the 'İstifadəçi adı və ya E-poçt' field with admin, fill the 'Şifrə' field with password, then click the 'Daxil Ol' button.
        # Daxil Ol button
        elem = page.get_by_role('button', name='Daxil Ol', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the dashboard statistics are displayed
        # Assert: Pending Evaluations count is displayed as "0".
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[3]/div[2]/div[2]/div[1]/p[1]").nth(0)).to_have_text("0", timeout=15000), "Pending Evaluations count is displayed as \"0\"."
        # Assert: Upcoming Trainings count is displayed as "0".
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[3]/div[2]/div[2]/div[2]/p[1]").nth(0)).to_have_text("0", timeout=15000), "Upcoming Trainings count is displayed as \"0\"."
        # Assert: Skills Pending Approval count is displayed as "0".
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[3]/div[2]/div[2]/div[3]/p[1]").nth(0)).to_have_text("0", timeout=15000), "Skills Pending Approval count is displayed as \"0\"."
        
        # --> Verify the authenticated workspace is displayed
        await page.locator("xpath=/html/body/div[2]/div/aside/div/div[2]/div/a").nth(0).scroll_into_view_if_needed()
        # Assert: Profile link is visible, indicating the user is authenticated.
        await expect(page.locator("xpath=/html/body/div[2]/div/aside/div/div[2]/div/a").nth(0)).to_be_visible(timeout=15000), "Profile link is visible, indicating the user is authenticated."
        await page.locator("xpath=/html/body/div[2]/div/aside/div/div[2]/div/form/button").nth(0).scroll_into_view_if_needed()
        # Assert: Logout button is visible, confirming an authenticated session.
        await expect(page.locator("xpath=/html/body/div[2]/div/aside/div/div[2]/div/form/button").nth(0)).to_be_visible(timeout=15000), "Logout button is visible, confirming an authenticated session."
        await page.locator("xpath=/html/body/div[2]/nav/div[1]/div/div[3]/div[3]/button").nth(0).scroll_into_view_if_needed()
        # Assert: User menu showing the account (including 'Sistem Administrator') is visible in the top navigation.
        await expect(page.locator("xpath=/html/body/div[2]/nav/div[1]/div/div[3]/div[3]/button").nth(0)).to_be_visible(timeout=15000), "User menu showing the account (including 'Sistem Administrator') is visible in the top navigation."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    