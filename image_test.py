

from inference_sdk import InferenceHTTPClient
from openai import OpenAI
import os 


def parse_image(image_url):


    os.environ["OPENAI_API_KEY"] = "[OPENAI API KEY]"
    client = OpenAI()



    # A model for identifying car warning signs on the dashboard
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com", 
        api_key="[Write The API key]"    #! Need to add API key from roboflow
    )

    result = CLIENT.infer(image_url, model_id="car-dashboard-icons/3")



    print(result)
    responce_text = ""
    output = []
    for warning_light in result["predictions"]:
        warning_class = warning_light["class"]
        output.append(warning_class)
        """
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a knowledgeble car mechanic. You will be given a car dashboard warning sign, explain what it means and what should be done about it."},
            {"role": "user", "content": warning_class}
        ]
        )

        responce_text += response.choices[0].message.content
    """
    return output

#parse_image("images/saved/second.jpg")