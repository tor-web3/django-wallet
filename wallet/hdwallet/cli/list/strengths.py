#!/usr/bin/env python

from tabulate import tabulate

try:
    from hdwallet.cli import click
except ImportError:
    from wallet.hdwallet.cli import click


def list_strengths():

    click.echo(tabulate(
        [
            [128, 12],
            [160, 15],
            [192, 18],
            [224, 21],
            [256, 24],
        ],
        [
            "Strength",
            "Words"
        ],
        tablefmt="github"
    ))
