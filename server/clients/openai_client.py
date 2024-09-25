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
            cls._client = OpenAI(api_key=api_key)  # Store the OpenAI client in the class variable
        else:
            print('Using existing OpenAIClient instance.')

        # Return the OpenAI client instance directly
        return cls._client