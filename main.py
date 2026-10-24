import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from pydantic import BaseModel, Field, ValidationError

MODEL_NAME = "gemini-3.8-flash"


class RequestAnalysis(BaseModel):
    topic: str = Field(description="Main topic of the User's request.")
    difficulty: Literal["Beginner", "Intermediate", "Advanced"] = Field(
        description="Difficulty level for User request"
    )
    needs_action: bool = Field(
        description="True if the request performs action otherwise false."
    )
    summary: str = Field(
        description="A short simple-language summary of User's request."
    )


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: your GEMINI_API_KEY is missing in your .env file")
        return

    user_request = input("Please enter your request: ").strip()

    if not user_request:
        print("User request is empty. Please write it again.")

    try:
        client = genai.Client(api_key=api_key)
        response = client.interactions.create(
            model=MODEL_NAME,
            input=(
                "Analyze the user request and return the requested fields."
                "Choose the difficulty from beginner, intermediate or advanced."
                "Sets the needs_action to true if user asks for an action otherwise false."
                "Do not perform any action. Classify the request.\n\n"
                f"User Request: {user_request}"
            ),
            response_format=[
                {
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": RequestAnalysis.model_json_schema(),
                }
            ],
        )

        output_text = response.output_text
        if not output_text or not output_text.strip():
            print("Gemini returned an empty response. Please try again.")
            return

        analysis = RequestAnalysis.model_validate_json(output_text)
        print("\nValidated Request Analysis:\n")
        print(f"Topic: {analysis.topic}")
        print(f"Difficulty: {analysis.difficulty}")
        print(f"Needs action: {analysis.needs_action}")
        print(f"Summary: {analysis.summary}")

    except ValidationError as error:
        print("The response did not pass validation")
        print(error)

    except errors.APIError as error:
        print(f"Gemini request failed: {type(error).__name__}")
        print("Check your API key, model access, and quota.")

    except (TimeoutError, ConnectionError) as error:
        print(f"Network request failed: {type(error).__name__}")
        print("Check your internet connection and try again.")


if __name__ == "__main__":
    main()
