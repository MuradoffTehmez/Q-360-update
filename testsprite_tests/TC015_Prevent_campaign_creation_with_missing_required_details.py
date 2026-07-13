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
        
        # -> Open the Login page and sign in using username 'admin' and password 'password'.
        await page.goto("http://localhost:8000/accounts/login/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill 'admin' into the "İstifadəçi adı və ya E-poçt" field, fill 'password' into the "Şifrə" field, then click the 'Daxil Ol' button to submit the login form.
        # İstifadəçi adınızı daxil edin text field
        elem = page.locator('[id="id_username"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin")
        
        # -> Fill 'admin' into the "İstifadəçi adı və ya E-poçt" field, fill 'password' into the "Şifrə" field, then click the 'Daxil Ol' button to submit the login form.
        # Şifrənizi daxil edin password field
        elem = page.locator('[id="id_password"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("password")
        
        # -> Fill 'admin' into the "İstifadəçi adı və ya E-poçt" field, fill 'password' into the "Şifrə" field, then click the 'Daxil Ol' button to submit the login form.
        # Daxil Ol button
        elem = page.get_by_role('button', name='Daxil Ol', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'CAMPAIGNS' card on the dashboard to open the Campaigns section.
        # Click the 'CAMPAIGNS' card on the dashboard to open the Campaigns section.
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div[3]/div/div[2]/div/div[2]/i')
        await elem.click(timeout=10000)
        
        # -> Click the 'Qiymətləndirmə və Rəylər' (Evaluations & Reviews) item in the left navigation to open the evaluations menu.
        # Qiymətləndirmə və Rəylər button
        elem = page.get_by_role('button', name='Qiymətləndirmə və Rəylər', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Kampaniyalar' link in the left navigation to open the Campaigns section.
        # Kampaniyalar link
        elem = page.get_by_role('link', name='Kampaniyalar', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the '+ Yeni Kampaniya' button to open the Create Campaign form or page.
        # Yeni Kampaniya link
        elem = page.get_by_role('link', name='Yeni Kampaniya', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Aktivləşdir' (Activate) button to submit the campaign form with required fields left empty.
        # Aktivləşdir button
        elem = page.get_by_role('button', name='Aktivləşdir', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify campaign validation errors are visible
        # Assert: The start date input shows invalid="true", indicating a validation error.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div[1]/input").nth(0)).to_have_attribute("invalid", "true", timeout=15000), "The start date input shows invalid=\"true\", indicating a validation error."
        # Assert: The end date input shows invalid="true", indicating a validation error.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div[2]/input").nth(0)).to_have_attribute("invalid", "true", timeout=15000), "The end date input shows invalid=\"true\", indicating a validation error."
        
        # --> Verify the campaign is not created
        # Assert: The browser is still on the Create Campaign URL, indicating no redirect after submission.
        await expect(page).to_have_url(re.compile("evaluations/campaigns/create/"), timeout=15000), "The browser is still on the Create Campaign URL, indicating no redirect after submission."
        # Assert: The start date input is marked invalid, showing validation prevented creation.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div[1]/input").nth(0)).to_have_attribute("invalid", "true", timeout=15000), "The start date input is marked invalid, showing validation prevented creation."
        # Assert: The end date input is marked invalid, showing validation prevented creation.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div/form/div[1]/div[3]/div[2]/input").nth(0)).to_have_attribute("invalid", "true", timeout=15000), "The end date input is marked invalid, showing validation prevented creation."
        await page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div/form/div[3]/div/button[2]").nth(0).scroll_into_view_if_needed()
        # Assert: The 'Aktivləşdir' button is still visible on the Create Campaign form, indicating the form remains displayed and creation did not complete.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div/form/div[3]/div/button[2]").nth(0)).to_be_visible(timeout=15000), "The 'Aktivl\u0259\u015fdir' button is still visible on the Create Campaign form, indicating the form remains displayed and creation did not complete."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    