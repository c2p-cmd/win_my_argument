# Win My Argument

A debate simulation tool that generates political arguments from different political viewpoints on any given topic.

## Description

Win My Argument is a Python application that simulates political debates between left-wing and right-wing perspectives. It uses the Gemini AI model to generate responses that mimic the thinking of political figures from different countries.

The application:

1. Takes a debate topic as input
2. Generates responses from both right-wing and left-wing perspectives
3. Uses DuckDuckGo search to gather relevant information for each perspective
4. Presents the debate results with arguments from each side

## Installation

```bash
# Clone the repository
git clone https://github.com/c2p-cmd/win_my_argument.git
cd win_my_argument

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the application from the command line with a debate topic:

```bash
python -m app.main --query "Should we increase the minimum wage?"
```

The application will return arguments from both perspectives, attributed to current political figures (defaults to US political figures).

## Configuration

The application defaults to US political figures, but can be configured for other countries by modifying the `__country` variable in model.py.

Currently supported countries:
- US (Donald Trump vs Joe Biden)
- DE (Alice Weidel vs Olaf Scholz)
- IN (BJP vs INC)

## Project Structure

- main.py - Entry point for the application
- model.py - Core data models and system prompts
- agents.py - AI agent configuration for different political perspectives
- service.py - Main service for coordinating the debate

## Requirements

The application requires Python 3.8+ and uses the following key dependencies:
- pydantic-ai - For agent-based AI workflows
- duckduckgo_search - For retrieving relevant information
- Google's Gemini AI model get your api key (here)[https://aistudio.google.com/] and create a `.env` see (`.env.example`)[.env.example]