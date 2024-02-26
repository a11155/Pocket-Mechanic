# Pocket Mechanic

Allows to ask LLM questions related to vehicles as text queries or images.

## Run Locally
You need to use python version 3.12.1. Other versions might not be working correctly

Install dependencies from the requirements.txt file:

```bash
  pip install -r requirements.txt
```

Run the application using streamlit:
```bash
  streamlit run main.py
```



Currenty the knowledge base of the pocket mechanic is limited to information about Nissan Pathfinder 2013, and has to be run using python 3.12.1 as described by the reasons below.




## About Using different Knowledge Base

Originally Pocket Mechanic allowed to share pdf documents from google drive to use as its data. However, image model worked only using python 3.12.1, which was incompatible with the version of llama-hub library required for importing documents through google drive. 

Therefore, right now the data the model uses as its knowledge base is static and is  stored in the storage folder, and is composed of a collection of car manuals for Nissan Pathfinder 2013.

If you would like to update the data to a different set of documents you can do by tweeking some parts of the code to remove the image model use, use python 3.9 with a version of llama-hub 0.0.60, create a [service account](https://cloud.google.com/iam/docs/keys-create-delete) and create a credentials.json file in the the project root to connect the service account to the Pocket Mechanic.

Also python 3.12.1 was not working with the dotenv library for some reason, which we realized only couple of minutes before presenting which means the API keys for OpenAI and Roboflow (which hosts the warning sings classification model) need to be hardcoded in the code as of right now. 



