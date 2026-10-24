import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors

MODEL_NAME = "gemini-3.8-flash"
DATA_DIRECTORY = Path(__file__).parent / "data"

ALLOWED_DOCUMENTS = {"ai_agent_notes.txt", "project_brief.txt"}

READ_DOCUMENT_TOOL = {
    "type": "function",
    "name": "read_document",
    "description": (
        "Reads an approved local text document and returns its contents. "
        "Use this tool when the user asks about information inside the document."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "document_name": {
                "type": "string",
                "enum": sorted(ALLOWED_DOCUMENTS),
                "description": ("The exact name of an approved document to read."),
            },
        },
        "required": ["document_name"],
    },
}


def read_document(document_name: str) -> dict[str, str]:
    if not isinstance(document_name, str):
        return "Error: The document must be in .txt format"

    if document_name not in ALLOWED_DOCUMENTS:
        return {"error": "The document is not present in data folder."}

    document_path = DATA_DIRECTORY / document_name

    try:
        content = document_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {"error": "Requested document does not exist."}
    except OSError:
        return "Error: The document could not be read."

    if not content.strip():
        return {"error": "Requested document cannot be empty."}

    return {
        "document_name": document_name,
        "content": content,
    }


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: your GEMINI_API_KEY is missing in your .env file")
        return

    user_request = input("What would you like to know about sample document?").strip()

    if not user_request:
        print("Please enter a question before continuing.")

    try:
        client = genai.Client(api_key=api_key)
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=(
                "You are a document assistant."
                "Use the read_document tool when the user asks about the contents of an approved document. "
                "Do not claim to have read a document unless the tool returns its contents. Base document-specific answers on the returned content. If the tool returns an error,  explain the problem clearly. Do not invent document facts.\n\n"
                f"User request: {user_request}"
            ),
            tools=[READ_DOCUMENT_TOOL],
        )

        function_call = next(
            (step for step in interaction.steps if step.type == "function_call"),
            None,
        )

        if function_call is None:
            print("\nGemini Response:\n")
            print(interaction.output_text or "No text response was returned.")
            return

        if function_call.name != "read_document":
            print("Error: Gemini requested an unsupported tool.")
            return

        arguments = function_call.arguments

        if not isinstance(arguments, dict):
            print("Error: The tool arguments were invalid.")
            return

        document_name = arguments.get("document_name")

        if not isinstance(document_name, str) or document_name not in ALLOWED_DOCUMENTS:
            print("Error: The requested document name failed validation.")
            return

        tool_result = read_document(document_name)

        print(f"\nTool called: {function_call.name}")
        print(f"Arguments: {arguments}")

        if "error" in tool_result:
            print(f"Tool result: {tool_result['error']}")
        else:
            print(f"Document read: {tool_result['document_name']}")

        final_interaction = client.interactions.create(
            model=MODEL_NAME,
            previous_interaction_id=interaction.id,
            tools=[READ_DOCUMENT_TOOL],
            input=[
                {
                    "type": "function_result",
                    "name": function_call.name,
                    "call_id": function_call.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(tool_result),
                        }
                    ],
                }
            ],
        )

        print("\nGemini Response:\n")
        print(final_interaction.output_text or "No final text response was returned.")

    except errors.APIError as error:
        print(f"Gemini request failed: {type(error).__name__}")
        print("Check your API key, model access, and quota.")
    except (TimeoutError, ConnectionError) as error:
        print(f"Network request failed: {type(error).__name__}")
        print("Check your internet connection and try again.")


if __name__ == "__main__":
    main()
