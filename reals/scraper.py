from playwright.sync_api import sync_playwright
import time, os

def scrape_feed(count=10):
    os.makedirs("screenshots", exist_ok=True)
    screenshots = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Try to load saved session
        if os.path.exists("session.json"):
            context = p.chromium.launch(headless=False).new_context(
                storage_state="session.json"
            )

        page = context.new_page()
        page.goto("https://www.instagram.com/")
        
        # Give user time to log in if needed
        print("👉 Log in to Instagram if prompted, then press Enter here...")
        input()

        # Save session for next time
        context.storage_state(path="session.json")

        # Scroll and screenshot
        print(f"📸 Capturing {count} posts...")
        captured = 0
        last_height = 0

        while captured < count:
            # Screenshot the current viewport
            path = f"screenshots/post_{captured}.png"
            page.screenshot(path=path, full_page=False)
            screenshots.append(path)
            captured += 1

            # Scroll down
            page.evaluate("window.scrollBy(0, 600)")
            time.sleep(2)  # wait for content to load

        browser.close()

    return screenshots