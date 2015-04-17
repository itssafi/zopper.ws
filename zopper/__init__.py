"""
Initialization
"""
try:
    # try using setuptools namespace package
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    # fall back on old style namespace package
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
