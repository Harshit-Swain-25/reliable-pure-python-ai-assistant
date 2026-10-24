
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from document_tool_demo import MODEL_NAME


def generate_summary(client: genai.Client, study_notes: str) -> str:
    response = client.interactions.create(
        model = MODEL_NAME,
        input = (
            "Summarize the following study notes in 5 clear bullet points."
            "Use beginner-friendly language.\n\n"
            f"Study notes:\n{study_notes}"
        ),
    )

    summary = response.output_text
    if not summary:
        raise ValueError("The model returned an empty summary")
    return summary

def build_questions_prompt(summary: str) -> str:
    return (
        "Create 3 study questions based only on the summary below. "
        "Do not provide the answers. Use clear, beginner-friendly language."
        f"\n\nSummary:\n{summary}"
    )

def generate_questions(client: genai.Client, summary: str) -> str:
    response = client.interactions.create(
        model = MODEL_NAME,
        input=build_questions_prompt(summary),
    )

    questions = response.output_text
    if not questions:
        raise ValueError("The model returned an empty questions")
    return questions


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: your GEMINI_API_KEY is missing in your .env file.")
        return

    client = genai.Client(api_key=api_key)
    study_notes = input("Enter your study notes or topic: ").strip()

    if not study_notes:
        print("Please enter some study notes or a topic.")
        return

    try:
        summary = generate_summary(client, study_notes)
        print("\n--- Summary ---")
        print(summary)

        questions = generate_questions(client, summary)
        print("\n--- Study Questions ---")
        print(questions)

    except ValueError as error:
        print(f"Could not complete the task: {error}")
    
    except errors.APIError as error:
        if getattr(error, "code", None) == 503:
            print("Gemini is temporarily unavailable or busy.")
            print("Please try again later.")
        else:
            print(f"Gemini request failed: {type(error).__name__}")
            print("Check your API key, model access, and quota.")

    except (TimeoutError, ConnectionError) as error:
        print(f"Network request failed: {type(error).__name__}")
        print("Check your internet connection and try again.")


if __name__ == "__main__":
    main()
