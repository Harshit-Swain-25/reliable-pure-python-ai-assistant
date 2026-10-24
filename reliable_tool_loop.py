import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from document_tool_demo import (
    ALLOWED_DOCUMENTS,
    MODEL_NAME,
    READ_DOCUMENT_TOOL,
    read_document,
)

MAX_TOOL_CALLS = 3


def can_execute_tool_call(tool_calls_executed: int) -> bool:
    return tool_calls_executed < MAX_TOOL_CALLS


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
                "You are a document assistant. "
                "Use the read_document tool when the user asks about an approved document. Base document-specific answers on the returned content. Never invent document facts."
                "If a tool returns an error, explain it clearly. "
                "Do not request unnecessary repeated tool calls.\n\n"
                f"User request: {user_request}"
            ),
            tools=[READ_DOCUMENT_TOOL],
        )

        tool_calls_executed = 0

        while True:
            function_calls = [
                step for step in interaction.steps if step.type == "function_call"
            ]

            if not function_calls:
                print("\nGemini Response:\n")
                print(interaction.output_text or "No text response was returned.")
                return

            function_results = []

            for function_call in function_calls:
                if not can_execute_tool_call(tool_calls_executed):
                    print("\nTool-call limit reached. Please try a simpler request.")
                    return

                tool_calls_executed += 1

                if function_call.name != "read_document":
                    print("Error: Gemini requested an unsupported tool.")
                    return

                arguments = function_call.arguments

                if not isinstance(arguments, dict):
                    tool_result = {"error": "The tool arguments must be an object."}
                else:
                    document_name = arguments.get("document_name")

                    if (
                        not isinstance(document_name, str)
                        or document_name not in ALLOWED_DOCUMENTS
                    ):
                        tool_result = {
                            "error": ("The requested document name is not approved.")
                        }
                    else:
                        tool_result = read_document(document_name)

                print(f"\nTool call: {tool_calls_executed}")
                print(f"Tool name: {function_call.name}")
                print(f"Arguments: {arguments}")
                print(f"Tool result: {tool_result}")

                function_results.append(
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
                )

            interaction = client.interactions.create(
                model=MODEL_NAME,
                previous_interaction_id=interaction.id,
                tools=[READ_DOCUMENT_TOOL],
                input=function_results,
            )

    except errors.APIError as error:
        print(f"Gemini request failed: {type(error).__name__}")
        print("Check your API key, model access, and quota.")
    except (TimeoutError, ConnectionError) as error:
        print(f"Network request failed: {type(error).__name__}")
        print("Check your internet connection and try again.")


if __name__ == "__main__":
    main()
