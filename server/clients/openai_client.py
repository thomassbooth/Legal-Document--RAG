import os
from openai import OpenAI

# Singleton pattern for the OpenAI client to prevent multiple instances
class OpenAIClient:
    _client = None

    def __new__(cls, *args, **kwargs):
        # Check if an instance already exists
        if cls._client is None:
            print('Creating a new OpenAIClient instance.')
            # Create a new instance if none exists
            cls._client = super().__new__(cls)
            # Initialize the OpenAI client
            api_key = "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" # Set the API key from environment variables
            cls._client = OpenAI(api_key=api_key)  # Store the OpenAI client in the class variable
        else:
            print('Using existing OpenAIClient instance.')

        # Return the OpenAI client instance directly
        return cls._client