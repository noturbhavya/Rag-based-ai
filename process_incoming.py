import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={"model": "bge-m3", "input": text_list}
    )
    return r.json()["embeddings"]

def inference(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )
    return r.json()["response"]  # ✅ return only the response text

# Load your stored embeddings dataframe
df = joblib.load('embeddings.joblib')

# Get user query and create embedding
incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0]

# Find similarities of question embedding with other embeddings
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
top_results = 2
max_indx = similarities.argsort()[::-1][0:top_results]
new_df = df.loc[max_indx]

# Build the prompt for LLM
prompt = f'''I am test project. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user askes unrelated question, tell him that you can only answer questions related to the data provided
'''

# Save prompt (optional)
with open("prompt.txt", "w") as f:
    f.write(prompt)

# Call inference
response_text = inference(prompt)
print(response_text)

# Save response (optional)
with open("response.txt", "w") as f:
    f.write(response_text)
    