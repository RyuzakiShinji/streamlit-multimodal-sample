"""
Multimodal Chat Application

This Streamlit application provides a chat interface that supports text and image inputs.
It uses OpenAI's GPT models to generate responses based on the conversation history and
uploaded images. The application maintains session state to preserve chat history.

Dependencies:
    - streamlit
    - openai
    - tiktoken
    - uuid
    - datetime
    - base64
"""

import base64
import datetime
import logging
from typing import Any, Dict, List, Optional, Tuple
import uuid

import streamlit as st
from streamlit.elements.widgets.chat import ChatInputValue
from openai import OpenAI
import tiktoken
from tiktoken.core import Encoding


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "gpt-4o-mini"
MODEL_MAX_INPUT_TOKEN = 128000
TOKENIZER = tiktoken.encoding_for_model("gpt-4o")
ALLOWED_FILE_TYPES = ["jpg", "jpeg", "png"]

# Type definitions for better code clarity
ChatMessage = Dict[str, Any]
ImageData = Dict[str, str]
ContentItem = Dict[str, Any]


class OpenAIClient:
    """Handles interactions with the OpenAI API."""

    def __init__(self) -> None:
        """Initialize the OpenAI client."""
        self.client = OpenAI()

    def generate_response(self, user_message: Dict[str, Any]) -> str:
        """
        Generate a response using the OpenAI API.

        Args:
            user_message: The formatted user message to send to the API

        Returns:
            The text response from the model

        Raises:
            Exception: If there's an error communicating with the API
        """
        try:
            response = self.client.chat.completions.create(model=MODEL_NAME, messages=[user_message])
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response from OpenAI: {str(e)}")
            raise Exception(f"Failed to get response from AI model: {str(e)}")


class SessionManager:
    """Manages the application's session state and chat history."""

    @staticmethod
    def initialize_session() -> None:
        """Initialize session state variables if they don't exist."""
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

    @staticmethod
    def add_message(role: str, content: str, files: Optional[List[Any]] = None) -> None:
        """
        Add a new message to the chat history.

        Args:
            role: The role of the message sender ('user' or 'assistant')
            content: The text content of the message
            files: Optional list of uploaded files
        """
        message_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()

        chat_message: ChatMessage = {
            "id": message_id,
            "role": role,
            "content": content,
            "timestamp": timestamp,
        }

        if files:
            chat_message["uploaded_filenames"] = [file.name for file in files]

        st.session_state.chat_messages.append(chat_message)

    @staticmethod
    def get_chat_history() -> List[ChatMessage]:
        """
        Get the current chat history.

        Returns:
            List of chat messages
        """
        return st.session_state.chat_messages


