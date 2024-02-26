from llama_index import StorageContext, load_index_from_storage
from logging_spinner import SpinnerHandler
from llama_index.indices.postprocessor import MetadataReplacementPostProcessor
import logging
import streamlit as st
from helpers import readGoogleDrive, create_mp3
import sys
from llama_index.query_engine import RetryQueryEngine
from llama_index.evaluation import RelevancyEvaluator
import os
from PIL import Image

from image_test import parse_image

def handle_image(image_url):
    responce = parse_image(image_url)
    for query in responce:
        top_k = 5
        query_engine = st.session_state.index.as_query_engine(
            similarity_top_k = top_k,
            node_postprocessors =  [MetadataReplacementPostProcessor(target_metadata_key="window")]
        )

        query_response_evaluator = RelevancyEvaluator()
        retry_query_engine = RetryQueryEngine(
            query_engine, query_response_evaluator
        )

        response = retry_query_engine.query("You are a knowledgeble car mechanic. You will be given a car dashboard warning sign, explain what it means and what should be done about it\n\n" + query)
        
        create_mp3(response)
        st.audio("speech.mp3")
        st.markdown(response)

def handle_user_input(query, top_k):
    print(top_k)
    query_engine = st.session_state.index.as_query_engine(
        similarity_top_k = top_k,
        node_postprocessors =  [MetadataReplacementPostProcessor(target_metadata_key="window")]
    )

    query_response_evaluator = RelevancyEvaluator()
    retry_query_engine = RetryQueryEngine(
        query_engine, query_response_evaluator
    )

    response = retry_query_engine.query("Imagine that you are an experienced mechanic at a car dealership. Answer the following query:\n\n" + query)
    
    create_mp3(response)
    st.audio("speech.mp3")
    st.markdown(response)       
    st.markdown('----------------------------------------------')
    st.markdown('**Evidence:**')
    for i in range(len(response.source_nodes)):        
        window = response.source_nodes[i].node.metadata["window"]
        sentence = response.source_nodes[i].node.metadata["original_text"]

        st.markdown(f"**Retrieved Sentence:** {sentence}")
        st.markdown('----------------------------------------------')
        
        st.markdown(f"**Window around Sentence:** {window}") 
        st.markdown('----------------------------------------------')
        
  
    # To log the questions and answers uncomment the following lines:
    #     with open("log/q&a.csv", "a") as log:
    #         log.write(f'{question},"{response}"\n')

def load_image(image_file):
    img = Image.open(image_file)
    return img

def main():
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(SpinnerHandler())


    os.environ["OPENAI_API_KEY"] = "[OpenAI API key]" #! Need to change the api key
    st.set_page_config(page_title="Pocket Mechanic", page_icon="🧊")

    if "index" not in st.session_state:
        st.session_state.index = None

    st.header("Chat with Pocket Mechanic")

    top_k = st.sidebar.slider("Top K:", 1, 10, 4)
    user_question = st.text_input("Ask a question:")
    

    image_file = st.file_uploader("Upload an image for inspection")

    if image_file is not None:
        file_details = {"FileName":image_file.name,"FileType":image_file.type}
        img = load_image(image_file)
        st.image(img,width=250)
        with open(os.path.join("images", "saved",image_file.name),"wb") as f: 
            f.write(image_file.getbuffer())         
            handle_image(os.path.join("images", "saved", image_file.name))
            #st.success("Saved File")
        



    if user_question:
        if st.session_state.index:        
            handle_user_input(user_question, top_k)
        else:
            st.write("Please enter your Google Folder ID first")
    with st.sidebar:
        st.subheader("Your Google Folder ID")
        folder_id = st.text_input("Enter your Google Folder ID:")

        if st.button("Process"):

            with st.spinner("Processing"):

                upload_new = False
                if upload_new:
                    st.session_state.index = readGoogleDrive(folder_id)

                else: 
                    # To use existing database uncomment the following lines
                    storage_context = StorageContext.from_defaults(persist_dir ="./storage")
                    st.session_state.index = load_index_from_storage(storage_context)


    
if __name__ == '__main__':
    main()