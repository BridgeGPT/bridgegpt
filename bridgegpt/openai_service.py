import openai
import os


class OpenAIService:
    def __init__(self):
        self.prompt = ""
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def generate_response(self, user_input):
        self.prompt += f"{user_input}\nAI:"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": user_input}
            ]
        )
        ai_response = response.choices[0].message.content.strip()
        self.prompt += f"{ai_response}\nUser:"
        return ai_response

    def list_models(self):
        models = openai.Model.list()
        model_list = []
        for model in models["data"]:
            print(model)
            model_list.append(f"{model['id']}")
        return "\n".join(model_list)
