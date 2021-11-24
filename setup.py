from setuptools import setup

setup(
    name="chatwars-api",
    version="1!2021.11.24b0",
    description="Client for Chat Wars API for Python3",
    author="Andrew Golovashevich",
    url="https://LandgrafHomyak.github.io/cwapi-python/",
    download_url="https://github.com/LandgrafHomyak/cwapi-python/releases/tag/v1!2021.11.24b0",
    packages=["cwapi"],
    python_requires=">=3.8, <3.12",
    install_requires=[
        "pika",
        "aio-pika",
    ],
    package_data={
        "cwapi": ["py.typed", "*.pyi"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Software Development",
        "Typing :: Typed"
    ],
    license="",
    license_files=["LICENSE"],

)
