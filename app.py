# app.py

import streamlit as st
import pandas as pd
import openai

def main():
    st.title("Data Analytics Streamlit App")
    st.write("Welcome to your data analytics dashboard!")

    st.header("Upload a CSV File (<10MB)")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Check file size
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
            else:
                st.info("No numeric columns found in the data.")

            # Categorical Aggregation
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns
            if len(categorical_columns) > 0:
                st.subheader("Categorical Features Summary")
                for col in categorical_columns:
                    st.markdown(f"**{col} Value Counts:**")
                    counts_df = df[col].value_counts().reset_index().rename(
                        columns={'index': col, col: "Count"}
                    )
                    st.dataframe(counts_df)
            else:
                st.info("No categorical columns found in the data.")

            st.header("AI Agent Q&A")
            user_question = st.text_input("Ask a question about your CSV data:")

            if st.button("Submit Question") and user_question:
                # Prepare a CSV summary context
                csv_preview = df.head().to_string()
                if not df.select_dtypes(include=['number']).empty:
                    numeric_summary_str = df.describe().to_string()
                else:
                    numeric_summary_str = "No numeric data available."

                if not df.select_dtypes(include=['object', 'category']).empty:
                    cat_summary = ""
                    for col in df.select_dtypes(include=['object', 'category']).columns:
                        cat_summary += f"{col} Value Counts:\n{df[col].value_counts().to_string()}\n\n"
                else:
                    cat_summary = "No categorical data available."

                prompt = f"""You are a data analyst.

Here is a preview of the CSV file:
{csv_preview}

Numeric Summary:
{numeric_summary_str}

Categorical Summary:
{cat_summary}

Based on the summaries above, please answer the following question:
{user_question}"""

                st.write("Querying AI agent...")

                try:
                    # Set your OpenAI API key (ensure it is set in your Streamlit secrets)
                    openai.api_key = st.secrets["OPENAI_API_KEY"]

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful data analyst assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=200,
                        temperature=0.5
                    )
                    answer = response.choices[0].message['content'].strip()
                    st.markdown("**AI Agent Answer:**")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error calling OpenAI API: {e}")

        except Exception as e:
            st.error(f"An error occurred while processing the CSV file: {e}")
    else:
        st.info("Awaiting CSV file upload. Please upload your file to see the preview and access the AI agent.")

if __name__ == '__main__':
    main()
