
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from conversation_session import ConversationSession
from document_tool_demo import MODEL_NAME


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: your GEMINI_API_KEY is missing in your .env file.")
        return

    client = genai.Client(api_key=api_key)
    session = ConversationSession()
   
    print("Conversation Memory Demo")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "exit":
            print("Conversation ended.")
            break

        if not user_message:
            print("Please enter a message.")
            continue

        try:
            interaction = client.interactions.create(
                model=MODEL_NAME,
                input=user_message,
                previous_interaction_id=session.previous_interaction_id,
            )

            assistant_message = (
                interaction.output_text or "No text response was returned."
            )
            print(f"\nAssistant: {assistant_message}\n")
            session.update(interaction.id)

        except errors.APIError as error:
            print(f"Gemini request failed: {type(error).__name__}")
            print("Check your API key, model access, and quota.")

        except (TimeoutError, ConnectionError) as error:
            print(f"Network request failed: {type(error).__name__}")
            print("Check your internet connection and try again.")


if __name__ == "__main__":
    main()
