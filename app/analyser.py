from app.prompts import get_full_analysis_prompt
from app import openai_client
from app.database.databaser import db

import app.json_cleaner as json_cleaner

def analyse(username):

    profile = db.get_profile_by_username(username)
    # Prepare the prompt with user data
    prompt = get_full_analysis_prompt(profile)
    
    # Call the generate_output function from openai_client
    response = openai_client.gpt4o_text(prompt)

    result = json_cleaner.clean(response)
    
    # Return the analysis result
    return result

if __name__ == "__main__":
    # Example user data for testing
    user_data = {"name": "John Doe", "age": 30, "bio": "Software developer..."}
    result = analyse(user_data)
    print(result)