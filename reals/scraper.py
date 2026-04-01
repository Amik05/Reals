from playwright.sync_api import sync_playwright
from PIL import Image
import time, os

def crop_comments(path):
    img = Image.open(path)
    width, height = img.size
    
   # Crop out top nav and bottom UI chrome
    left = int(width * 0.45)      # skip left 2%
    right = int(width * 0.77) 
    top = int(height * 0.09)      # skip top 5% (nav bar)
    bottom = int(height * 0.7)   # skip bottom 12% (like/comment buttons)
    
    cropped = img.crop((left, top, right, bottom))
    cropped.save(path)

def get_comments(page, captured):
    try:
        # Click center first to focus current reel
        page.mouse.click(215, 466)
        time.sleep(1)

        # Click comment button by position (right side, ~60% down)
        #731.25, y:670
        page.mouse.click(735, 680)
        time.sleep(2)

        path = f"screenshots/comments_{captured}.png"
        page.screenshot(path=path, full_page=False)
        crop_comments(path)

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
            page = context.new_page()
            page.goto("https://www.instagram.com/reels/")
            # page.pause()
            print("Continuing saved session.")
        else:
            context = browser.new_context(viewport=viewport)
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
            crop_reel(path) 
            comments_path = get_comments(page, captured)
            screenshots.append((path, comments_path))   
            captured += 1
            page.keyboard.press("ArrowDown")
            time.sleep(2)  # wait for content to load

        browser.close()

    return screenshots