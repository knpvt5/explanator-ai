document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.querySelector(".chat-box");
    const messagesContainer = chatBox.querySelector(".chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    const suggestedQuestionBox = document.querySelector(".suggested-question-box");

    const backendAPI = "/data_sets/nvidia-raw-dataset-reader-api/";

    const appendMessage = (sender, message) => {
        const messageBox = document.createElement('div');
        messageBox.classList.add("chat-message", sender);
        messageBox.textContent = message;
        messagesContainer.appendChild(messageBox)
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return messageBox;
    };

    const sendMessage = async () => {
        const userMessage = userInput.value;
        if (!userMessage) return;

        appendMessage("user", userMessage)
        const botMessageBox = appendMessage("bot", "Generating...")

        try {
            const csrfToken = getCookie("csrftoken");
            const response = await fetch(backendAPI, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({
                    "userInput": userMessage
                })
            });


            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Handle streaming response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let responseText = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split("\n");

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        try {
                            const data = JSON.parse(line.slice(5));
                            if (data.chunk) {
                                responseText += data.chunk;
                                // Use marked to parse and render markdown in real-time
                                botMessageBox.innerHTML = marked.parse(responseText);
                                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                            }
                        } catch (e) {
                            console.error("Error parsing chunk:", e);
                        }
                    }
                }
            }
        } catch (error) {
            botMessageBox.textContent = "An error occurred. Please try again.";
            console.error("Error occurred:", error);
        } finally {
            userInput.value = "";
            userInput.disabled = false;
            sendButton.disabled = true;
            userInput.focus();
        }
    };

    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    // event for send button click
    sendButton.addEventListener("click", () => {
        sendMessage();
        suggestedQuestionBox.remove();
        userInput.value = "";
    });

    userInput.addEventListener("keydown", (e) => {
        // Handle Enter key without Shift 
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
            suggestedQuestionBox.remove();
            userInput.value = "";
        }
    });

});