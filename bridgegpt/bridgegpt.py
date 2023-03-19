import click

from bridgegpt.system_service import SystemService
from .openai_service import OpenAIService
import os


openai_service = OpenAIService()
system_service = SystemService()

# Get the absolute path to the directory containing this file
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load the base prompt from a file in the same directory
with open(os.path.join(dir_path, "base_prompt.txt"), "r") as f:
    base_prompt = f.read()

@click.group()
def bridgegpt():
    pass


@bridgegpt.command()
def chat():
    context = base_prompt.strip()
    openai_service.prompt = f"Conversation:\nUser: {context}\nAI:"

    while True:
        user_input = click.prompt("\nYou")
        ai_response = openai_service.generate_response(user_input)

        if system_service.is_valid_json(ai_response):
            click.echo(f"\nAI (hidden): {ai_response}")
            bridgegpt_response = system_service.process_json(ai_response)
            click.echo(f"BridgeGPT (hidden): {bridgegpt_response}")
            ai_response = openai_service.generate_response(bridgegpt_response)

        click.echo(f"\nAI: {ai_response}")
        if ai_response.endswith("Goodbye!"):
            break


@bridgegpt.command()
def list_models():
    models = openai_service.list_models()
    click.echo_via_pager(models)


if __name__ == "__main__":
    bridgegpt()