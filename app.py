import streamlit as st
import openai
import altair as alt
import pandas as pd


# Set OpenAI API key from Streamlit secrets
openai.api_key = "YOUR OPENAI-API KEY"  # Changed for security reasons

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

data = pd.DataFrame({
    "Category": ["Colorectal", "Prostate", "Lip and oral cavity", "Non-Hodgkin lymphoma"],
    "Value": [8.7, 8.5, 7.6, 6.4], 
})

data1= pd.DataFrame({
    "Category": ["Breast", "Ovary and uterine adnexa", "Lip and oral cavity", "Cervix uteri", "Colorectal"],
    "Value": [45.9, 4.9, 4.2, 4.0, 3.9],
})

data2 = pd.DataFrame({
   "Category": ["Punjab", "Sindh", "Khyber Pakhtunkhwa (KP)", "Baluchistan"],
    "Value": [45.13, 26.83, 16.46, 3.52],
})

# Create the bar chart using Altair

# Create pie charts
chart1 = alt.Chart(data).mark_arc().encode(
    theta=alt.Theta(field="Value", type="quantitative"),
    color=alt.Color(field="Category", type="nominal", title="Common Cancers in Males"),
    tooltip=["Category", "Value"]
).properties(width=300, height=200)

chart2 = alt.Chart(data1).mark_arc().encode(
    theta=alt.Theta(field="Value", type="quantitative"),
    color=alt.Color(field="Category", type="nominal", title="Common Cancers in Females"),
    tooltip=["Category", "Value"]
).properties(width=300, height=200)

chart3 = alt.Chart(data2).mark_arc().encode(
    theta=alt.Theta(field="Value", type="quantitative"),
    color=alt.Color(field="Category", type="nominal", title="Province-wise Distribution"),
    tooltip=["Category", "Value"]
).properties(width=300, height=200)

st.title("Cancer Awareness Chatbot")

# Display pie charts as widgets
col1, col2, col3 = st.columns(3)
col1.altair_chart(chart1)
col2.altair_chart(chart3)
col3.altair_chart(chart2)


with st.sidebar:
    st.header("About")
    st.write("This app provides information based on AI-generated content for educational purposes only and is not a substitute for professional medical advice.")
    st.write("**Health Advisory:** If you or someone you know is facing a health emergency or cancer diagnosis, consult with healthcare professionals directly for appropriate tests, treatments, and actions.")
    st.header("Resources")
    st.markdown("[Cancer Statistics in Pakistan From 1994 to 2021: Data From Cancer Registry](https://pubmed.ncbi.nlm.nih.gov/37450777/)")
    st.markdown("[National Cancer Registry of Pakistan: First Comprehensive Report of Cancer Statistics 2015-2019](https://pubmed.ncbi.nlm.nih.gov/37300256/)")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("What is up?")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides cancer awareness information."},
                {"role": "user", "content": prompt}
            ],
        )
    except Exception as e:
        st.error(f"Error generating response: {e}")
        response = None

    if response:
        # Add assistant message to chat history
        assistant_response = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        # Display assistant message in chat message container
        with st.chat_message("assistant"):
            st.markdown(assistant_response)