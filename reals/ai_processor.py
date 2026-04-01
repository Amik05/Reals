import anthropic, base64

client = anthropic.Anthropic()

def process_screenshot(image_path):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    }
                },
                {
                    "type": "text",
                    "text": """This is a screenshot of an Instagram feed. 
                    Extract and return ONLY a JSON object with these fields:
                    - username: the poster's username (or 'unknown')
                    - caption: the post caption text (or empty string)
                    - type: 'reel', 'photo', or 'carousel'
                    - summary: one punchy sentence describing what this post is about
                    Return only valid JSON, nothing else."""
                }
            ]
        }]
    )

    import json
    try:
        text = message.content[0].text
        return json.loads(text)
    except:
        return {
            "username": "unknown",
            "caption": "",
            "type": "photo",
            "summary": "Instagram post"
        }