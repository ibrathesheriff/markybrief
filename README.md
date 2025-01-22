# markybrief
A lightweight Python tool for generating concise summaries of markdown files. Perfect for developers and teams to quickly grasp the essence of documentation.

## Features
+ 📝 Summarizes markdown files into brief, digestible insights.
+ ⚡ Fast and lightweight.
+ 🔧 Easy to integrate into existing workflows.
+ 📂 Supports batch processing of multiple markdown files.

## Installation

### Plug-and-play
TBC

### Intend to extend or contribute
TBC

## Usage

### Basic Usage
Create a markdown summary:
```python

from markybrief.briefer import Briefer

briefer = Briefer()

# Path to your markdown file
file_path = "example_docs/example1.md"

output = briefer.brief(file_path)

print(output)
```

Create a HTML summary:
```python

from markybrief.briefer import Briefer

briefer = Briefer()

# Path to your markdown file
file_path = "example_docs/example1.md"

output = briefer.brief(file_path, "html")

print(output)
```

## Build the package
To build the MarkyBrief package run:
```shell
python setup.py sdist bdist_wheel
```

## License
MarkyBrief is licensed under the [MIT License](https://mit-license.org/).

## Feedback and Support
If you encounter any issues or have suggestions, please open an issue or reach out on the Discussions tab.

## TODO
+ [] Add Batch Processing so that Users can summarise multiple files.
+ [] Add command-line support.
+ [] Update configuration to allows things like ignoring sections.
+ [] Add styling to HTML summarises
+ [] Add code highlighting to HTML summarises
+ [] Add an overview section to the HTML output like a table of contents. Users can use this to navigate to certain content sections in the summary.