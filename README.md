# LangChain Agent Interface

A powerful interface that combines LangChain, MCP (Model Control Protocol), and Gradio to create an interactive agent system.

## Features

- Interactive Gradio-based web interface
- Integration with LangChain for agent creation
- Uses Groq's Llama 3.1 8B model for responses
- MCP (Model Control Protocol) integration for enhanced capabilities
- Asynchronous operation for better performance

## Prerequisites

- Python 3.x
- Required Python packages (install via pip):
  - gradio
  - langchain-groq
  - langchain-mcp-adapters
  - langgraph
  - python-dotenv

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your Groq API key:
   ```
   GITHUB_TOKEN=your_api_Key_here
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python client.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (typically http://127.0.0.1:7860)
3. Enter your prompt in the text box and click "Run Agent"

## Project Structure

- `client.py`: Main application file containing the Gradio interface and agent setup
- `pr_analyzer.py`: MCP script for handling agent operations

## Note

This project uses the Groq API with the Llama 3.1 8B model. Make sure you have valid API credentials before running the application.
