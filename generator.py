from google import generativeai as genai
from scraper import get_title_prizes_companies

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

# Get reponse from gemini and parse it into dictionary
def get_parsed_reponse(url : str) -> str :
    
    title,companies,prizes = get_title_prizes_companies(url)

    prompt = f"""

    Generate a table containing a generous amount of detailed winning hackathon ideas. 
    The hackathon is sponsered by these companies : {companies} , and these 
    are the possible prizes : {prizes}.

    Cater each of the project ideas to a sponsoring company and a prize. You can include more
    than one prize and more than one sponsor per project idea. 

    """

    response = (chat_session.send_message(prompt)).text
    response = response.split("\n")
    
    response = [idea for idea in response if '|' in idea]
    response = [idea.split("|") for idea in response]
    response = [[element.strip().strip("*") for element in idea if element != '' ] for idea in response]
    response.pop(1)

    keys = response[0]
    response = response[1:]

    ideas_json = {"hackathon" : title, "ideas_list" : []}
    for i in range(len(response)) :
        temp_json = {}
        for j in range(len(keys)) :
            temp_json[keys[j]] = response[i][j]
        ideas_json["ideas_list"].append(temp_json)
    return ideas_json