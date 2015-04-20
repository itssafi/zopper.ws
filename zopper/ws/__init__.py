"""
Main entry point
"""
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("zopper.ws.views")
    config.scan("zopper.ws.renderer")
    return config.make_wsgi_app()
