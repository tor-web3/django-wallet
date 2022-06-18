#!/usr/bin/env python

from tabulate import tabulate

try:
    from hdwallet.cli import click
except ImportError:
    from wallet.hdwallet.cli import click


def list_languages():

    click.echo(tabulate(
        [
            ["Chinese Simplified"],
            ["Chinese Traditional"],
            ["English"],
            ["French"],
            ["Italian"],
            ["Japanese"],
            ["Korean"],
            ["Spanish"],
        ],
        [
            "Language"
        ],
        tablefmt="github"
    ))
