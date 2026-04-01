from playwright.sync_api import sync_playwright
import time, os

def scrape_feed(count=10):
    os.makedirs("screenshots", exist_ok=True)
    screenshots = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        if os.path.exists("session.json"):
            context = browser.new_context(
                viewport={"width": 430, "height": 932},
                storage_state="session.json"
            )
            page = context.new_page()
            page.goto("https://www.instagram.com/reels/")
            print("Continuing saved session.")
        else:
            context = browser.new_context(viewport={"width": 430, "height": 932})
            page = context.new_page()
            page.goto("https://www.instagram.com/reels/")
            print("Log in to Instagram if prompted, then press Enter here...")
            input()

        context.storage_state(path="session.json")

        print(f"Capturing {count} posts...")
        captured = 0

        while captured < count:
            path = f"screenshots/post_{captured}.png"
            page.screenshot(path=path, full_page=False)
            screenshots.append(path)
            captured += 1
            page.keyboard.press("ArrowDown")
            time.sleep(1)

        browser.close()

    return screenshots