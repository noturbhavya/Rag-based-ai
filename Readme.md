# How to use this RAG AI Teaching Assistant on your data
## Step 1 - Collect your videos
Move all your video files to the videos folder 

## Step 2 - Covert to mp3
Covert all the video files to mp3 by running Video_to_mp3

## Step 3 - Covert mp3 to json
Covert all the mp3 files to json by running mp3_to_json

## Step 4 - convert the json files to vectors
use the file preprocess_json to convert the json files to a dataframe with embeddings and save it as a joblib piickle

## Step 5 - Prompt generation and feeding to LLM
Read the joblib file and load it into the memory. Then create a relevant prompt as per the user query and feed it to the LLM
