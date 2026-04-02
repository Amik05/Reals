from dotenv import load_dotenv
import anthropic, base64, os, json
load_dotenv()

PROVIDER = os.getenv("AI_PROVIDER", "claude")  # "claude" or "gemini"

def process_screenshot(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()

    if PROVIDER == "gemini":
        return _process_gemini(image_data)
    else:
        return _process_claude(image_data)

PROMPT = """This is a screenshot of an Instagram Reel.
Extract and return ONLY a JSON object with these fields:
- username: the poster's username (or 'unknown')
- caption: the post caption text (or empty string)
- type: 'reel', 'photo', or 'carousel'
- summary: a vivid one sentence description of the visual content, written as if describing it to someone who cannot see it
Return only valid JSON, nothing else."""

def _parse(text):
    try:
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(text)
    except Exception as e:
        print("Parse error:", e)
        return {"username": "unknown", "caption": "", "type": "photo", "summary": "Instagram post"}

def _process_claude(image_data):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system="You are a helpful assistant that analyzes Instagram screenshots and returns structured JSON only. No preamble, no markdown, no backticks.",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": base64.b64encode(image_data).decode("utf-8")}},
                {"type": "text", "text": PROMPT}
            ]
        }]
    )
    return _parse(message.content[0].text)

def _process_gemini(image_data):
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")

    import PIL.Image, io
    img = PIL.Image.open(io.BytesIO(image_data))

    response = model.generate_content([PROMPT, img])
    return _parse(response.text)