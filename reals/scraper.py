from playwright.async_api import async_playwright
import asyncio, os

async def capture(browser, i, screenshots, seen_urls, lock):
    ctx = await browser.new_context(
        viewport={"width": 430, "height": 932},
        storage_state="session.json"
    )
    pg = await ctx.new_page()
    await pg.goto("https://www.instagram.com/reels/")
    await pg.wait_for_load_state("load", timeout=30000)
    await asyncio.sleep(2)

    # Keep scrolling until we find a unique URL
    while True:
        current_url = pg.url

        async with lock:
            if current_url not in seen_urls:
                seen_urls.add(current_url)
                break  # Unique URL found, take screenshot

        # Duplicate — scroll to next reel
        print(f"Window {i + 1}: Duplicate URL, scrolling to next reel...")
        await pg.keyboard.press("ArrowDown")
        await asyncio.sleep(1.5)

    path = f"screenshots/post_{i}.png"
    await pg.screenshot(path=path, full_page=False)
    screenshots[i] = path
    print(f"Window {i + 1}: Captured {current_url}")
    await ctx.close()

async def scrape_feed_async(count=10):
    os.makedirs("screenshots", exist_ok=True)
    screenshots = [None] * count
    seen_urls = set()
    lock = asyncio.Lock()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        if os.path.exists("session.json"):
            ctx = await browser.new_context(
                viewport={"width": 430, "height": 932},
                storage_state="session.json"
            )
            pg = await ctx.new_page()
            await pg.goto("https://www.instagram.com/reels/")
            print("Continuing saved session.")
        else:
            ctx = await browser.new_context(viewport={"width": 430, "height": 932})
            pg = await ctx.new_page()
            await pg.goto("https://www.instagram.com/reels/")
            print("Log in to Instagram if prompted, then press Enter here...")
            input()

        await ctx.storage_state(path="session.json")
        await ctx.close()

        print(f"Opening {count} windows simultaneously...")
        await asyncio.gather(*[capture(browser, i, screenshots, seen_urls, lock) for i in range(count)])

        await browser.close()

    return [s for s in screenshots if s]

def scrape_feed(count=10):
    return asyncio.run(scrape_feed_async(count))