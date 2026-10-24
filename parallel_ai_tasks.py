
import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from document_tool_demo import MODEL_NAME


def generate_explanation(client: genai.Client, notes: str) -> str:
    response = client.interactions.create(
        model=MODEL_NAME,
        input=(
            "Explain the following study notes in simple, "
            "beginner-friendly language.\n\n"
            f"Study notes:\n{notes}"
        ),
    )

    result = response.output_text
    if not result:
        raise ValueError("The model returned an empty explanation.")

    return result


def generate_questions(client: genai.Client, notes: str) -> str:
    response = client.interactions.create(
        model=MODEL_NAME,
        input=(
            "Create three study questions based on the following notes. "
            "Do not provide the answers. Use beginner-friendly language."
            f"\n\nStudy notes:\n{notes}"
        ),
    )

    result = response.output_text
    if not result:
        raise ValueError("The model returned empty questions.")

    return result


def run_parallel_tasks(client: genai.Client, notes: str) -> tuple[str, str]:
    with ThreadPoolExecutor(max_workers=2) as executor:
        explanation_future = executor.submit(
            generate_explanation, client, notes
        )
        questions_future = executor.submit(
            generate_questions, client, notes
        )

        explanation = explanation_future.result()
        questions = questions_future.result()

    return explanation, questions


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY is missing from your .env file.")
        return

    notes = input("Enter study notes or a topic: ").strip()

    if not notes:
        print("Please enter some study notes or a topic.")
        return

    try:
        client = genai.Client(api_key=api_key)
        explanation, questions = run_parallel_tasks(client, notes)

        print("\n--- Explanation ---")
        print(explanation)

        print("\n--- Study Questions ---")
        print(questions)

    except ValueError as error:
        print(f"Could not complete the task: {error}")

    except errors.APIError as error:
        print(f"Gemini request failed: {type(error).__name__}")
        print("Check your API key, model access, and quota.")

    except (TimeoutError, ConnectionError) as error:
        print(f"Network request failed: {type(error).__name__}")
        print("Check your internet connection and try again.")


if __name__ == "__main__":
    main()
