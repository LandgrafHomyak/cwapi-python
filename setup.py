from setuptools import setup

setup(
    name="chatwars-api",
    version="0.0a0",
    packages=["cwapi"],
    install_requires=[
        "pika",
    ],
    package_data={
        "cwapi": ["py.typed", "*.pyi"],
    }
)
