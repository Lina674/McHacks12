from google import generativeai as genai

genai.configure(api_key="AIzaSyBQqnpIRFvNbjrZBDp1Fjgi_IsQmPpgcHU")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-8b",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

# Get reponse from gemini
def get_reponse(prompt : str) -> str :
        response = (chat_session.send_message(prompt)).text
        return response