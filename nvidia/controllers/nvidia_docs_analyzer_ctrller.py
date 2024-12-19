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
        # Initialize session storage if it doesn't exist
        if 'file_data' not in request.session:
            request.session['file_data'] = []

        # Handle file upload request
        if request.FILES:
            files = request.FILES.getlist('input_file')
            print(f"Files received: {[file.name for file in files]}")

            UPLOAD_DIR = 'static/data'
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            file_data = []
            for file in files:
                try:
                    file_path = os.path.join(UPLOAD_DIR, file.name)
                    
                    # Save file to disk
                    with open(file_path, 'wb+') as f:
                        for chunk in file.chunks():
                            f.write(chunk)

                    file_data.append({
                        'name': file.name,
                        'path': file_path
                    })
                except Exception as e:
                    print(f"Error saving file '{file.name}': {str(e)}")
                    return JsonResponse({"error": f"Error saving file '{file.name}': {str(e)}"}, status=500)

            # Update session with new file data
            request.session['file_data'] = file_data

            return JsonResponse({
                "message": "Files uploaded successfully",
                "files": [{"name": file.name} for file in files]
            })
            

        # Handle analysis request
        elif request.content_type == "application/json":
            data = json.loads(request.body.decode('utf-8'))
            user_input = data.get("userInput")
            model_name = data.get("modelName")

            if not model_name:
                model_name = "nvidia/llama-3.1-nemotron-70b-instruct"
            
            if not user_input:
                return JsonResponse({"error": "No Question Provided."}, status=400)

            # If no files are uploaded, skip file extraction logic
            all_files_data_str = ""
            if 'file_data' in request.session and request.session['file_data']:
                def extract_all_files_data():
                    all_data = []
                    for file_info in request.session['file_data']:
                        print("files in the list", file_info)
                        try:
                            file_path = file_info['path']
                            if not os.path.exists(file_path):
                                print(f"File not found: {file_path}")
                                continue

                            filename = file_info['name'].lower()
                            
                            if filename.endswith(".txt"):
                                with open(file_path, 'r', encoding='utf-8') as textFile:
                                    text_content = textFile.read()
                                    all_data.append({
                                        'filename': filename,
                                        'text_content': text_content
                                    })

                            elif filename.endswith(".csv"):
                                csvData = []
                                with open(file_path, 'r', encoding='utf-8') as file:
                                    CSVreader = csv.DictReader(file)
                                    csvData = [row for row in CSVreader]
                                all_data.append({
                                    'filename': filename,
                                    'csv_data': csvData
                                })

                            elif filename.endswith(".json"):
                                with open(file_path, 'r', encoding='utf-8') as file:
                                    json_data = json.load(file)
                                    all_data.append({
                                        'filename': filename,
                                        'json_data': json_data
                                    })

                            elif filename.endswith(".pdf"):
                                with open(file_path, 'rb') as file:
                                    pdf_reader = PyPDF2.PdfReader(file)
                                    text = ""
                                    for page in pdf_reader.pages:
                                        text += page.extract_text()
                                    all_data.append({
                                        'filename': filename,
                                        'pdf_data': text
                                    })

                        except Exception as e:
                            print(f"Error processing file {file_info['name']}: {str(e)}")
                            continue

                    return all_data

                all_files_data = extract_all_files_data()

                if all_files_data:
                    all_files_data_str = "\n".join([str(data) for data in all_files_data])
                else:
                    return JsonResponse({"error": "No data could be extracted from the uploaded files."}, status=400)

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