class TokenManager:
    """Handles token counting and message formatting with token limits."""

    def __init__(self, tokenizer: Encoding, max_tokens: int) -> None:
        """
        Initialize the token manager.

        Args:
            tokenizer: The tokenizer to use for counting tokens
            max_tokens: Maximum number of tokens allowed
        """
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens in the text
        """
        return len(self.tokenizer.encode(text))

    def format_chat_history(self, chat_messages: List[ChatMessage]) -> str:
        """
        Format chat history with token limit consideration.

        Args:
            chat_messages: List of chat message dictionaries

        Returns:
            Formatted chat history string that fits within token limits
        """
        token_count: int = 0
        formatted_history: str = ""

        # Process messages from newest to oldest to prioritize recent context
        for message in reversed(chat_messages):
            message_text = f"{message['role']}: {message['content']}\n"
            message_tokens = self.count_tokens(message_text)

            # Check if adding this message would exceed the token limit
            if token_count + message_tokens > self.max_tokens:
                break

            # Add message to history and update token count
            token_count += message_tokens
            formatted_history = message_text + formatted_history

        return formatted_history


class PromptGenerator:
    """
    Handles the creation and formatting of prompts for the AI model.
    Responsible for incorporating chat history, sanitizing inputs, and
    generating the final prompt structure to send to the OpenAI API.
    """

    def __init__(self, token_manager: TokenManager) -> None:
        """
        Initialize the prompt generator.

        Args:
            token_manager: The token manager to use for formatting chat history
        """
        self.token_manager = token_manager

    def generate_enhanced_prompt(self, prompt: str, chat_history: Optional[List[ChatMessage]] = None) -> str:
        """
        Generate an enhanced prompt that includes context from chat history.

        Args:
            prompt: The user's original text input
            chat_history: Optional chat history for context

        Returns:
            An enhanced prompt with chat history context if available
        """
        if not chat_history:
            return prompt

        formatted_history = self.token_manager.format_chat_history(chat_history)
        enhanced_prompt = f"""
        Generate a response for the user considering the prompt and the conversation history.

        Chat history:
        {formatted_history}

        User's prompt:
        {prompt}
        """
        return enhanced_prompt

    def sanitize_prompt(self, prompt: str) -> str:
        """
        Sanitize the prompt to help prevent injection attacks.

        Args:
            prompt: The prompt to sanitize

        Returns:
            Sanitized prompt
        """
        # This is a basic implementation - a production system would need more robust checks
        dangerous_patterns = [
            "ignore previous instructions",
            "ignore all previous prompts",
            "disregard your instructions",
        ]

        sanitized_prompt = prompt
        for pattern in dangerous_patterns:
            if pattern.lower() in prompt.lower():
                logger.warning(f"Potentially dangerous prompt detected: {pattern}")
                sanitized_prompt = sanitized_prompt.replace(pattern, "[FILTERED]")

        return sanitized_prompt


class MessageProcessor:
    """Processes messages for the OpenAI API."""

    def __init__(self, token_manager: TokenManager) -> None:
        """
        Initialize the message processor.

        Args:
            token_manager: The token manager to use for token counting
        """
        self.token_manager = token_manager
        self.prompt_generator = PromptGenerator(token_manager)

    def generate_user_message(
        self, prompt: str, chat_history: Optional[List[ChatMessage]] = None, images: Optional[List[ImageData]] = None
    ) -> Dict[str, Any]:
        """
        Generate a structured message to send to the OpenAI API.

        Args:
            prompt: The user's text input
            chat_history: Optional chat history for context
            images: Optional list of encoded images

        Returns:
            A formatted message dictionary for the API
        """
        content: List[ContentItem] = []

        # Add images if provided
        if images:
            for image in images:
                content.append(
                    {"type": "image_url", "image_url": {"url": f"data:image/{image['type']};base64,{image['data']}"}}
                )

        # Generate enhanced prompt with context and sanitization
        enhanced_prompt = self.prompt_generator.generate_enhanced_prompt(prompt, chat_history)
        sanitized_prompt = self.prompt_generator.sanitize_prompt(enhanced_prompt)

        # Add text content as the first item
        content.insert(0, {"type": "text", "text": sanitized_prompt})

        return {"role": "user", "content": content}


class InputHandler:
    """Handles processing of uploaded files and user inputs."""

    @staticmethod
    def process_user_input(user_input: Any) -> Tuple[str, List[Any]]:
        """
        Process user input and extract text and files.

        Args:
            user_input: The input from Streamlit's chat_input widget

        Returns:
            Tuple of (prompt text, list of files)

        Raises:
            ValueError: If the input type is unexpected
        """
        if isinstance(user_input, str):
            return user_input, []
        elif isinstance(user_input, ChatInputValue):
            return user_input.text, user_input.files or []
        else:
            raise ValueError(f"Unexpected input type: {type(user_input)}")

    @staticmethod
    def encode_images(files: List[Any]) -> List[ImageData]:
        """
        Extract and encode images from uploaded files into base64 format.

        Args:
            files: List of uploaded files

        Returns:
            List of dictionaries with image type and base64-encoded data

        Note:
            If an error occurs while processing a file, the error is logged
            but the function continues processing remaining files.
        """
        if not files:
            return []

        image_data = []
        for file in files:
            try:
                encoded_data = base64.b64encode(file.read()).decode("utf-8")
                file_type = file.type.split("/")[-1]  # Extract format from MIME type
                image_data.append({"type": file_type, "data": encoded_data})
            except Exception as e:
                logger.error(f"Error processing file {file.name}: {str(e)}")
                # Continue processing other files even if one fails

        return image_data


class ChatUI:
    """Manages the Streamlit UI components for the chat application."""

    def __init__(self) -> None:
        """Initialize the UI components and dependencies."""
        self.openai_client = OpenAIClient()
        token_manager = TokenManager(TOKENIZER, MODEL_MAX_INPUT_TOKEN)
        self.message_processor = MessageProcessor(token_manager)
        self.file_handler = InputHandler()

    def setup_page(self) -> None:
        """Set up the page configuration and title."""
        st.set_page_config(page_title="Multimodal Chat Application", page_icon="💬", layout="centered")
        st.title("Multimodal Chat Application")
        st.subheader("Chat with AI using text and images")

    def display_chat_history(self) -> None:
        """Display the current chat history."""
        for message in SessionManager.get_chat_history():
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                # Display attached files if present
                if message["role"] == "user" and message.get("uploaded_filenames"):
                    with st.expander("Attached Files", expanded=False):
                        for filename in message["uploaded_filenames"]:
                            st.caption(filename)

    def handle_user_input(self) -> None:
        """Process user input and generate responses."""
        user_input = st.chat_input(
            "Type your message here...",
            accept_file="multiple",
            file_type=ALLOWED_FILE_TYPES,
        )

        if not user_input:
            return

        try:
            # Process the user input
            prompt, files = self.file_handler.process_user_input(user_input)

            # Extract and encode images
            images = self.file_handler.encode_images(files)

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
                if files:
                    with st.expander("Attached Files", expanded=False):
                        for file in files:
                            st.caption(file.name)

            # Generate and display AI response
            with st.spinner("Generating response..."):
                try:
                    # Prepare message for the API
                    user_message = self.message_processor.generate_user_message(
                        prompt, SessionManager.get_chat_history(), images
                    )

                    # Get response from OpenAI
                    response_text = self.openai_client.generate_response(user_message)

                    # Display the response
                    with st.chat_message("assistant"):
                        st.markdown(response_text)

                    # Update chat history
                    SessionManager.add_message("user", prompt, files)
                    SessionManager.add_message("assistant", response_text)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    logger.error(f"Error in AI response generation: {str(e)}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"Error in input processing: {str(e)}")


def main() -> None:
    """
    Main application entry point.
    Sets up the UI and handles the application flow.
    """
    try:
        # Initialize session state
        SessionManager.initialize_session()

        # Set up and run the chat UI
        chat_ui = ChatUI()
        chat_ui.setup_page()
        chat_ui.display_chat_history()
        chat_ui.handle_user_input()

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.critical(f"Critical application error: {str(e)}")


if __name__ == "__main__":
    main()
