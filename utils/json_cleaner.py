import json
import re

def extract_clean_json(text: str) -> dict:
    """
    Attempts to extract the first valid JSON object from an LLM response.
    """
    text = text.strip()
    # Remove markdown-style code fencing
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).strip("` \n")

    # Extract first {...} JSON object
    json_match = re.search(r"{.*}", text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(0))
    else:
        raise ValueError("No valid JSON object found")