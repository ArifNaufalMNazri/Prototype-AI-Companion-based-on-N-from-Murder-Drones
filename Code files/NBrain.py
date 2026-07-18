from google import genai
from google.genai import types

key = "AQ.Ab8RN6KNkbZY7Q-PxJJ9vKqXAs1_YRcppkThNCw2r4FNL0GAGQ"

personality = "You must answer in only one sentence."

client = genai.Client(api_key = key)

def think(user_prompt):
  print(f"[N-Brain]: Hold on, I'm trying to understand ({user_prompt}) using the Cloud")
  try:
    response = client.models.generate_content(
      model = "gemini-2.5-flash",
      contents = user_prompt,
      config = types.GenerateContentConfig(
        system_instruction = personality
      )
    )

    return response.text

  except Exception as e:
    return f"My brain is getting fried!: {str(e)}"