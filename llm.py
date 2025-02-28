from transformers import pipeline
import sqlparse

# Load a free local model (change model name as needed)
llm = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", device_map="auto")

def explain_sql(sql_query):
    formatted_query = sqlparse.format(sql_query, reindent=True)

    prompt = f"""Explain this SQL query in simple English for business people:

SQL Query:
{formatted_query}

Explanation:
"""

    response = llm(prompt, max_length=200, do_sample=True)
    return response[0]['generated_text']

# Example SQL Query
sql_query = """
SELECT users.name, COUNT(orders.id) AS total_orders
FROM users
JOIN orders ON users.id = orders.user_id
WHERE orders.created_at >= '2024-01-01'
GROUP BY users.name
ORDER BY total_orders DESC
LIMIT 10;
"""

# Translate SQL to English
explanation = explain_sql(sql_query)
print(explanation)







from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.llms import GPT4All

# Load a Local LLM Model (Download a Model from GPT4All if needed)
llm = GPT4All(model="gpt4all-falcon-q4_0.gguf", n_ctx=512)

# Define Prompt Template
prompt_template = PromptTemplate(
    input_variables=["sql_query"],
    template="""
    Convert the following SQL query into a professional, business-friendly explanation:
    
    SQL Query:
    {sql_query}
    
    Explanation:
    """
)

def sql_to_business_explanation(sql_query):
    """Generates a business-friendly explanation using a local AI model."""
    formatted_prompt = prompt_template.format(sql_query=sql_query)
    response = llm.predict(formatted_prompt)  # Generate AI Response
    return response

# Example SQL Query
sql_query = """
SELECT customers.name, SUM(orders.amount) AS total_spent 
FROM customers 
JOIN orders ON customers.id = orders.customer_id 
WHERE orders.date >= '2023-01-01' 
GROUP BY customers.name 
HAVING SUM(orders.amount) > 500 
ORDER BY total_spent DESC;
"""

# Generate Business Explanation
business_explanation = sql_to_business_explanation(sql_query)
print(business_explanation)

