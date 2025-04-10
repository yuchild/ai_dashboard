# app.py

import streamlit as st
import pandas as pd

def main():
    st.title("Data Analytics Streamlit App")
    st.write("Welcome to your data analytics dashboard!")

    st.header("Upload a CSV File (<10MB)")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Check the file size
        file_bytes = uploaded_file.getvalue()
        file_size_mb = len(file_bytes) / (1024 * 1024)
        if file_size_mb > 10:
            st.error("File too large! Please upload a file smaller than 10MB.")
            return

        try:
            # Load CSV into a DataFrame
            df = pd.read_csv(uploaded_file)
            st.success("File loaded successfully!")
            st.write("Preview of your data:")
            st.dataframe(df.head())

            st.header("Dashboard - Data Aggregations")
            # Numeric Aggregation
            numeric_columns = df.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                st.subheader("Numeric Features Summary")
                numeric_summary = df[numeric_columns].describe().T
                st.dataframe(numeric_summary)
                numeric_summary_str = numeric_summary.to_string()
            else:
                st.info("No numeric columns found in the data.")
                numeric_summary_str = "No numeric data available."

            # Categorical Aggregation
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns
            cat_summary = ""
            if len(categorical_columns) > 0:
                st.subheader("Categorical Features Summary")
                for col in categorical_columns:
                    st.markdown(f"**{col} Value Counts:**")
                    counts_df = df[col].value_counts().reset_index().rename(
                        columns={'index': col, col: "Count"}
                    )
                    st.dataframe(counts_df)
                    cat_summary += f"\n{col} value counts:\n" + df[col].value_counts().to_string()
            else:
                st.info("No categorical columns found in the data.")
                cat_summary = "No categorical data available."

            st.header("Local AI Agent Q&A")
            user_question = st.text_input("Ask a question about your CSV data:")

            if st.button("Submit Question") and user_question:
                # Build a context from the CSV data (note: longer contexts may be truncated)
                csv_preview = df.head().to_string()
                combined_context = (
                    f"CSV Preview:\n{csv_preview}\n\n"
                    f"Numeric Summary:\n{numeric_summary_str}\n\n"
                    f"Categorical Summary:\n{cat_summary}"
                )
                # Truncate the context to avoid exceeding the model's max token limit
                max_chars = 1000
                if len(combined_context) > max_chars:
                    combined_context = combined_context[:max_chars]

                st.write("Querying local AI agent...")

                try:
                    from transformers import pipeline
                    # Use the question-answering pipeline with a small extractive QA model
                    qa_pipeline = pipeline(
                        "question-answering",
                        model="distilbert-base-uncased-distilled-squad"
                    )
                    result = qa_pipeline(question=user_question, context=combined_context)
                    answer = result.get('answer', 'No answer found.')
                    st.markdown("**Local AI Agent Answer:**")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error using local AI agent: {e}")

        except Exception as e:
            st.error(f"An error occurred while processing the CSV file: {e}")
    else:
        st.info("Awaiting CSV file upload. Please upload your file to see the preview and access the local AI agent.")

if __name__ == '__main__':
    main()
