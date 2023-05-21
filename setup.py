import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyanimeclick",
    version="2.1",
    author="stefanodvx",
    author_email="pp.stefanodvx@gmail.com",
    description="Async API wrapper for AnimeClick.it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefanodvx/pyanimeclick",
    project_urls={
        "Tracker": "https://github.com/stefanodvx/pyanimeclick/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "httpx",
        "pydantic",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)