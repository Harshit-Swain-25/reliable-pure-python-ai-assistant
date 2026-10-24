import unittest

from reliable_tool_loop import MAX_TOOL_CALLS, can_execute_tool_call


class TestToolCallLimit(unittest.TestCase):
    def test_first_tool_call_is_allowed(self):
        self.assertTrue(can_execute_tool_call(0))

    def test_last_allowed_tool_call_can_start(self):
        self.assertTrue(can_execute_tool_call(MAX_TOOL_CALLS - 1))

    def test_next_tool_call_is_rejected_at_limit(self):
        self.assertFalse(can_execute_tool_call(MAX_TOOL_CALLS))

    def test_tool_call_remains_rejected_above_limit(self):
        self.assertFalse(can_execute_tool_call(MAX_TOOL_CALLS + 1))


if __name__ == "__main__":
    unittest.main()
