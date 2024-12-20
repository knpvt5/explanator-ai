import json
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
import google.generativeai as genai


def handle_gemini_api_cb_request(request, model, generate_stream_responses):
    if request.method == "POST":
        try:
            # Parse and validate the request body
            body = json.loads(request.body)
            user_input = body.get("question", "")
            if not user_input:
                return JsonResponse({"error": "No question provided"}, status=400)

            # Define safety settings
            safety_settings = [
                {"category": "HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            ]

            # Generate response using the model
            try:
                response = model.generate_content(
                    user_input,
                    generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
                    safety_settings=safety_settings,
                    stream=True,
                )

                # Stream the response back to the client
                return StreamingHttpResponse(
                    generate_stream_responses(response),
                    content_type    ="text/event-stream",
                )

            except Exception as model_error:
                return JsonResponse({"error": f"Model Error: {str(model_error)}"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
        
        except Exception as general_error:
            return JsonResponse({"error": f"Unexpected Error: {str(general_error)}"}, status=500)

    # Return error for non-POST requests
    return JsonResponse({"error": "Invalid request method"}, status=405)
