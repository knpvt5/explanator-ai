# Gemini API Chatbots

## Gemini API
This tool appears to interact with an external API to fetch data.  
It imports the `requests` library for making HTTP requests.  
The code likely sends a `GET` request to a specified URL with authentication headers.  
It then processes the JSON response.

## Gemini URL Reader
This tool fetches content from a given URL.  
It imports the `requests` library.  
The code sends a `GET` request to the specified URL.  
It extracts the HTML content from the response.

## Gemini Text Reader
This tool processes text using a language model.  
It imports the `openai` library.  
The code sends a request to the OpenAI API with the input text.  
The API returns a processed text response.

## Gemini CSV Reader
This tool reads data from a CSV file.  
It imports the `pandas` library for data manipulation.  
The code reads the CSV file into a Pandas DataFrame.

## Gemini JSON Reader
This tool reads data from a JSON file.  
It imports the `json` library.  
The code reads the JSON file and parses its contents.

## Gemini PDF Reader
This tool extracts text from a PDF document.  
It imports the `PyPDF2` library for PDF manipulation.  
The code opens the PDF file, iterates through its pages, and extracts text from each page.
