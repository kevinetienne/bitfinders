from distutils.core import setup

version = "0.1alpha"

setup(
    name = "bitfinders",
    description = "Access bitcoin* api to display data",
    version = version,
    packages = ['bitfinders',],
    long_description = open('README').read(),
)
