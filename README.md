<p align="center">  
  <img src="docs/images/beegen.png" alt="BeeGen">  
</p>
<p align="center">
    <em>BeeGen is an intelligent command-line tool designed to assist developers with everyday tasks, leveraging the power of generative AI.</em>
</p>
<p align="center">
    <a href="https://github.com/psf/black"><img alt="Code Style Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://pycqa.github.io/isort/"><img alt="Imports Isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
    <a href="https://github.com/PyCQA/bandit"><img alt="Security Bandit" src="https://img.shields.io/badge/security-bandit-yellow.svg"></a>
    
</p>

## BeeGen

With Beegen, you can streamline your development process, improve code quality, and automate various aspects of project creation and management.

## Features

- **Mock APIs:** Quickly create and run mock API servers.
- **Sensitive Data Anonymization:** Use generative AI to mask identifiable information and ensure privacy.
- **Vector Store Generation:** Create a local vector store using FAISS for projects that require semantic search.
- **README Generator:** Automatically generate a detailed README file for your projects.
- **Translation:** Quickly translate text between different languages.
- **Code Snippets:** Add, list, remove, and use code snippets directly from the command line.
- **AI Chat Interface:** Interact with language models in a terminal-based chat.

## Installation

You can install BeeGen in two ways:

[PyPI](https://pypi.org/project/beegen/)

```bash
pip install beegen
```

Directly from the repository using [poetry](https://python-poetry.org/)

```bash
poetry install
```

## Usage

Here are a few examples of how you can use BeeGen for daily tasks:

### Configure

Configure the LLM and access keys for usage.

```bash
beegen configure
```

![](docs/images/commands/configure.gif)

### Full List of Commands

To view the complete list of available commands, run:

```bash
beegen list
```

