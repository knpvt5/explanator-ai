import os
from django.http import JsonResponse, StreamingHttpResponse
import google.generativeai as genai
import csv
import json
import PyPDF2

def handle_gemini_docs_analyzer_request(request, model, generate_stream_responses):
    
    try:
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("user_input", "")
    
        if not user_input:
            return JsonResponse({"error": "User input is required."}, status=400)

        # Specify the file paths
        files = [
            "static/eg_data/eg-txt-data/eg.txt",
            "static/eg_data/eg-csv-data/eg1.csv",
            "static/eg_data/eg-json-data/eg1.json",
            "static/eg_data/eg-pdf-data/eg.pdf",
        ]

        all_Data = []

        for filename in files:
            try:
                if filename.endswith(".txt"):
                    with open(filename, "r", encoding="utf-8") as file:
                        text_content = file.read()
                        all_Data.append(text_content)
                        # print(f"txt file data: {text_content}\n")
                        
                elif filename.endswith(".csv"):
                    csvData = []
                    with open(filename, "r", encoding="utf-8") as csvFile:
                        CSVreader = csv.DictReader(csvFile)
                        for CSVrow in CSVreader:
                            csvData.append(CSVrow)
                        # print(f"CSV file data: {csvData}\n")
                        all_Data.append(csvData)

                elif filename.endswith(".json"):
                    jsonData = []
                    with open(filename, "r", encoding="utf-8") as jsonFile:
                        JSONreader = json.load(jsonFile)
                        for JSONrow in JSONreader:
                            jsonData.append(JSONrow)
                        # print(f"json file data: {jsonData}\n")
                        all_Data.append(jsonData)
                    
                elif filename.endswith(".pdf"):
                    pdfData = []
                    with open(filename, "rb") as pdfFile:
                        PDFreader = PyPDF2.PdfReader(pdfFile)
                        for page in PDFreader.pages:
                            text = page.extract_text()
                            pdfData.append(text)
                        # print(f"pdf file data: {pdfData}\n")
                        all_Data.append(pdfData)
                else:
                    print(f"Unsupported file format: {filename}")
            except FileNotFoundError:
                    print(f"Error: File not found at path '{filename}'. Please ensure the file exists.\n")


        # Convert all data to string format
        all_Data_str = str(all_Data) if all_Data else ""
        print("all data string:", all_Data_str)

        if not all_Data:
            print("No data extracted. Exiting...")
            return JsonResponse({"error": "No data extracted."}, status=400)
            
        
        try:
            # Generate content using the text data as context
            prompt = (
                # "You are a helpful assistant. Only answer questions based on the provided text data. "
                # "Do not answer any questions that are not based on the text data. "
                f"Text Data:\n{all_Data_str}\n\n"
                    f"User's Input: {user_input}"
                )

            response = model.generate_content(
                contents=prompt,
                generation_config=genai.types.GenerationConfig(
                max_output_tokens=1024),
                stream=True,
                # tools=None,
                # tool_config=None,
                # request_options=None
            )
            
            return StreamingHttpResponse(
                generate_stream_responses(response),
                content_type="text/event-stream",
            )
                
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
            
    except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
        