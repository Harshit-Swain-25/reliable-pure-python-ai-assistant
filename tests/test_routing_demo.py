
import unittest
from unittest.mock import Mock

from routing_demo import classify_request, dispatch_request


class TestRequestRouting(unittest.TestCase):
    def test_explanation_request(self) -> None:
        self.assertEqual(
            classify_request("Explain AI agents."),
            "explanation",
        )

    def test_summary_request(self) -> None:
        self.assertEqual(
            classify_request("Summarize my notes."),
            "summary",
        )

    def test_questions_request(self) -> None:
        self.assertEqual(
            classify_request("Give me three questions."),
            "questions",
        )

    def test_unknown_request(self) -> None:
        self.assertEqual(
            classify_request("Tell me a joke."),
            "unknown",
        )

    def test_empty_request_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            classify_request("   ")

    def test_routing_is_case_insensitive(self) -> None:
        self.assertEqual(
            classify_request("EXPLAIN AI AGENTS."),
            "explanation",
        )
    
    
    def test_explanation_route_executes_correct_handler(self) -> None:
        client = Mock()
        client.interactions.create.return_value.output_text = "Mock explanation"

        result = dispatch_request("Explain AI agents.", client)

        self.assertEqual(result, "Mock explanation")
        client.interactions.create.assert_called_once()
        self.assertIn(
            "beginner-friendly language",
            client.interactions.create.call_args.kwargs["input"],
        )

    def test_summary_route_executes_correct_handler(self) -> None:
        client = Mock()
        client.interactions.create.return_value.output_text = "Mock summary"

        result = dispatch_request("Summarize my notes.", client)

        self.assertEqual(result, "Mock summary")
        client.interactions.create.assert_called_once()
        self.assertIn(
            "Summarize",
            client.interactions.create.call_args.kwargs["input"],
        )

    def test_questions_route_executes_correct_handler(self) -> None:
        client = Mock()
        client.interactions.create.return_value.output_text = "Mock questions"

        result = dispatch_request("Give me three questions.", client)

        self.assertEqual(result, "Mock questions")
        client.interactions.create.assert_called_once()
        self.assertIn(
            "three useful study questions",
            client.interactions.create.call_args.kwargs["input"],
        )

    def test_unknown_route_is_not_executed(self) -> None:
        client = Mock()

        result = dispatch_request("Tell me a joke.", client)

        self.assertEqual(
            result,
            "Sorry, this request type is not supported yet.",
        )
        client.interactions.create.assert_not_called()



if __name__ == "__main__":
    unittest.main()
