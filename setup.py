from setuptools import setup

setup(
    name="pyrcv",
    version="0.0.1",
    packages=["pyrcv"],

    # dependencies
    install_requires=[
        'numpy>1.14.0,<2.0.0',
        'pytest-runner',
    ],
    tests_require=[
        "pytest",
    ],

    # metadata for upload to PyPI
    author="Tobias Windisch",
    author_email="tobias.windisch@posteo.de",
    description="Python library for ranked choice voting",
    license="GNU GPL3",
    keywords="rcv votings",
    url="https://github.com/windisch/pyrcv",
)
