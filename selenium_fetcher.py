import undetected_chromedriver as uc
from pyvirtualdisplay import Display
import time


def get_html(url: str) -> str:
    """
    Launches Chrome with stealth patches, opens the given URL,
    and returns the rendered HTML.
    """
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    # Initialize Chrome with stealth options
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")


    driver = uc.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

    try:
        driver.get(url)
        print("Waiting 10 seconds for initial Cloudflare challenge resolution...")
        time.sleep(10)

        print("Waiting up to 45 seconds for final page to load...")


        # Grab the rendered HTML after Cloudflare verification
        html = driver.page_source
        return html
    except Exception as e:
        print(f"An error occurred during page loading/waiting. The page may still be blocked or timed out: {e}")
        # In case of failure, return the current page source (which will be the CF block page)
        return driver.page_source 
    finally:
        driver.quit()
