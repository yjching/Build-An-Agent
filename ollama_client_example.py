import re
import os
from dotenv import load_dotenv, find_dotenv

from clients.ollama import OllamaClient

base_client = OllamaClient(
    model_name="mistral",
    system_prompt=""
)

base_client.generate_completion("What is the capital of France?")

