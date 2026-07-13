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
        
        # -> Open the 'Login' page by navigating to /accounts/login/ (the explicit login path).
        await page.goto("http://localhost:8000/accounts/login/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill 'admin' into the İstifadəçi adı və ya E-poçt field, fill 'password' into the Şifrə field, then click the 'Daxil Ol' button to submit the login form.
        # İstifadəçi adınızı daxil edin text field
        elem = page.locator('[id="id_username"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin")
        
        # -> Fill 'admin' into the İstifadəçi adı və ya E-poçt field, fill 'password' into the Şifrə field, then click the 'Daxil Ol' button to submit the login form.
        # Şifrənizi daxil edin password field
        elem = page.locator('[id="id_password"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("password")
        
        # -> Fill 'admin' into the İstifadəçi adı və ya E-poçt field, fill 'password' into the Şifrə field, then click the 'Daxil Ol' button to submit the login form.
        # Daxil Ol button
        elem = page.get_by_role('button', name='Daxil Ol', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the dashboard is displayed
        # Assert: The browser URL contains /dashboard/, confirming the dashboard page is loaded.
        await expect(page).to_have_url(re.compile("/dashboard/"), timeout=15000), "The browser URL contains /dashboard/, confirming the dashboard page is loaded."
        await page.locator("xpath=/html/body/div[2]/div/aside/div/nav/div[1]/button").nth(0).scroll_into_view_if_needed()
        # Assert: The dashboard sidebar item 'Panel və Analitika' is visible.
        await expect(page.locator("xpath=/html/body/div[2]/div/aside/div/nav/div[1]/button").nth(0)).to_be_visible(timeout=15000), "The dashboard sidebar item 'Panel v\u0259 Analitika' is visible."
        await page.locator("xpath=/html/body/div[2]/div/aside/div/div[2]/div/form/button").nth(0).scroll_into_view_if_needed()
        # Assert: The 'Logout' button is visible, indicating an authenticated dashboard session.
        await expect(page.locator("xpath=/html/body/div[2]/div/aside/div/div[2]/div/form/button").nth(0)).to_be_visible(timeout=15000), "The 'Logout' button is visible, indicating an authenticated dashboard session."
        
        # --> Verify protected workspace navigation is available
        # Assert: The left sidebar shows the "Panel və Analitika" navigation item.
        await expect(page.locator("xpath=/html/body/div[2]/div/aside/div/nav/div[1]/button").nth(0)).to_have_text("Panel v\u0259 Analitika", timeout=15000), "The left sidebar shows the \"Panel v\u0259 Analitika\" navigation item."
        # Assert: The left sidebar shows the "Qiymətləndirmə və Rəylər" navigation item.
        await expect(page.locator("xpath=/html/body/div[2]/div/aside/div/nav/div[2]/button").nth(0)).to_have_text("Qiym\u0259tl\u0259ndirm\u0259 v\u0259 R\u0259yl\u0259r", timeout=15000), "The left sidebar shows the \"Qiym\u0259tl\u0259ndirm\u0259 v\u0259 R\u0259yl\u0259r\" navigation item."
        # Assert: The left sidebar shows the "Kompetensiya və Təlim" navigation item.
        await expect(page.locator("xpath=/html/body/div[2]/div/aside/div/nav/div[3]/button").nth(0)).to_have_text("Kompetensiya v\u0259 T\u0259lim", timeout=15000), "The left sidebar shows the \"Kompetensiya v\u0259 T\u0259lim\" navigation item."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    