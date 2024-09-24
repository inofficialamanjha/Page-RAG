# PageRag: An LLM and RAG Based Product FAQ Agent

## Detailed Notes

### To Run

#### System Requirements

1. [Python 3.11](https://www.python.org/downloads/release/python-3119/) or higher
2. Create a [virtual environment](https://docs.python.org/3/library/venv.html#)

#### Tool Requirements

1. Microsoft Azure Ai Services - [OpenAi](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
2. Populate the `AppSettings.json` with the required keys at placeholders

#### Command

`cd Page-RAG` : Make sure you are in the root directory of the project

```shell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r dependencies\requirements.txt
```


```shell
python startup.py
```

### Understanding Startup Arguments

1. `files`: A list of files to be containerized by the agent and saved in the database. This will be later used for recall

2. `save`: A flag to save the containerized files in the database post session completion

3. `reset`: A flag to reset the whole database on startup

4. `host`: A flag to notify the startup to host the application as a Flask app

Incase, no files are provided, the agent will automatically pick up the container files from the last sessions