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
        
        # -> Navigate to the login page (/accounts/login/) to open the 'Login' form.
        await page.goto("http://localhost:8000/accounts/login/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the username field with 'admin', fill the password field with 'password', then click the 'Daxil Ol' button to log in.
        # İstifadəçi adınızı daxil edin text field
        elem = page.locator('[id="id_username"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin")
        
        # -> Fill the username field with 'admin', fill the password field with 'password', then click the 'Daxil Ol' button to log in.
        # Şifrənizi daxil edin password field
        elem = page.locator('[id="id_password"]')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("password")
        
        # -> Fill the username field with 'admin', fill the password field with 'password', then click the 'Daxil Ol' button to log in.
        # Daxil Ol button
        elem = page.get_by_role('button', name='Daxil Ol', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'İşçi Mənsubiyyəti' sidebar item to open the recruitment submenu.
        # İşçi Mənsubiyyəti button
        elem = page.get_by_role('button', name='İşçi Mənsubiyyəti', exact=True)
        await elem.click(timeout=10000)
        
        # -> Scroll the sidebar/page to reveal additional recruitment links (look for a link labeled like 'Vakansiyalar', 'İş Elanları', or 'Job Vacancies').
        await page.mouse.wheel(0, 300)
        
        # -> Click the 'Vakansiyalar' or 'İş Elanları' link in the recruitment submenu (when it becomes visible).
        await page.mouse.wheel(0, 300)
        
        # -> Scroll the left navigation sidebar further down to reveal the 'Vakansiyalar' or 'İş Elanları' link.
        await page.mouse.wheel(0, 300)
        
        # -> Scroll the left sidebar navigation to reveal submenu items under 'İşçi Mənsubiyyəti', looking for 'Vakansiyalar' or 'İş Elanları'.
        await page.mouse.wheel(0, 300)
        
        # -> Click the 'HR İdarəetməsi' (HR Management) sidebar item to reveal recruitment-related submenu links such as 'Vakansiyalar' (Job Vacancies).
        # HR İdarəetməsi button
        elem = page.get_by_role('button', name='HR İdarəetməsi', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Vakansiya Yarat' link in the left navigation to open the job vacancy creation page.
        # Vakansiya Yarat link
        elem = page.get_by_role('link', name='Vakansiya Yarat', exact=True)
        await elem.click(timeout=10000)
        
        # -> Fill the 'Vəzifə Adı' field with 'Sınaq Mühəndisi (QA Automation)', fill 'Kod' with 'QA-2026-01', and select 'Nazirin Aparatı' from the 'Şöbə' dropdown.
        # title text field
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/div/form/div/input')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("S\u0131naq M\u00fch\u0259ndisi (QA Automation)")
        
        # -> Fill the 'Vəzifə Adı' field with 'Sınaq Mühəndisi (QA Automation)', fill 'Kod' with 'QA-2026-01', and select 'Nazirin Aparatı' from the 'Şöbə' dropdown.
        # code text field
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/div/form/div[2]/div/div/input')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("QA-2026-01")
        
        # -> Fill the 'Vəzifə Adı' field with 'Sınaq Mühəndisi (QA Automation)', fill 'Kod' with 'QA-2026-01', and select 'Nazirin Aparatı' from the 'Şöbə' dropdown.
        # Seçin Nazirin Aparatı Rəqəmsal İnkişaf... dropdown
        elem = page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/div/form/div[2]/div[2]/div/select").nth(0)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.select_option("")
        
        # -> Fill the 'Təsvir', 'Vəzifə Öhdəlikləri', and 'Tələblər' fields with valid content and click the 'Yarat' button to submit the new vacancy.
        # description text area
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/div/form/div[3]/textarea')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("Responsible for designing, developing, and maintaining automated tests for web applications. Collaborate with development and product teams to ensure high-quality software releases. Participate in test planning and continuous improvement of QA processes.")
        
        # -> Fill the 'Təsvir', 'Vəzifə Öhdəlikləri', and 'Tələblər' fields with valid content and click the 'Yarat' button to submit the new vacancy.
        # responsibilities text area
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/div/form/div[4]/textarea')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("\u2022 Develop and maintain automated test suites.\n\u2022 Create and execute test plans and test cases.\n\u2022 Validate bug fixes and perform regression testing.\n\u2022 Work with developers to reproduce and triage defects.")
        
        # -> Fill the 'Təsvir', 'Vəzifə Öhdəlikləri', and 'Tələblər' fields with valid content and click the 'Yarat' button to submit the new vacancy.
        # requirements text area
        elem = page.locator('xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/div/form/div[5]/textarea')
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("\u2022 Bachelor's degree in Computer Science or related field preferred.\n\u2022 2+ years of experience in QA automation.\n\u2022 Experience with Selenium, Cypress, or similar tools.\n\u2022 Strong analytical and communication skills.")
        
        # -> Fill the 'Təsvir', 'Vəzifə Öhdəlikləri', and 'Tələblər' fields with valid content and click the 'Yarat' button to submit the new vacancy.
        # Yarat button
        elem = page.get_by_role('button', name='Yarat', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify a success confirmation is visible
        await page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[1]").nth(0).scroll_into_view_if_needed()
        # Assert: The 'Redaktə Et' (Edit) button is visible, confirming the vacancy was created successfully.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[1]").nth(0)).to_be_visible(timeout=15000), "The 'Redakt\u0259 Et' (Edit) button is visible, confirming the vacancy was created successfully."
        await page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[2]").nth(0).scroll_into_view_if_needed()
        # Assert: The 'Yayımla' (Publish) button is visible, confirming the vacancy was created successfully.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[2]").nth(0)).to_be_visible(timeout=15000), "The 'Yay\u0131mla' (Publish) button is visible, confirming the vacancy was created successfully."
        await page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[3]").nth(0).scroll_into_view_if_needed()
        # Assert: The 'Paylaş' (Share) button is visible, confirming the vacancy was created successfully.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[3]").nth(0)).to_be_visible(timeout=15000), "The 'Payla\u015f' (Share) button is visible, confirming the vacancy was created successfully."
        
        # --> Verify the new job vacancy is created
        await page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[1]").nth(0).scroll_into_view_if_needed()
        # Assert: The vacancy's Edit (Redaktə Et) button is visible on the detail page.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[1]").nth(0)).to_be_visible(timeout=15000), "The vacancy's Edit (Redakt\u0259 Et) button is visible on the detail page."
        await page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[2]").nth(0).scroll_into_view_if_needed()
        # Assert: The vacancy's Publish (Yayımla) button is visible on the detail page.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[2]").nth(0)).to_be_visible(timeout=15000), "The vacancy's Publish (Yay\u0131mla) button is visible on the detail page."
        await page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[3]").nth(0).scroll_into_view_if_needed()
        # Assert: The vacancy's Share (Paylaş) button is visible on the detail page.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/button[3]").nth(0)).to_be_visible(timeout=15000), "The vacancy's Share (Payla\u015f) button is visible on the detail page."
        await page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/a").nth(0).scroll_into_view_if_needed()
        # Assert: The Back (Geri) link is visible on the vacancy detail page.
        await expect(page.locator("xpath=/html/body/div[2]/div/main/div/div/div/div[2]/div/a").nth(0)).to_be_visible(timeout=15000), "The Back (Geri) link is visible on the vacancy detail page."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    