
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from document_tool_demo import read_document


class TestDocumentToolRecovery(unittest.TestCase):
    def test_unapproved_filename_is_rejected(self):
        result = read_document("../.env")
        self.assertEqual(
            result["error"],
            "The document is not present in data folder.",
        )

    def test_missing_document_returns_error(self):
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            patch(
                "document_tool_demo.DATA_DIRECTORY",
                Path(temp_dir),
            ),
        ):
            result = read_document("project_brief.txt")

        self.assertEqual(
            result["error"],
            "Requested document does not exist.",
        )

    def test_empty_document_returns_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_file = Path(temp_dir) / "project_brief.txt"
            empty_file.write_text("", encoding="utf-8")

            with patch(
                "document_tool_demo.DATA_DIRECTORY",
                Path(temp_dir),
            ):
                result = read_document("project_brief.txt")

        self.assertEqual(
            result["error"],
            "Requested document cannot be empty.",
        )


if __name__ == "__main__":
    unittest.main()
