import json
from django.http import JsonResponse, StreamingHttpResponse

def handle_nvidia_api_cb_request(request, client, generate_stream_responses):
    try:
        # Parse the JSON payload
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get("userInput")
        model_name = data.get("modelName")

        if not user_input:
            return JsonResponse({"error": "No Question Provided."}, status=400)

        if not model_name:
            model_name = "nvidia/llama-3.1-nemotron-70b-instruct"

        if not client:
            return JsonResponse({"error": "Service not available"}, status=503)

        # Create a streaming chat completion request
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
            stream=True
        )

        # Return a streaming response
        return StreamingHttpResponse(
            generate_stream_responses(response),
            content_type='text/event-stream'
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
