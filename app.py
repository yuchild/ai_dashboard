# app.py

import streamlit as st
import pandas as pd

def main():
    st.title("Data Analytics Streamlit App")
    st.write("Welcome to your data analytics dashboard!")
    st.write("This is the initial setup. Now let's add CSV file upload capability.")

    st.header("Step 2: Upload a CSV File (<10MB)")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Convert the uploaded file to bytes and calculate its size in MB
        file_bytes = uploaded_file.getvalue()
        file_size_mb = len(file_bytes) / (1024 * 1024)
        if file_size_mb > 10:
            st.error("File too large! Please upload a file smaller than 10MB.")
        else:
            try:
                # Load the CSV file into a pandas DataFrame
                df = pd.read_csv(uploaded_file)
                st.success("File loaded successfully!")
                st.write("Preview of your data:")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"An error occurred while loading the CSV file: {e}")
    else:
        st.info("Awaiting CSV file upload. Please upload your file to see the preview.")

if __name__ == '__main__':
    main()
