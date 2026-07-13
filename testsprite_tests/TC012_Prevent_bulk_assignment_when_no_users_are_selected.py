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
        
        # -> Click the 'Login' link to open the sign-in page.
        # Login link
        elem = page.get_by_role('link', name='Login', exact=True)
        await elem.click(timeout=10000)
        
        # -> Fill the 'İstifadəçi adı və ya E-poçt' field with admin, fill the 'Şifrə' field with password, then click the 'Daxil Ol' (Sign in) button.
        # İstifadəçi adınızı daxil edin text field
        elem = page.locator('[id="id_username"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin")
        
        # -> Fill the 'İstifadəçi adı və ya E-poçt' field with admin, fill the 'Şifrə' field with password, then click the 'Daxil Ol' (Sign in) button.
        # Şifrənizi daxil edin password field
        elem = page.locator('[id="id_password"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("password")
        
        # -> Fill the 'İstifadəçi adı və ya E-poçt' field with admin, fill the 'Şifrə' field with password, then click the 'Daxil Ol' (Sign in) button.
        # Daxil Ol button
        elem = page.get_by_role('button', name='Daxil Ol', exact=True)
        await elem.click(timeout=10000)
        
        # -> Open the 'Evaluations' menu to find the Bulk Assign page or link.
        # Evaluations button
        elem = page.get_by_role('button', name='Evaluations', exact=True)
        await elem.click(timeout=10000)
        
        # -> Open the 'Bulk Assign' page (navigate to the Bulk Assign page) so the bulk-assign form can be tested.
        await page.goto("http://localhost:8000/evaluations/bulk-assign/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Scroll the Bulk Assign page to reveal the campaign selection control and the bottom of the form so a campaign can be selected and the assignment attempted.
        await page.mouse.wheel(0, 300)
        
        # -> Click the 'Heç birini seçmə' (Deselect All) link to ensure no recipients are selected.
        # Heç birini seçmə link
        elem = page.locator('[id="deselectAll"]')
        await elem.click(timeout=10000)
        
        # -> Scroll the Bulk Assign page down to reveal the campaign selection control (labelled 'Kampaniyalar') so a campaign can be chosen.
        await page.mouse.wheel(0, 300)
        
        # -> Scroll up to reveal the campaign selection control labelled 'Kampaniyalar' so the campaign dropdown can be observed.
        await page.mouse.wheel(0, 300)
        
        # -> Reveal the campaign dropdown labelled 'Kampaniyalar' by locating the label on the page and scrolling to it so it can be selected.
        await page.mouse.wheel(0, 300)
        
        # -> Scroll up one full page to reveal the campaign dropdown labelled 'Kampaniyalar' so it can be inspected and used.
        await page.mouse.wheel(0, 300)
        
        # -> Scroll the Bulk Assign page down to reveal the 'Kampaniyalar' campaign dropdown so it can be selected.
        await page.mouse.wheel(0, 300)
        
        # -> Click the 'Tapşırıqları Yarat' (Create Assignments) button to submit the bulk assign form without any recipients selected and observe validation feedback.
        # Tapşırıqları Yarat button
        elem = page.locator('[id="submitBtn"]')
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify no assignments are completed
        # Assert: Page remained on the bulk-assign URL, indicating no assignments were completed.
        await expect(page).to_have_url(re.compile("/evaluations/bulk\\-assign/"), timeout=15000), "Page remained on the bulk-assign URL, indicating no assignments were completed."
        await page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div[2]/form/div[4]/div/button[2]").nth(0).scroll_into_view_if_needed()
        # Assert: The 'Tapşırıqları Yarat' button is still visible, indicating no assignments were completed.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div[2]/div/div/div/div[2]/div[2]/form/div[4]/div/button[2]").nth(0)).to_be_visible(timeout=15000), "The 'Tap\u015f\u0131r\u0131qlar\u0131 Yarat' button is still visible, indicating no assignments were completed."
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
    