# Development Information

## Running the test cases
From the project directory run:
```shell
pytest
```
This will run all the test cases

## Core Requirements
+ `pip install bert-extractive-summarizer`
+ `pip install beautifulsoup4`
+ `pip install torch`
+ `pip install Markdown`
+ `pip install html5lib`
+ `pip install -U pytest`

## Setting up packaging
1. Setup the packaging system: `pip install setuptools1
2. Configure the `setup.py` file in the project directory.
3. Building and installing your package:
    - To build: `python setup.py sdist bdist_wheel`
    - To install: `pip install dist/markybrief-0.1.0.tar.gz` or `pip install dist/markybrief-0.1.0.whl`
