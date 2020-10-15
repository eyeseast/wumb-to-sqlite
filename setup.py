from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
    ) as fp:
        return fp.read()


setup(
    name="wumb-to-sqlite",
    description="Scrape WUMB playlists to SQLite",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Chris Amico",
    url="https://github.com/eyeseast/wumb-to-sqlite",
    project_urls={
        "Issues": "https://github.com/eyeseast/wumb-to-sqlite/issues",
        "CI": "https://github.com/eyeseast/wumb-to-sqlite/actions",
        "Changelog": "https://github.com/eyeseast/wumb-to-sqlite/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["wumb_to_sqlite"],
    entry_points="""
        [console_scripts]
        wumb-to-sqlite=wumb_to_sqlite.cli:cli
    """,
    install_requires=["click", "beautifulsoup4", "httpx", "pytz", "sqlite-utils"],
    extras_require={"test": ["pytest"]},
    tests_require=["wumb-to-sqlite[test]"],
)
