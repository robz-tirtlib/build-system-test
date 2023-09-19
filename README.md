# Build system

Build system is capable of:
- circular dependencies detection
- topological sorting of dependencies
- interacting with data via CLI

# Installation

Create and activate virtual environment
```
py -m venv .venv
```
On Windows:
```
.venv\Scripts\activate
```
On Linux:
```
. .venv/bin/activate
```
Install necessary dependencies
```
pip install -r requirements.txt
```

# Usage

General look of interaction:
```
main.py (command) (arguments) [optionals]
```

Example:
```
main.py list tasks -t path/to/tasks.yaml -b path/to/builds.yaml
```

Detailed description of commands can be seen by:
```
main.py -h
```

# Testing

Tests are invoked this way:
```
pytest
```
