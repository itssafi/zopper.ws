"""Main entry point
"""
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("zopper.ws.restful_services.views")
    config.scan("zopper.ws.restful_services.renderer")
    return config.make_wsgi_app()
