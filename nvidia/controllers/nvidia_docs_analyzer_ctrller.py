from django.http import StreamingHttpResponse, JsonResponse
import json
import csv
import PyPDF2
from bs4 import BeautifulSoup
import requests
import os
import asyncio

def handle_nvidia_docs_analyzer_request(request, client, generate_stream_responses):
    try:
        files = []
        file_data = []
        user_input = None
        model_name = None
        
        if request.FILES:
            files = request.FILES.getlist('input_file')
            print(f"Files received: {[file.name for file in files]}")

            # Inside the block, save the file data in the session
            if 'file_data' not in request.session:
                request.session['file_data'] = []

            # Assume you're saving files to a directory, such as 'uploaded_files'
            UPLOAD_DIR = 'uploaded_files'  # You can change this to any directory you prefer

            # Create the upload directory if it doesn't exist
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            file_data = []
            for file in files:
                try:
                    # Define the file path where you want to save the file
                    file_path = os.path.join(UPLOAD_DIR, file.name)

                    # Write the content to the file on disk
                    with open(file_path, 'wb') as f:
                        f.write(file.read())  # Write the raw file content

                    # Store the file path in the session
                    file_data.append({
                        'name': file.name,
                        'path': file_path  # Store the file path instead of content
                    })
                except Exception as e:
                    print(f"Error saving file '{file.name}': {str(e)}")

            # Store the file data in the session
            request.session['file_data'] = file_data

            # Return a response
            return JsonResponse({
                "message": "Files uploaded successfully",
                "files": [{"name": file.name} for file in files]
            })
                            
            
        elif request.content_type == "application/json":
            data = json.loads(request.body.decode('utf-8'))
            user_input = data.get("userInput")
            model_name = data.get("modelName")

            stored_file_data = request.session.get('file_data', [])
            all_files_data_str = "\n".join([f.get('content', '') for f in stored_file_data])

            if not model_name:
                model_name = "nvidia/llama-3.1-nemotron-70b-instruct"
            
            if not user_input:
                return JsonResponse({"error": "No Question Provided."}, status=400)

            for file in request.session['file_data']:
                print("Files in file data list:", file)
            
            def extract_all_files_data():
                all_data = []  

                for file in request.session['file_data']:
                    file_name = file['name']
                    file_path = file['path']
                    filename = file_name.lower()
                    
                    if filename.endswith(".txt"):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as textFile:
                                text_content = textFile.read()
                                all_data.append({
                                    'text_content': text_content
                                })
                            print(f"Total text data from {file_name}: {text_content}")
                            print("="*100 + "\n")
                        except Exception as e:
                            print(f"Error reading text file {file_name}: {e}")
                            
                    elif filename.endswith(".csv"):
                        try:
                            csvData = []
                            with open(file_path, 'r', encoding='utf-8') as file:
                                CSVreader = csv.DictReader(file)
                                for CSVrow in CSVreader:
                                    csvData.append(CSVrow)
                            print(f"Total CSV data from {file_name}: {csvData}")
                            print("="*100 + "\n")
                            all_data.append(csvData) 
                        except Exception as e:
                            print(f"Error reading CSV file {file_name}: {e}")
                            
                    elif filename.endswith(".json"):
                        try:
                            json_data = json.loads(file.read().decode('utf-8'))
                            all_data.append(json_data)
                        except Exception as e:
                            print(f"Error reading JSON file {file_name}: {e}")
                        
                    elif filename.endswith(".pdf"):
                        try:
                            pdf_reader = PyPDF2.PdfReader(file)
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text()
                            all_data.append({'pdf_data': text})
                        except Exception as e:
                            print(f"Error reading PDF file {filename}: {e}")

                return all_data

            all_files_data = extract_all_files_data()
            all_files_data_str = "\n".join([str(row) for row in all_files_data])

            if not all_files_data_str:
                print("No data extracted.")
                
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "system", "content": f"Data:\n{all_files_data_str}"},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5,
                top_p=0.7,
                max_tokens=1024,
                stream=True
            )

            return StreamingHttpResponse(generate_stream_responses(completion), content_type="text/event-stream")

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    except Exception as e:
        import traceback
        print("Error in handle_nvidia_docs_analyzer_request:", str(e))
        print(traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)
