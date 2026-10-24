
import unittest
from unittest.mock import Mock, patch

from parallel_ai_tasks import (
    generate_explanation,
    generate_questions,
    run_parallel_tasks,
)


class TestParallelAITasks(unittest.TestCase):
    def test_generate_explanation_returns_model_response(self) -> None:
        client = Mock()
        client.interactions.create.return_value.output_text = (
            "Python is used to build AI applications."
        )

        result = generate_explanation(client, "Python helps build AI.")

        self.assertEqual(
            result,
            "Python is used to build AI applications.",
        )
        client.interactions.create.assert_called_once()

    def test_generate_questions_returns_model_response(self) -> None:
        client = Mock()
        client.interactions.create.return_value.output_text = (
            "1. What is Python?"
        )

        result = generate_questions(client, "Python is used in AI.")

        self.assertEqual(result, "1. What is Python?")
        client.interactions.create.assert_called_once()

    def test_empty_explanation_raises_error(self) -> None:
        client = Mock()
        client.interactions.create.return_value.output_text = ""

        with self.assertRaisesRegex(ValueError, "empty explanation"):
            generate_explanation(client, "Example notes.")

    def test_empty_questions_raise_error(self) -> None:
        client = Mock()
        client.interactions.create.return_value.output_text = ""

        with self.assertRaisesRegex(ValueError, "empty questions"):
            generate_questions(client, "Example notes.")

    @patch("parallel_ai_tasks.ThreadPoolExecutor")
    def test_parallel_tasks_return_both_results(
        self,
        executor_class: Mock,
    ) -> None:
        executor = executor_class.return_value.__enter__.return_value
        explanation_future = Mock()
        explanation_future.result.return_value = "Explanation result"
        questions_future = Mock()
        questions_future.result.return_value = "Questions result"

        executor.submit.side_effect = [
            explanation_future,
            questions_future,
        ]

        client = Mock()

        explanation, questions = run_parallel_tasks(
            client,
            "Example notes.",
        )

        self.assertEqual(explanation, "Explanation result")
        self.assertEqual(questions, "Questions result")
        self.assertEqual(executor.submit.call_count, 2)
        executor_class.assert_called_once_with(max_workers=2)


if __name__ == "__main__":
    unittest.main()
