import openai
import os

openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this may change in the future

def ChatCompletion(deployment: str, prompt: str) -> str:
    '''
    Use chat models like completion models.
    '''
    response = openai.ChatCompletion.create(
        engine=deployment,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']