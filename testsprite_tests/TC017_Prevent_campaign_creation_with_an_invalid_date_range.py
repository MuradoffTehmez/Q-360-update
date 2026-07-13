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
        
        # -> Open the 'Login' page (go to /accounts/login/).
        await page.goto("http://localhost:8000/accounts/login/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the username and password fields and click the 'Daxil Ol' button to submit the login form.
        # İstifadəçi adınızı daxil edin text field
        elem = page.locator('[id="id_username"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin")
        
        # -> Fill the username and password fields and click the 'Daxil Ol' button to submit the login form.
        # Şifrənizi daxil edin password field
        elem = page.locator('[id="id_password"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("password")
        
        # -> Fill the username and password fields and click the 'Daxil Ol' button to submit the login form.
        # Daxil Ol button
        elem = page.get_by_role('button', name='Daxil Ol', exact=True)
        await elem.click(timeout=10000)
        
        # -> Open the 'Qiymətləndirmə və Rəylər' (Evaluations) menu to reveal Campaigns and related actions.
        # Qiymətləndirmə və Rəylər button
        elem = page.get_by_role('button', name='Qiymətləndirmə və Rəylər', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Kampaniyalar' (Campaigns) link in the left navigation to open the Campaigns page.
        # Kampaniyalar link
        elem = page.get_by_role('link', name='Kampaniyalar', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the '+ Yeni Kampaniya' button to open the Create Campaign form.
        # Yeni Kampaniya link
        elem = page.get_by_role('link', name='Yeni Kampaniya', exact=True)
        await elem.click(timeout=10000)
        
        # -> Fill the 'Kampaniya Adı' field with a unique name, set 'Başlama Tarixi' to 2026-07-10 and 'Bitmə Tarixi' to 2026-07-01 (earlier), then click the 'Aktivləşdir' button to submit the form.
        # title text field
        elem = page.locator('[id="id_title"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("Automation Test Campaign 2026-07-06")
        
        # -> Fill the 'Kampaniya Adı' field with a unique name, set 'Başlama Tarixi' to 2026-07-10 and 'Bitmə Tarixi' to 2026-07-01 (earlier), then click the 'Aktivləşdir' button to submit the form.
        # start_date date field
        elem = page.locator('[id="id_start_date"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("2026-07-10")
        
        # -> Fill the 'Kampaniya Adı' field with a unique name, set 'Başlama Tarixi' to 2026-07-10 and 'Bitmə Tarixi' to 2026-07-01 (earlier), then click the 'Aktivləşdir' button to submit the form.
        # end_date date field
        elem = page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div[2]/input").nth(0)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("2026-07-01")
        
        # -> Fill the 'Kampaniya Adı' field with a unique name, set 'Başlama Tarixi' to 2026-07-10 and 'Bitmə Tarixi' to 2026-07-01 (earlier), then click the 'Aktivləşdir' button to submit the form.
        # Aktivləşdir button
        elem = page.get_by_role('button', name='Aktivləşdir', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify the campaign is not created
        # Assert: The URL remains on /evaluations/campaigns/create/, confirming the campaign was not created.
        await expect(page).to_have_url(re.compile("/evaluations/campaigns/create/"), timeout=15000), "The URL remains on /evaluations/campaigns/create/, confirming the campaign was not created."
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
    