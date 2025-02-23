import re
import json

from clients.ollama import OllamaClient
from prompts.base_prompts import TOOL_SYSTEM_PROMPT
from tools.base_tools import get_space_news
from strategies.react import ReActStrategy

base_client = OllamaClient(
    model_name="mistral",
    system_prompt=TOOL_SYSTEM_PROMPT
)

## ReAcT
agent = ReActStrategy(base_client, [get_space_news])