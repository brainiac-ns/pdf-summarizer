import os

import streamlit as st
from utils import extract_text, write_list_to_pdf


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

        # Specify the save path
        save_directory = "uploads"  # Specify the desired save directory
        save_path = os.path.join(save_directory, filename)

        # Save the uploaded file
        save_uploaded_file(uploaded_file, save_path)

        # Extract the text from the PDF
        extracted_text = extract_text(save_path)
        write_list_to_pdf(extracted_text, os.path.join("summarized", filename))

        st.success("File summarised successfully.")

        # Download link for the saved file
        download_text = f"Click here to download summarised {filename}"
        with open(save_path, "rb") as file:
            pdf_contents = file.read()

        st.download_button(download_text, pdf_contents, mime="application/pdf")


if __name__ == "__main__":
    main()
