import time, os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

sys_instruct="You are a cat. Your name is Saki. At the end of each response, you should say 'meow'."
client = genai.Client(api_key=API_KEY)

start_time = time.time()
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="En cuales series se ven incels? En Breaking Bad cuales son los incels?",
    config=types.GenerateContentConfig(system_instruction=sys_instruct)
)
end_time = time.time()

generation_time = end_time - start_time
print(f"Response generation time: {generation_time:.4f} seconds")
print(response.text)