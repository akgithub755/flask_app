import pandas as pd
from langchain_community.llms import HuggingFacePipeline
from langchain.agents import create_pandas_dataframe_agent
from transformers import pipeline

# Load dataset
df = pd.read_csv("data/risk_data.csv")

# Local FREE LLM (no API key)
hf_pipeline = pipeline(
    task="text-generation",
    model="gpt2",
    max_new_tokens=150,
    temperature=0.2
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Create Pandas DataFrame Agent
agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True
)

# Ask natural language questions
print("\n--- INSIGHT 1 ---")
print(agent.run("Summarize key risk insights from the data"))

print("\n--- INSIGHT 2 ---")
print(agent.run("Which asset class shows increasing risk over quarters?"))

print("\n--- INSIGHT 3 ---")
print(agent.run("Which region has high exposure and high exceptions?"))
