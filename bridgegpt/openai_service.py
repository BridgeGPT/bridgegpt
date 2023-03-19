import getpass

import openai
import os


class OpenAIService:
    def __init__(self):
        self.prompt = ""
        self.context = []
        self.model_id = "gpt-3.5-turbo"
        openai.api_key = os.environ["OPENAI_API_KEY"]

        # Get the path to the base prompt file
        script_dir = os.path.dirname(os.path.realpath(__file__))
        prompt_path = os.path.join(script_dir, "base_prompt.txt")

        # Read the base prompt from the file
        with open(prompt_path, "r") as f:
            self.prompt = f.read().strip()

        self.context.append({"role": "system", "content": self.prompt})

    def generate_response(self, user_input):
        self.context.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model=self.model_id,
            temperature=0.9,
            max_tokens=2048,
            n=1,
            stop=None,
            presence_penalty=0,
            frequency_penalty=0,
            messages=self.context
        )
        msg = response.choices[0].message
        ai_response = msg.content.strip()
        self.context.append({"role": msg.role, "content": ai_response})
        return ai_response
