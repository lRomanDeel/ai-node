import requests
import json
from kernel.llm.base_client import BaseLLMClient


class OllamaClient(BaseLLMClient):
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"

    def generate(self, model: str, prompt: str, max_tokens: int = 30):
        response = requests.post(
            self.url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "num_predict": max_tokens
                }
            },
            stream=True
        )

        full = ""

        for line in response.iter_lines():
            if not line:
                continue

            try:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                print(token, end="", flush=True)
                full += token
            except:
                pass

        print("\n")
        return full.strip()
