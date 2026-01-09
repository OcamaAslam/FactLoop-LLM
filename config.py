import os
from openai import OpenAI

# API Configuration
# Note: In a production environment, use os.environ.get() for keys
BASE_URL = "https://integrate.api.nvidia.com/v1"
API_KEY = "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"
MODEL_NAME = "openai/gpt-oss-20b"

# Initialize Client
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

class Args:
    """Configuration arguments for the reflection loops."""
    max_knowledge_loop = 2
    max_response_loop = 2
    threshold_fact = 0.8
    threshold_cons = 0.8
    temperature = 0.7

# Global instance
args = Args()