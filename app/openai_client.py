from openai import AsyncAzureOpenAI
import sys
import os
import asyncio
# add root for importing consts:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app.consts as consts

# Initialize the Azure OpenAI client
client = AsyncAzureOpenAI(
    api_key=consts.AZURE_OPENAI_KEY,
    api_version="2023-03-15-preview",
    azure_endpoint=consts.AZURE_OPENAI_ENDPOINT
)

deployment_name = consts.AZURE_OPENAI_DEPLOYMENT

async def gpt4o_text(prompt: str) -> str:
    """
    Gpt-4o model
    """
    client = AsyncAzureOpenAI(
        api_key=consts.AZURE_OPENAI_KEY,
        api_version="2023-03-15-preview",
        base_url=f"{consts.AZURE_OPENAI_ENDPOINT}/openai/deployments/{consts.AZURE_OPENAI_DEPLOYMENT}",
    )

    response = await client.chat.completions.create(
        model=consts.AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a tik tok profile analyser."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=4000,
        temperature=0.7,
    )

    return response.choices[0].message.content

async def gpt4o_image_url_to_text(image_url, prompt):
    """
    Gpt-4o model using image url
    """
    client = AsyncAzureOpenAI(
        api_key=consts.AZURE_OPENAI_KEY,
        api_version="2023-03-15-preview",
        base_url=f"{consts.AZURE_OPENAI_ENDPOINT}/openai/deployments/{consts.AZURE_OPENAI_DEPLOYMENT}",
    )

    response = await client.chat.completions.create(
        model=consts.AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant to analyse images.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            },
        ],
        max_tokens=4000,
        temperature=0.5,
    )

    return response.choices[0].message.content

# Example usage
async def main():
    prompt = "What is 4 X 2."
    output = await gpt4o_text(prompt)
    print(output)

    image_url = "https://replicate.delivery/mgxm/f4e50a7b-e8ca-432f-8e68-082034ebcc70/demo.jpg"
    caption = await gpt4o_image_url_to_text(image_url, "What is this?")
    print(caption)


if __name__ == "__main__":
    asyncio.run(main())
