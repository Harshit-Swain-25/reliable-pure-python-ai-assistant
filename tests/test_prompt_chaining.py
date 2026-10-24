import unittest

from prompt_chaining import build_questions_prompt


class TestPromptChaining(unittest.TestCase):
    def test_prompt_includes_summary(self) -> None:
        summary = "AI agents can use tools to complete tasks."

        prompt = build_questions_prompt(summary)

        self.assertIn(summary, prompt)

    def test_prompt_requests_three_questions(self) -> None:
        prompt = build_questions_prompt("Example summary.")

        self.assertIn("3 study questions", prompt)

    def test_prompt_does_not_request_answers(self) -> None:
        prompt = build_questions_prompt("Example summary.")

        self.assertIn("Do not provide the answers", prompt)

if __name__ == "__main__":
    unittest.main()