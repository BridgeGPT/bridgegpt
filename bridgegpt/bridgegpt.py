import asyncio

import click

from bridgegpt.ui_service import UIService
from bridgegpt.vo_service import VOService
from typing import NoReturn


@click.group()
def bridgegpt():
    ...


@bridgegpt.command()
@click.option('--debug', default=False, is_flag=True)
def gui(debug: bool) -> NoReturn:
    """
    Run the visual TKInter GUI
    """
    vo_service = VOService.instance()
    ui_service = UIService(vo_service)
    asyncio.run(ui_service.exec())


@bridgegpt.command()
@click.option('--debug', default=False, is_flag=True)
def chat(debug: bool) -> NoReturn:
    """
    Command line tool to chat
    """
    vo_service = VOService.instance()
    vo_service.set_dialog_print(click.echo)
    if debug:
        vo_service.set_gptbridge_print(click.echo)

    click.echo('Starting BridgeGPT...\n')
    click.echo(vo_service.initialize())
    while True:
        user_input = click.prompt("\nYou")
        ai_response = vo_service.handle_input(user_input)
        click.echo(f"\nAI: {ai_response}")

        if ai_response.endswith("Goodbye!"):
            break
