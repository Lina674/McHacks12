from google import generativeai as genai
import json

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
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

# Get reponse from gemini
def get_parsed_reponse(prompt : str, companies : list[str], prizes : list[str]) -> str :
    response = (chat_session.send_message(prompt)).text
    response = response.split("\n")
    
    response = [idea for idea in response if '|' in idea]
    response = [idea.split("|") for idea in response]
    response = [[element.strip().strip("*") for element in idea if element != '' ] for idea in response]
    response.pop(1)

    keys = response[0]
    response = response[1:]

    ideas_json = {"ideas_list" : []}
    for i in range(len(response)) :
        temp_json = {}
        for j in range(len(keys)) :
            temp_json[keys[j]] = response[i][j]
        ideas_json["ideas_list"].append(temp_json)
    return ideas_json