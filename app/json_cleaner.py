import json
import logging

def clean(output):
    """
    Cleans the JSON model output of an LLM.
    """
    output = output.strip()
    if output.startswith("```json"):
        output = output[7:]
    if output.endswith("```"):
        output = output[:-3]
    cleaned_output = output.strip()

    try:
        json_data = json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")
        return cleaned_output

    def clean_json(data):
        if isinstance(data, dict):
            return {key: clean_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [clean_json(item) for item in data]
        elif isinstance(data, str):
            return "" if data.lower() in ["unknown", "na", "null"] else data
        else:
            return data

    cleaned_json_data = clean_json(json_data)
    #cleaned_output = json.dumps(cleaned_json_data, ensure_ascii=False)

    return cleaned_json_data