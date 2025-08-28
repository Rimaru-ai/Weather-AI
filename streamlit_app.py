import streamlit as st
from rag_weather import build_weather_rag_qa

st.set_page_config(page_title="Weather RAG App", page_icon="⛅", layout="centered")

st.title("🌤️ Weather RAG System")
st.write("Ask about weather forecasts stored in the system.")

# Load RAG system
qa = build_weather_rag_qa("data/weather_data.csv")

# User input
query = st.text_input("Ask a weather question:")

if query:
    with st.spinner("Thinking..."):
        result = qa.invoke({"query": query})
    st.success("Answer:")
    st.write(result["result"])
