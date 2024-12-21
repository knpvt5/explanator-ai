import os
from django.http import JsonResponse, StreamingHttpResponse
import google.generativeai as genai
import csv
import json
import PyPDF2
import logging

# Configure logging to display messages to the terminal
logging.basicConfig(
    level=logging.DEBUG,  
    format=' %(levelname)s - %(message)s - %(name)s -%(asctime)s ', 
)

# Initialize logging
logger = logging.getLogger(__name__)

def handle_gemini_docs_analyzer_request(request, model, generate_stream_responses):
    try:
        files = []
        user_input = None
        file_data = []

        # Initialize session storage if it doesn't exist
        if 'file_data' not in request.session:
            request.session['file_data'] = []

        # Handle file upload request
        if request.FILES:
            files = request.FILES.getlist('input_file')
            logging.info(f"Files received: {[file.name for file in files]}")

            UPLOAD_DIR = '/data/site_data'
            os.makedirs(UPLOAD_DIR, exist_ok=True)
        
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
            
        elif request.content_type == "application/json":
            body = json.loads(request.body.decode("utf-8"))
            user_input = body.get("user_input", "")

            if not user_input:
                logging.warning("User input is missing in the request body.")
                return JsonResponse({"error": "User input is required."}, status=400)
            
        
        all_Data = []

        for file in request.session.get('file_data'):
            filename = file.get("path")
            file_path = file.get("path")
            logging.info("filename:", file)
            
            try:
                if filename.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as file:
                        text_content = file.read()
                        all_Data.append(text_content)
                        # print(f"txt file data: {text_content}\n")
                        logging.info(f"Successfully read text file: {filename}")

                elif filename.endswith(".csv"):
                    csvData = []
                    with open(file_path, "r", encoding="utf-8") as csvFile:
                        CSVreader = csv.DictReader(csvFile)
                        for CSVrow in CSVreader:
                            csvData.append(CSVrow)
                        # print(f"CSV file data: {csvData}\n")
                        all_Data.append(csvData)
                        logging.info(f"Successfully read CSV file: {filename}")

                elif filename.endswith(".json"):
                    jsonData = []
                    with open(file_path, "r", encoding="utf-8") as jsonFile:
                        JSONreader = json.load(jsonFile)
                        for JSONrow in JSONreader:
                            jsonData.append(JSONrow)
                        # print(f"json file data: {jsonData}\n")
                        all_Data.append(jsonData)
                        logging.info(f"Successfully read JSON file: {filename}")

                elif filename.endswith(".pdf"):
                    pdfData = []
                    with open(file_path, "rb") as pdfFile:
                        PDFreader = PyPDF2.PdfReader(pdfFile)
                        for page in PDFreader.pages:
                            text = page.extract_text()
                            pdfData.append(text)
                        # print(f"pdf file data: {pdfData}\n")
                        all_Data.append(pdfData)
                        logging.info(f"Successfully read PDF file: {filename}")

                else:
                    logging.warning(f"Unsupported file format: {filename}")

            except FileNotFoundError:
                logging.error(f"Error: File not found at path '{filename}'. Please ensure the file exists.")

        # Convert all data to string format
        all_Data_str = str(all_Data) if all_Data else ""
        logging.info("All data converted to string format.")

        if not all_Data_str:
            logging.warning("No data extracted. Continuing without any Data provided...")
        try:
            # Generate content using the text data as context
            prompt = (
                "You are a helpful assistant. "
                # "Do not answer any questions that are not based on the data. "
                f"Data:\n{all_Data_str}\n\n"
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
            logging.error(f"An error occurred while generating content: {str(e)}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    except json.JSONDecodeError:
        logging.error("Invalid JSON in request body.")
        return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
