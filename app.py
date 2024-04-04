import streamlit as st
from dotenv import load_dotenv
from utils import *
import tempfile
import pathlib


def main():
    load_dotenv()

    temp_dir = tempfile.TemporaryDirectory() # to use temp dir to write the uploaded files and then to be destroyed after the script finishes
    st.set_page_config(page_title="Invoice Data Pull Extraction Bot")
    st.title("Invoice Data Pull Extraction Bot ")
    st.subheader("I can help you in extracting data from multiple files")


    # Upload the Invoices (pdf, csv, json files)
    uploaded_files = st.file_uploader("Upload invoices here, only PDF, CSV, JSON files allowed", type=["pdf", "csv","json"],accept_multiple_files=True)
    # Once a file is uploaded, files contains the file data 
    # but one can not directly pass this to document loader from langchain as it is a BytesIO object.
    # We need to save this file locally and temporarily
    uploaded_file_dir = pathlib.Path(temp_dir.name) 
    temp_file_list=[]
    for uploaded_file in uploaded_files:
        temp_file=uploaded_file_dir /uploaded_file.name
        with open(temp_file, mode='wb') as w:
            w.write(uploaded_file.getvalue())
        temp_file_list.append(temp_file)
        # and then, pass its file path to the loader


    submit=st.button("Extract Data")
    
    if submit:
        with st.spinner('Wait for it...'):
            
            df=create_docs(temp_file_list)
            st.write(df.head())

            data_as_csv= df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download data as CSV", 
                data_as_csv, 
                "output.csv",
                "text/csv",
                key="download-tools-csv",
            )
        st.success("Hope I was helpful !!!❤️❤️❤️")


#Invoking main function
if __name__ == '__main__':
    main()
