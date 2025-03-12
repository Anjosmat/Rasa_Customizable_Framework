#!/usr/bin/env python
import click
from admin.cli import admin_cli


@click.group()
def cli():
    """Management script for the Rasa Customizable Framework"""
    pass


# Add the admin commands to the main CLI
cli.add_command(admin_cli)

if __name__ == '__main__':
    cli()
