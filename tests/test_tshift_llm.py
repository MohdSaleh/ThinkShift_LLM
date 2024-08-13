import unittest
from unittest.mock import Mock
from tshift_llm.tshift_llm import tShift_LLM

class TestTShiftLLM(unittest.TestCase):
    def setUp(self):
        # Create mock LiteLLMClient objects
        self.mock_client1 = Mock()
        self.mock_client1.llm = Mock()
        self.mock_client1.llm.model = "gpt-3.5-turbo"
        
        self.mock_client2 = Mock()
        self.mock_client2.llm = Mock()
        self.mock_client2.llm.model = "gpt-3.5-turbo"

        # Initialize tShift_LLM with mock clients
        self.tshift_llm = tShift_LLM(clients=[self.mock_client1, self.mock_client2])

    def test_completion_success(self):
        self.mock_client1.completion.return_value = "Success"
        result = self.tshift_llm.completion([{"role": "user", "content": "Test"}])
        self.assertEqual(result, "Success")
        self.mock_client1.completion.assert_called_once()

    def test_completion_fallback(self):
        self.mock_client1.completion.side_effect = Exception("Error")
        self.mock_client2.completion.return_value = "Fallback Success"
        result = self.tshift_llm.completion([{"role": "user", "content": "Test"}])
        self.assertEqual(result, "Fallback Success")
        self.mock_client1.completion.assert_called_once()
        self.mock_client2.completion.assert_called_once()

if __name__ == "__main__":
    unittest.main()
