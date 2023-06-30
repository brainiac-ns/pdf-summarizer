import os
from time import time

import streamlit as st
from sum import summarize_pdf
from utils import extract_text, write_list_to_pdf
from text_summarization import to_summarize


def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as file:
        file.write(uploaded_file.getbuffer())


def main():
    st.title("PDF Uploader")

    # File upload section
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        # Get the filename and extension
        filename = uploaded_file.name
        summarized_path = os.path.join("summarized", filename)
        if os.path.exists(summarized_path):
            download_text = f"Click here to download summarised {filename}"
            with open(summarized_path, "rb") as file:
                pdf_contents = file.read()

            st.download_button(download_text, pdf_contents, mime="application/pdf")
            return

        # Specify the save path
        save_directory = "uploads"  # Specify the desired save directory
        save_path = os.path.join(save_directory, filename)

        # Save the uploaded file
        save_uploaded_file(uploaded_file, save_path)
        progress_bar = st.progress(0)
        # Extract the text from the PDF
        extracted_text = extract_text(save_path)

        start = time()
        extracted_paragraphs = summarize_pdf(extracted_text, progress_bar)
        print(f"Time taken to summarize {filename}: {time() - start} seconds")

        write_list_to_pdf(extracted_paragraphs, summarized_path)

        st.success("File summarised successfully.")

        # Download link for the saved file
        download_text = f"Click here to download summarised {filename}"
        with open(summarized_path, "rb") as file:
            pdf_contents = file.read()

        st.download_button(download_text, pdf_contents, mime="application/pdf")
        uploaded_file = None


if __name__ == "__main__":
    main()
