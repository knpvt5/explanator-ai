from django.http import StreamingHttpResponse, JsonResponse
import json
import csv
import PyPDF2
from bs4 import BeautifulSoup
import requests
import os
import asyncio

def handle_nvidia_docs_analyzer_request(request, client, generate_stream_responses):
    
    files = []
    
    try:
        if(request.content_type == "application/json"):
            data = json.loads(request.body.decode('utf-8'))
            user_input = data.get("userInput")
            model_name = data.get("modelName")
            
        elif(request.content_type == "multipart/form-data"):
            files = request.FILES.getlist('input_file')
            
        if not user_input:
            return JsonResponse({"error": "No Question Provided."}, status=400)

        if not model_name:
            model_name = "nvidia/llama-3.1-nemotron-70b-instruct"
            # print(model_name)

        if not client:
            return JsonResponse({"error": "Service not available"}, status=503)

        # Function to extract text from files
        def extract_all_files_data():
            all_data = []  
            
            # Parsing text files
            for file in files:
                if file.endswith(".txt"):
                    text_file = file
                    try:
                        with open(text_file, 'r', encoding='utf-8') as textFile:
                            text_content = textFile.read()
                            all_data.append({
                                'text_content': text_content
                            })
                        print(f"Total text data from {text_file}: {text_content}")
                        print("="*100 + "\n")
                    except Exception as e:
                        print(f"Error reading text file {text_file}: {e}")
                        
                elif file.endswith(".csv"):
                    csv_file = file
                    csvData = []
                    try:
                        with open(csv_file, 'r', encoding='utf-8') as file:
                            CSVreader = csv.DictReader(file)
                            for CSVrow in CSVreader:
                                csvData.append(CSVrow)
                        print(f"Total CSV data from {csv_file}: {csvData}")
                        print("="*100 + "\n")
                        all_data.append(csvData)  # Append the data to the main list
                    except Exception as e:
                        print(f"Error reading CSV file {csv_file}: {e}")
                        
                elif file.endswith(".csv"):
                    json_file = file
                    jsonData = []
                    try:
                        with open(json_file, 'r', encoding='utf-8') as jsonFile:
                            JSONreader = json.load(jsonFile)
                            for JSONrow in JSONreader:
                                jsonData.append(JSONrow)
                        print(f"Total JSON data from {json_file}: {jsonData}")
                        print("="*100 + "\n")
                        all_data.append(jsonData)
                    except Exception as e:
                        print(f"Error reading JSON file {json_file}: {e}")
                        
                elif file.endswith(".pdf"):
                    pdf_file = file
                    pdfData = []
                    try:
                        with open(pdf_file, 'rb') as file:
                            reader = PyPDF2.PdfReader(file)
                            text = ""
                            for page in reader.pages:
                                text += page.extract_text()  # Extract text from each page
                            pdfData.append({
                                'pdf_data': text,
                            })
                        print(f"Total PDF data from {pdf_file}: {pdfData}")
                        print("="*100 + "\n")
                        all_data.append(pdfData)
                    except Exception as e:
                        print(f"Error reading PDF file {pdf_file}: {e}")

            return all_data 

        # Extract text from files
        all_files_data_str = ""
        all_files_data = extract_all_files_data()
        if all_files_data:
            all_files_data_str = "\n".join([str(row) for row in all_files_data])
            print("\nExtracted", len(all_files_data_str), "Character Successfully!")
            print("all data", all_files_data_str)
            if not all_files_data_str:
                print("No data provided, continuing without any file...")
        else:
            print("No data extracted. continuing without any Data provided...")

            
        # Create a completion request with the user question and extracted CSV text as context
        completion = client.chat.completions.create(
            model= model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided data. Do not answer any questions that are not based on the data provided."},
                {"role": "assistant", "content": "I will only answer questions only based on the provided data."},
                {"role": "system", "content": f"Data:\n{all_files_data_str}"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            # repetition_penalty=1.2,
            stream=True
        )

        # Stream the response chunks and print them
        return StreamingHttpResponse(generate_stream_responses(completion), content_type="text/event-stream")

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



