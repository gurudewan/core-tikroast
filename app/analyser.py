from app.prompts import get_full_analysis_prompt
from app import openai_client
from app.database.databaser import db
import asyncio
import app.json_cleaner as json_cleaner


async def analyse(username: str) -> str:
    profile = await db.get_profile_by_username(username)  # Assuming this is an async function
    # Prepare the prompt with user data
    prompt = get_full_analysis_prompt(profile)
    
    # Call the generate_output function from openai_client
    response = await openai_client.gpt4o_text(prompt)

    result = json_cleaner.clean(response)
    
    # Return the analysis result
    return result

if __name__ == "__main__":
    # Example user data for testing
    username = "John_Doe" # As username should be str, not dict.
    
    async def main():
        result = await analyse(username)
        print(result)

    # Run the main coroutine
    asyncio.run(main())