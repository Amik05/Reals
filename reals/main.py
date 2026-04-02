import sys
from scraper import scrape_feed
from ai_processor import process_screenshot
from pdf_builder import build_pdf

COUNT = 1  # keep low for hackathon demo speed

DRY_RUN = "--dry-run" in sys.argv   

DUMMY_DATA = {
    "username": "natgeo",
    "caption": "japan is turning footsteps into energy",
    "type": "photo",
    "summary": "Stunning shot of shibuya crossing"
}

print("Starting Reals...")
screenshots = scrape_feed(count=COUNT)

if DRY_RUN:
    print("Dry run - skipping AI calss")
    post_data = [DUMMY_DATA] * len(screenshots)
else:
    print("Processing with AI...")
    post_data = [process_screenshot(s) for s, c in screenshots]


print("Building PDF...")
build_pdf(screenshots, post_data)

print("Done! Open reals.pdf and print it.")