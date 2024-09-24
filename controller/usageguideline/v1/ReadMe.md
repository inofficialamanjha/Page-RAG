# Flask App: Page-RAG

# Release Notes

1. `flask_app.py` host the API's to upload files and query

# Detailed Notes

## Home: GET

GET request to `/` will return the home page

## Upload Files: POST

A POST request that enables process and index files via the pipeline

1. `Url`: `{{base_url}}/upload_files`
2. `Body: form-data`

   | Key       | Value                  | Description                         |
   |-----------|------------------------|-------------------------------------|
   | "enctype" | "multipart/form-data"  | Enables browser to upload file data |
   | "file"    | <file_to_upload: file> | The file to be uploaded             |

## Query: GET

A GET request that enables user query and get augment generated responses

1. `Url`: `{{base_url}}/query`
2. `Body: Params`

   | Key          | Value                | Description                           |
   |--------------|----------------------|---------------------------------------|
   | "user_query" | <query: str>         | The query from the user               |
   | "stream"     | <true_or_false: str> | Weather to stream the response or not |


## Search: GET

A GET request that enables searching on our vector database and get relevant pages

1. `Url`: `{{base_url}}/search`
2. `Body: Params`

   | Key            | Value                | Description                          |
   |----------------|----------------------|--------------------------------------|
   | "search_query" | <query: str>         | The search query                     |
   | "simplify"     | <true_or_false: str> | Weather to simplify the query or not |
