
import os
from collections.abc import Callable

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from document_tool_demo import MODEL_NAME

ROUTE_INSTRUCTIONS = {
    "explanation": (
        "You are a helpful AI tutor. Explain the user's topic in simple, "
        "beginner-friendly language. Use a short example when useful."
    ),
    "summary": (
        "You are a study assistant. Summarize the user's supplied notes "
        "clearly, focusing on the most important ideas. If no notes are "
        "provided, ask the user to supply them."
    ),
    "questions": (
        "You are a study assistant. Create three useful study questions "
        "based on the user's topic or supplied notes. Do not provide "
        "the answers unless the user asks for them."
    ),
}


def classify_request(request: str) -> str:
    cleaned_request = request.strip().lower()

    if not cleaned_request:
        raise ValueError("Request cannot be empty.")

    if "question" in cleaned_request or "quiz" in cleaned_request:
        return "questions"

    if "summarize" in cleaned_request or "summary" in cleaned_request:
        return "summary"

    if "explain" in cleaned_request:
        return "explanation"

    return "unknown"


def run_gemini(
    request: str,
    route: str,
    client: genai.Client,
) -> str:
    instructions = ROUTE_INSTRUCTIONS[route]

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=f"{instructions}\n\nUser request: {request}",
    )

    return interaction.output_text or "Gemini returned no text response."


def explain_request(request: str, client: genai.Client) -> str:
    return run_gemini(request, "explanation", client)


def summarize_request(request: str, client: genai.Client) -> str:
    return run_gemini(request, "summary", client)


def generate_questions(request: str, client: genai.Client) -> str:
    return run_gemini(request, "questions", client)


def dispatch_request(request: str, client: genai.Client) -> str:
    route = classify_request(request)

    handlers: dict[str, Callable[[str, genai.Client], str]] = {
        "explanation": explain_request,
        "summary": summarize_request,
        "questions": generate_questions,
    }

    handler = handlers.get(route)

    if handler is None:
        return "Sorry, this request type is not supported yet."

    return handler(request, client)


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY is missing from your .env file.")
        return

    request = input("What would you like help with? ").strip()

    try:
        client = genai.Client(api_key=api_key)
        result = dispatch_request(request, client)
        print(f"\nResponse:\n{result}")

    except ValueError as error:
        print(f"Input error: {error}")
    except errors.APIError as error:
        print(f"Gemini request failed: {type(error).__name__}")
        print("Check your API key, model access, and quota.")
    except (TimeoutError, ConnectionError) as error:
        print(f"Network request failed: {type(error).__name__}")
        print("Check your internet connection and try again.")


if __name__ == "__main__":
    main()
