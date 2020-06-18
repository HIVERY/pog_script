from src.templete.psa import PSAInterface
import click


@click.command()
@click.option(
    "--path",
    "-p",
    help="The path to psa file.",
    required=True
)
def extract(path):
    psa = PSAInterface()
    psa.read_psa(path)
    print(psa)
