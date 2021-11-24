from setuptools import setup

setup(
    name="chatwars-api",
    version="1!2021.11.24b0",
    packages=["cwapi"],
    install_requires=[
        "pika",
        "aio-pika",
    ],
    package_data={
        "cwapi": ["py.typed", "*.pyi"],
    }
)
