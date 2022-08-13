import json

import click
import requests


@click.group()
def files():
    ...


@click.command()
@click.argument("name")
@click.argument("content")
@click.option("--delimiter", "-d", default=",", help='delimiter charater (default ",")')
@click.option("--quote-char", "-q", default="", help='quote character (default "")')
def post(name, content, delimiter, quote_char):
    request_headers = {
        "Content-Type": "text/csv",
        "X-Filename": name,
        "X-Delimiter": delimiter,
        "X-Quotechar": quote_char,
    }

    response = requests.post(
        "http://localhost:8000/api/csv_files/",
        data=content,
        headers=request_headers,
    )
    if response.status_code == 201:
        click.echo(json.dumps(response.json(), indent=2))
    else:
        raise RuntimeError(
            f"Error posting csv file. status_code={response.status_code}, content={response.content}"
        )


files.add_command(post)


@click.group()
def cli():
    ...


cli.add_command(files)


if __name__ == "__main__":
    cli()
