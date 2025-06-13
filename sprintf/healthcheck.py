import sys
import requests
import click

@click.command()
@click.option("--host", default="localhost", help="Host to query the server on")
@click.option("--port", default=8000, help="Port to query the server on")
def main(host, port):
    url = f"http://{host}:{port}/up"
    try:
        resp = requests.get(url, timeout=1)
        resp.raise_for_status()
        if resp.status_code == 200:
            click.echo("Healthcheck passed.")
            sys.exit(0)
        else:
            click.echo(f"Healthcheck failed: status {resp.status_code}")
            sys.exit(1)
    except Exception as e:
        click.echo(f"Healthcheck error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
