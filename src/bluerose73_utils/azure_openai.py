import openai
from openai.error import *
import os
import logging
from sys import stderr
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    wait_exponential,
    stop_after_attempt,
    after_log,
)
from loguru import logger

openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this may change in the future

@retry(
    retry=retry_if_exception_type(
        exception_types=(
            RateLimitError,
            Timeout,
            ServiceUnavailableError,
            APIConnectionError,
            APIError,
            TryAgain,
            KeyError,
        )
    ),
    wait=wait_exponential(multiplier=1, min=5, max=60),
    stop=stop_after_attempt(50),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.WARNING),
    reraise=True,
)
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
    resp = response.choices[0].message.get('content')
    if resp is None:
        return ""
    return resp

@retry(
    retry=retry_if_exception_type(
        exception_types=(
            RateLimitError,
            Timeout,
            ServiceUnavailableError,
            APIConnectionError,
            APIError,
            TryAgain,
            KeyError,
        )
    ),
    wait=wait_exponential(multiplier=1, min=5, max=60),
    stop=stop_after_attempt(50),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.WARNING),
    reraise=True,
)
def Embedding(deployment: str, text: str) -> str:
    '''
    Create embeddings
    '''
    response = openai.Embedding.create(
        engine=deployment,
        input=text
    )
    resp = response['data'][0]['embedding']
    return resp