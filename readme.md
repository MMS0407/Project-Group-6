# Project Overview

## How to Start the Code

### Installation

First, ensure you have Python installed on your system. Then install the necessary package by running:

```bash
pip install rich==13.9.4
```

### Running the Application

After installing the required packages, start the application with the following command:

```bash
python3 -m main.py
```

This will launch the CLI where you can interact with the banking system. The CLI provides clear instructions on how to navigate and use the program.

## How We Created the Code

This section details the architectural decisions, selection of libraries, and construction of the project's components.

### Architecture

-   **Modular Design**: The code is organized into separate modules corresponding to each major component such as accounts, transactions, and the banking CLI.
-   **External Libraries**: We utilized `rich` for its capabilities in creating enhanced CLI experiences, providing an engaging and interactive user interface.

## How We Did Testing

Testing was a critical part of our development process, ensuring the reliability and functionality of the application through various methods.

### Unit Testing

We have developed comprehensive unit tests for each component.

-   Run tests with:

```bash
python3 -m coverage run -m unittest discover -s . -p '*_test.py'
```

### Integration Testing

Integration tests were developed to ensure that different parts of the application work together seamlessly.

### Coverage Reporting

To view the test coverage report, run:

-   `python3 -m coverage report`
    This command helps identify any parts of the codebase that may need additional testing to ensure comprehensive coverage.