""" CLI version """

import click
import uvicorn # type: ignore

@click.command()
@click.option("--reload", is_flag=True)
@click.option("--port", type=int)
@click.option("--host", type=str)
@click.option("--proxy-headers", is_flag=True)
def cli(
    reload: bool=False,
    port: int=8000,
    host: str="0.0.0.0",
    proxy_headers: bool=False,
    ):
    """ sprintf server """
    uvicorn.run(
        app="sprintf:app",
        reload=reload,
        host=host,
        port=port,
        proxy_headers=proxy_headers,
        )

if __name__ == '__main__':
    cli()
