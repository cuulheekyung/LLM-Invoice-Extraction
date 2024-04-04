# from langchain.llms import OpenAI
# from langchain.llms.openai import OpenAI
# pip install -U langchain-community
# from langchain_community.llms import OpenAI


import pandas as pd
import re
from pypdf import PdfReader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import JSONLoader


import json
import pathlib 
# from pprint import pprint

#Extract Information from PDF file
def get_pdf_text(doc):
    text = ""
    pages = PyPDFLoader(doc).load_and_split()
    print(pages)
    for i in range(len(pages)):
        page=pages[i]
        text += page.page_content
    return text

def get_csv_text(doc):
    text = CSVLoader(doc).load()

    return text

def get_json_text(doc):
    text = json.loads(pathlib.Path(doc).read_text())

    return text


from langchain.prompts import PromptTemplate

from langchain_anthropic import ChatAnthropic

# model = ChatAnthropic(model='claude-3-opus-20240229')
# model = ChatAnthropic(model='claude-3-sonnet-20240229')
# or use 'claude-2.1'
# from langchain_anthropic import AnthropicLLM
# model = AnthropicLLM(model='claude-2.1')



#Function to extract data from text
def extracted_data(pages_data):

    template = """Extract all the following values : Name, Invoice no., Description, Quantity, Date, 
        Unit price , Amount, Total, Email, Phone number and Address from this data: {pages}

        Expected output: remove any dollar symbols and any titles from name, that is, mr., ms., mrs., etc should be removed in name. {{'Name': 'Shelly Phei', 'Invoice no.': '1001329','Description': 'Office Chair','Quantity': '2','Date': '5/4/2023','Unit price': '1100.00','Amount': '2200.00','Total': '2200.00','Email': 'Shelly.Phei@gmail.com','Phone number': '782-897-0012','Address': 'Vancouver, BC, Canada'}}
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    # llm = OpenAI(temperature=.7)
    llm = ChatAnthropic(model='claude-3-sonnet-20240229')
    full_response=llm.predict(prompt_template.format(pages=pages_data))
    
    

    #print(full_response)
    return full_response


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_file_list):
    df_list=[]
 
    for user_file in user_file_list:
        
        # print(user_file)
        #split the process depending on the file type, pdf, csv, json only
        if user_file.name[-3:]=='pdf':
            raw_data=get_pdf_text(user_file)
        elif user_file.name[-3:]=='csv':
            raw_data=get_csv_text(user_file)
        elif user_file.name[-3:]=='son':
            raw_data=get_json_text(user_file)
        else: print("Error, file types are not matched")        
        #print(raw_data)
        #print("extracted raw data")

        llm_extracted_data=extracted_data(raw_data)
        #print("llm extracted data")
        #Adding items to our list - Adding data & its metadata

        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            # Converting the extracted text to a dictionary
            data_dict = eval('{' + extracted_text + '}')
            print(data_dict)
        else:
            print("No match found.")

        df_list.append(data_dict)
        df=pd.DataFrame(df_list)
        # df=df.append([data_dict], ignore_index=True)
        print("********************DONE***************")
        

    df.head()
    return df