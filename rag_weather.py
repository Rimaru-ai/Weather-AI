import os
import pandas as pd
from datetime import datetime, timedelta
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document

# =========================
# 1. Load API Key
# =========================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # In Colab: %env OPENAI_API_KEY=your_key_here

# =========================
# 2. Load Weather Data
# =========================
def load_weather_data(csv_file="weather.csv"):
    df = pd.read_csv(csv_file)

    # Ensure columns are consistent
    required_cols = {"city", "date", "avg_temp", "avg_humidity", "weather_desc"}
    if not required_cols.issubset(set(df.columns)):
        raise KeyError(f"CSV must contain {required_cols}, found {df.columns}")

    docs = []
    for _, row in df.iterrows():
        text = (
            f"City: {row['city']}, Date: {row['date']}, "
            f"Average Temp: {row['avg_temp']}°C "
            f"(Min: {row['min_temp']}°C, Max: {row['max_temp']}°C), "
            f"Humidity: {row['avg_humidity']}%, "
            f"Weather: {row['weather_desc']}"
        )
        docs.append(Document(page_content=text, metadata={"city": row["city"], "date": row["date"]}))
    return docs

# =========================
# 3. Normalize Query (Handle 'today', 'tomorrow')
# =========================
def normalize_query(query: str) -> str:
    today = datetime.today()
    if "tomorrow" in query.lower():
        tomorrow = today + timedelta(days=1)
        return query + f" (specifically {tomorrow.strftime('%Y-%m-%d')})"
    if "today" in query.lower():
        return query + f" (specifically {today.strftime('%Y-%m-%d')})"
    return query

# =========================
# 4. Build RAG Pipeline
# =========================
def build_rag_pipeline(docs):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Create FAISS vector store
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt = PromptTemplate(
        template=(
            "You are a helpful assistant answering weather questions from stored forecasts.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\nAnswer:"
        ),
        input_variables=["context", "question"],
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
    )
    return qa

# =========================
# 5. Main
# =========================
if __name__ == "__main__":
    docs = load_weather_data("weather.csv")
    qa = build_rag_pipeline(docs)

    print("✅ Weather RAG system ready. Ask your questions!")

    while True:
        query = input("\nAsk a weather question (or 'exit'): ")
        if query.lower() == "exit":
            break
        normalized = normalize_query(query)
        result = qa({"query": normalized})
        print("\nAnswer:", result["result"])
