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
        
        # -> Open the 'Login' page (navigate to /accounts/login/) so the login form can be observed.
        await page.goto("http://localhost:8000/accounts/login/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill 'admin' into the username field, fill 'password' into the password field, then click the 'Daxil Ol' (Login) button.
        # İstifadəçi adınızı daxil edin text field
        elem = page.locator('[id="id_username"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin")
        
        # -> Fill 'admin' into the username field, fill 'password' into the password field, then click the 'Daxil Ol' (Login) button.
        # Şifrənizi daxil edin password field
        elem = page.locator('[id="id_password"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("password")
        
        # -> Fill 'admin' into the username field, fill 'password' into the password field, then click the 'Daxil Ol' (Login) button.
        # Daxil Ol button
        elem = page.get_by_role('button', name='Daxil Ol', exact=True)
        await elem.click(timeout=10000)
        
        # -> Open the 'Create Campaign' page (the campaign creation form) so the campaign fields can be inspected.
        await page.goto("http://localhost:8000/evaluations/campaigns/create/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'Kampaniya Adı' field with a unique campaign name, set valid start and end dates, then click the 'Layihə kimi saxla' (Save as draft) button to create the campaign.
        # title text field
        elem = page.locator('[id="id_title"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("Automated Test Campaign 2026-07-06")
        
        # -> Fill the 'Kampaniya Adı' field with a unique campaign name, set valid start and end dates, then click the 'Layihə kimi saxla' (Save as draft) button to create the campaign.
        # start_date date field
        elem = page.locator('[id="id_start_date"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("2026-07-07")
        
        # -> Fill the 'Kampaniya Adı' field with a unique campaign name, set valid start and end dates, then click the 'Layihə kimi saxla' (Save as draft) button to create the campaign.
        # end_date date field
        elem = page.locator('[id="id_end_date"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("2026-07-14")
        
        # -> Fill the 'Kampaniya Adı' field with a unique campaign name, set valid start and end dates, then click the 'Layihə kimi saxla' (Save as draft) button to create the campaign.
        # Layihə kimi saxla button
        elem = page.get_by_role('button', name='Layihə kimi saxla', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the new campaign appears in the workspace
        # Assert: Verified the campaign "Automated Test Campaign 2026-07-06" is listed in the workspace.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[3]/div[3]/div/div/table/tbody/tr[1]/td[1]").nth(0)).to_have_text("Automated Test Campaign 2026-07-06", timeout=15000), "Verified the campaign \"Automated Test Campaign 2026-07-06\" is listed in the workspace."
        current_url = await page.evaluate("() => window.location.href")
        # Assert: page loaded with a URL (final outcome verified by the AI judge during the run)
        assert current_url, 'Page should have loaded with a URL'
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    