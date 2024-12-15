document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.querySelector(".chat-box");
    const messagesContainer = chatBox.querySelector(".chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    const backendAPI = "/gemini/gemini-json-reader-api/";

    const appendMessage = (sender, message) => {
        const messageBox = document.createElement("div");
        messageBox.classList.add("chat-message", sender);
        messageBox.textContent = message;
        messagesContainer.appendChild(messageBox);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return messageBox;
    };

    const sendMessage = async () => {
        const question = userInput.value.trim();
        if (!question) return;

        // Add user message
        appendMessage("user", question);

        // Create bot message container
        const botMessageBox = appendMessage("bot", ""); // Empty container for streaming

        // Disable input during processing
        userInput.disabled = true;
        sendButton.disabled = true;

        try {
            const csrfToken = getCookie("csrftoken");
            const response = await fetch(backendAPI, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ question }),
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
            console.error("Error:", error);
            botMessageBox.textContent = `Error: ${error.message}`;
        } finally {
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.value = ""; 
            userInput.focus(); 
            if(window.innerWidth < 768) {
                userInput.blur();
            }
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


    const suggestedQuestionBox = document.querySelector(".suggested-question-box");
    function hideSuggestionBox() {
        if (suggestedQuestionBox) {
            suggestedQuestionBox.style.display = "none";
        }
    }

    sendButton.addEventListener("click", () => {
        sendMessage();
        hideSuggestionBox();
        userInput.value = "";
    });

    userInput.addEventListener("keydown", (e) => {
        // Handle Enter key without Shift 
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
            hideSuggestionBox();
            userInput.value = "";
        }
    });

});

