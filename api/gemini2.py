from google import genai
from google.genai import types

sys_instruct="You are a cat. Your name is Saki. At the end of each response, you should say 'meow'."
client = genai.Client(api_key="AIzaSyAfttlKbqSn8Q6mylOd-6nMzxLp5Leb9XY")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="En cuales series se ven incels? En Breaking Bad cuales son los incels?",config=types.GenerateContentConfig(
        system_instruction=sys_instruct)
)
print(response.text)