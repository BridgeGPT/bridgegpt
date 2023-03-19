import click

from bridgegpt.vo_service import VOService


vo_service = VOService.instance()


@click.group()
def bridgegpt():
    pass


@bridgegpt.command()
@click.option('--debug', default=False, is_flag=True)
def chat(debug):
    click.echo('Starting BridgeGPT...\n')
    click.echo(vo_service.initialize())
    while True:
        user_input = click.prompt("\nYou")
        ai_response = vo_service.handle_input(user_input)
        click.echo(f"\nAI: {ai_response}")
        if ai_response.endswith("Goodbye!"):
            break


if __name__ == "__main__":
    bridgegpt()
