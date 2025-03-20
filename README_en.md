# Streamlit Multimodal Chat Application

*[English](README_en.md) | [日本語](README.md)*

A sample application demonstrating Streamlit's `chat_input()` functionality with multimodal capabilities. This repository serves as a reference for a technical blog post about Streamlit's enhanced chat interface features.

## Overview

This application showcases a modern chat interface built with Streamlit that supports both text and image inputs. It leverages OpenAI's GPT models to generate responses based on the conversation history and uploaded images.

The main focus is on demonstrating Streamlit's `chat_input()` function which was recently updated to support file uploads directly in the chat interface, enabling a more seamless multimodal experience.

## Features

- **Multimodal Chat Interface**: Accept both text and image inputs through a single chat input field
- **Image Upload Support**: Directly upload images via the chat interface
- **Conversation History**: Maintain and display chat history in a conversational UI
- **OpenAI Integration**: Use OpenAI's models to generate contextual responses
- **Token Management**: Track and manage token usage to stay within model limits
- **Session Management**: Preserve chat state between interactions

## Installation

This project uses Poetry for dependency management. To get started:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/streamlit-multimodal-sample.git
   cd streamlit-multimodal-sample
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. The application will be available at `http://localhost:8501`

3. Type your messages in the chat input at the bottom of the page

4. To upload images, click the file upload button next to the chat input and select an image file (supported formats: jpg, jpeg, png)

## Configuration

- Maximum upload size is configured to 5MB in `.streamlit/config.toml`
- The application uses the `gpt-4o-mini` model by default, which can be modified in the code

## Key Components

- `OpenAIClient`: Handles interactions with the OpenAI API
- `SessionManager`: Manages the application's session state and chat history
- `TokenManager`: Handles token counting and message formatting with token limits
- `MessageProcessor`: Processes messages for the OpenAI API
- `InputHandler`: Processes user inputs including file uploads
- `ChatUI`: Manages the Streamlit UI components

## Requirements

- Python 3.12+
- Streamlit 1.43.2+
- OpenAI API access
- Other dependencies as specified in pyproject.toml

## Adding an OpenAI API key

To use this application, you'll need to provide your OpenAI API key. This can be done by:

1. Creating a `.env` file in the root directory
2. Adding your API key: `OPENAI_API_KEY=your_api_key_here`

## Technologies Used

- [Streamlit](https://streamlit.io/): For the web interface
- [OpenAI API](https://openai.com/): For text generation
- [tiktoken](https://github.com/openai/tiktoken): For tokenization
- [Poetry](https://python-poetry.org/): For dependency management

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 RyuzakiShinji

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

*This repository is intended as a reference for a technical blog post and not for active contribution.*
