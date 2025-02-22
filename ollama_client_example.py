import re
import json

from clients.ollama import OllamaClient
from prompts.base_prompts import TOOL_SYSTEM_PROMPT
from tools.base_tools import get_space_news
from strategies.tool import SingleToolStrategy

base_client = OllamaClient(
    model_name="mistral",
    system_prompt=TOOL_SYSTEM_PROMPT
)

agent = SingleToolStrategy(base_client)

question = "What is the latest news on space? Return at least 5 articles."

agent.run(question, [get_space_news])

