from setuptools import setup

setup(
    name="chatwars-api",
    version="0.0a0",
    packages=["cwapi", "cwapi.types"],
    install_requires=[
        "pika",
    ],
    package_data={
        "cwapi": ["py.typed", "*.pyi"],
        "cwapi.types": ["py.typed", "*.pyi"],
    }
)
