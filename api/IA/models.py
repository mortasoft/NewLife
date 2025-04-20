from typing import List, Optional, Dict, Any
import utils as app_utils
from google import genai
from google.genai import types
import os,time
  
class GeminiManager:
    def __init__(self, engine) -> None:
        self.engine = engine

    def request(self, prompt: str, sys_instruction: str) -> Dict[str, Any]:
        """Request to the Gemini API."""
        try:
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            start_time = time.time()
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=sys_instruction)
            )
            end_time = time.time()
            generation_time = end_time - start_time
            print(f"Response generation time: {generation_time:.4f} seconds")
            print(response.text)
            result = {"generation_time": generation_time, "response": response.text}
                
            return {
                'data': result,
                'message': app_utils.generate_message("Gemini", 'request'),
                'result': 'ok',
                'status_code': 200
            }
        except Exception as e:
            return {
                'data': None,
                'message': f"Error requesting to Gemini: {str(e)}",
                'result': 'error',
                'status_code': 400
            }
