from playwright.sync_api import sync_playwright
from PIL import Image
import time, os

def crop_comments(path):
    img = Image.open(path)
    width, height = img.size
    
    # Comment drawer sits in the bottom portion of the screen
    top = int(height * 0.3)      # skip the reel above
    bottom = int(height * 0.95)  # skip bottom nav
    
    cropped = img.crop((0, top, width, bottom))
    cropped.save(path)

def get_comments(page, index):
    try:
        # Click comment icon
        page.locator("[aria-label='Comment']").first.click()
        time.sleep(2)

        # Screenshot the comment drawer
        path = f"screenshots/comments_{index}.png"
        page.screenshot(path=path, full_page=False)

        # Close drawer
        page.keyboard.press("Escape")
        time.sleep(1)

        return path
    except:
        return None

def crop_reel(path):
    img = Image.open(path)
    width, height = img.size
    
    # Crop out top nav and bottom UI chrome
    left = int(width * 0.2)      # skip left 2%
    right = int(width * 0.85) 
    top = int(height * 0.05)      # skip top 5% (nav bar)
    bottom = int(height * 0.88)   # skip bottom 12% (like/comment buttons)
    
    cropped = img.crop((left, top, right, bottom))
    cropped.save(path)

def scrape_feed(count=10):
    os.makedirs("screenshots", exist_ok=True)
    screenshots = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        viewport = {"width": 930, "height": 1000}

        if os.path.exists("session.json"):
            context = browser.new_context(
                storage_state="session.json",
                viewport=viewport
            )
        else:
            context = browser.new_context(viewport=viewport)

        page = context.new_page()
        page.goto("https://www.instagram.com/reels/")
        
        # Give user time to log in if needed
        print("Log in to Instagram if prompted, then press Enter here...")
        input()

        # Save session for next time
        context.storage_state(path="session.json")

        # Scroll and screenshot
        print(f"Capturing {count} posts...")
        captured = 0

        while captured < count:
            # Screenshot the current viewport
            path = f"screenshots/post_{captured}.png"
            path = f"screenshots/comments_{captured}.png"
            page.screenshot(path=path, full_page=False)
            crop_reel(path) 
            comments_path = get_comments(page, captured)
            screenshots.append((path, comments_path))   
            captured += 1

            # Scroll down
            page.keyboard.press("ArrowDown")
            time.sleep(1.5)  # wait for content to load

        browser.close()

    return screenshots