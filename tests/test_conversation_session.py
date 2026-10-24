
import unittest

from conversation_session import ConversationSession


class TestConversationSession(unittest.TestCase):
    def test_new_session_has_no_interaction_id(self) -> None:
        session = ConversationSession()

        self.assertIsNone(session.previous_interaction_id)

    def test_update_stores_interaction_id(self) -> None:
        session = ConversationSession()

        session.update("interaction-123")

        self.assertEqual(
            session.previous_interaction_id,
            "interaction-123",
        )

    def test_update_replaces_previous_interaction_id(self) -> None:
        session = ConversationSession()
        session.update("interaction-123")

        session.update("interaction-456")

        self.assertEqual(
            session.previous_interaction_id,
            "interaction-456",
        )


if __name__ == "__main__":
    unittest.main()
