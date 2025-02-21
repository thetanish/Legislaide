# -*- coding: utf-8 -*-
"""Legislaide.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17vn43WhZiCiclZUFlZJ8BdAEK26M-tSg
"""

!pip install openai==0.28.1
!pip install panel
!pip install llama-index==0.8.7

from google.colab import drive
drive.mount('/content/drive')
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import os
import openai
import panel as pn

openai.api_key = 'insert key here'
from google.colab import drive
!pip install pypdf
!pip install mdfreader

import os
documents = SimpleDirectoryReader('drive/MyDrive/SantaCruzCountyAgenda').load_data()

from google.colab import drive
drive.mount('/content/drive')

def continue_conversation(messages, temperature=0):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
    )
    #print(str(response.choices[0].message["content"]))
    return response.choices[0].message["content"]

def add_prompts_conversation(_):
    prompt = client_prompt.value_input
    client_prompt.value = ''

    context.append({'role':'user', 'content':f"{prompt}"})

    response = continue_conversation(context)

    context.append({'role':'assistant', 'content':f"{response}"})

    panels.append(
        pn.Row('Customer:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Legislaide:', pn.pane.Markdown(response, width=600)))

    return pn.Column(*panels)

context = [ {'role':'system', 'content':"""'I am Legislaide, a helpful chatbot meant to answer your questions about Santa Cruz County Agendas. How may I help you? (Say "thank you" to end the session) \n'"""} ]

pn.extension()

panels = []

client_prompt = pn.widgets.TextInput(value="Hi", placeholder='Enter your questions here…')
button_conversation = pn.widgets.Button(name="Chat with Legislaide!")

interactive_conversation = pn.bind(add_prompts_conversation, button_conversation)

dashboard = pn.Column(
    client_prompt,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True),
)

dashboard

from llama_index import VectorStoreIndex, SimpleDirectoryReader


from llama_index import StorageContext, load_index_from_storage
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist()

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
question = input('I am Legislaide, a helpful chatbot meant to answer your questions about Santa Cruz County Agendas. How may I help you? (Say "thank you" to end the session) \n')
while question != "thank you":
  response = query_engine.query(question)
  print(response)
  question = input()

