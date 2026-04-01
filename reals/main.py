from scraper import scrape_feed
from ai_processor import process_screenshot
from pdf_builder import build_pdf

COUNT = 8  # keep low for hackathon demo speed

print("🚀 Starting Reals...")
screenshots = scrape_feed(count=COUNT)

print("🤖 Processing with AI...")
post_data = [process_screenshot(s) for s in screenshots]

print("📄 Building PDF...")
build_pdf(screenshots, post_data)

print("🎉 Done! Open reals.pdf and print it.")