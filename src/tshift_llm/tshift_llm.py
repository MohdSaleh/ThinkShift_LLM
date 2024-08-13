from llama_index.llms.litellm import LiteLLM
from llama_index.core.llms import ChatMessage
from typing import List, Dict, Any
import time
import logging
import json

class LiteLLMClient:
    def __init__(self, model: str, api_key: str, api_base: str):
        self.llm = LiteLLM(model=model, api_key=api_key, api_base=api_base)

    def completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        chat_messages = [ChatMessage(role=msg['role'], content=msg['content']) for msg in messages]
        return self.llm.chat(chat_messages, **kwargs)

class tShift_LLM:
    def __init__(self, clients: List[LiteLLMClient]):
        self.clients = clients
        self.current_client_index = 0
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger("tShift_LLM")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("tshift_llm.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_request(self, client: LiteLLMClient, messages: List[Dict[str, str]], start_time: float, 
                    end_time: float, status: str, response: Any = None, error: str = None):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "client_model": client.llm.model,
            "messages": messages,
            "duration": end_time - start_time,
            "status": status
        }
        if response:
            log_entry["response"] = response if isinstance(response, str) else response.dict()
        if error:
            log_entry["error"] = error
        self.logger.info(json.dumps(log_entry))

    def get_next_client(self) -> LiteLLMClient:
        client = self.clients[self.current_client_index]
        self.current_client_index = (self.current_client_index + 1) % len(self.clients)
        return client

    def completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        for _ in range(len(self.clients)):
            client = self.get_next_client()
            start_time = time.time()
            try:
                response = client.completion(messages, **kwargs)
                end_time = time.time()
                self.log_request(client, messages, start_time, end_time, "success", response=response)
                return response
            except Exception as e:
                end_time = time.time()
                self.log_request(client, messages, start_time, end_time, "error", error=str(e))
                print(f"Error with {client.llm.model}: {str(e)}. Shifting to next model.")
        
        raise Exception("All models failed to generate a response")

    def stream_completion(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        for _ in range(len(self.clients)):
            client = self.get_next_client()
            start_time = time.time()
            try:
                stream = client.completion(messages, stream=True, **kwargs)
                for chunk in stream:
                    yield chunk
                end_time = time.time()
                self.log_request(client, messages, start_time, end_time, "success")
                return
            except Exception as e:
                end_time = time.time()
                self.log_request(client, messages, start_time, end_time, "error", error=str(e))
                print(f"Error with {client.llm.model}: {str(e)}. Shifting to next model.")
        
        raise Exception("All models failed to generate a streaming response")
