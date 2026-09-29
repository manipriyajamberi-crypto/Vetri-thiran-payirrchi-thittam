from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_FLASH_MODEL,
)

from app.schemas import (
    OutlineResponse,
    PromptRequest,
)


def get_client():

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please add it to your .env file."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_outline(
    request: PromptRequest,
) -> OutlineResponse:

    prompt = f"""
You are a professional comic story planner.

Create a coherent 5-panel comic outline.

USER STORY PROMPT:
{request.story_prompt}

MAIN CHARACTER:
{request.character_name}

SETTING:
{request.setting}

STORY TONE:
{request.tone}

ART STYLE:
{request.art_style}

Requirements:

1. Create exactly 5 panels.
2. Panels must be chronological.
3. Keep the main character consistent.
4. Create a clear beginning.
5. Develop the conflict or main event.
6. Create a satisfying ending.
7. Each panel needs:
   - panel_number
   - title
   - scene_description
   - image_prompt
8. Do not write dialogue inside image_prompt.
9. The image prompt must describe:
   - characters
   - environment
   - composition
   - lighting
   - action
   - art style
10. Keep the visual identity consistent between panels.
"""

    client = get_client()

    response = client.models.generate_content(
        model=GEMINI_FLASH_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
            response_schema=OutlineResponse,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini Flash returned an empty response."
        )

    return OutlineResponse.model_validate_json(
        response.text
    )