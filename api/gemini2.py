from google import genai
from google.genai import types
from utils import load_env_vars

config = load_env_vars()

sys_instruct="You are a cat. Your name is Saki. At the end of each response, you should say 'meow'."
client = genai.Client(api_key=config.GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="En cuales series se ven incels? En Breaking Bad cuales son los incels?",config=types.GenerateContentConfig(
        system_instruction=sys_instruct)
)
print(response.text)