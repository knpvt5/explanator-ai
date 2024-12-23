document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.querySelector(".chat-box");
    const messagesContainer = chatBox.querySelector(".chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const suggestedQuestionBox = document.querySelector(".suggested-question-box");

    // Input event for textarea with user input
    document.querySelectorAll(".suggested-question").forEach((question) => {
        question.addEventListener("click", function () {
            const questionText = this.textContent.trim();
            const chatBoxTextarea = document.querySelector(".chat-box textarea");

            chatBoxTextarea.value = questionText;
            // manual Trigger 
            chatBoxTextarea.dispatchEvent(new Event("input", { bubbles: true }));
            sendButton.click();
        });

        // Enable/Disable send button based on input
        userInput.addEventListener("input", () => {
            sendButton.disabled = userInput.value.trim() === "";
        });
    });

    // Storing and getting from local storage
    userInput.addEventListener("input", (e) => {
        localStorage.setItem("geminiApiCbTextInput", JSON.stringify(e.target.value));
    });
    const geminiApiCbTextInput = JSON.parse(localStorage.getItem("geminiApiCbTextInput"));
    if (geminiApiCbTextInput) {
        userInput.value = geminiApiCbTextInput;

    }
    // Initial send button state based on input
    sendButton.disabled = !userInput.value.trim();


    const backendAPI = "/gemini/gemini-api/";

    const appendMessage = (sender, message, parsed = false) => {
        const messageBox = document.createElement("div");
        messageBox.classList.add("chat-message", sender);

        if (parsed) {
            // Use marked to parse markdown
            messageBox.innerHTML = marked.parse(message);
        } else {
            messageBox.textContent = message;
        }

        messagesContainer.appendChild(messageBox);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return messageBox;
    };

    const sendMessage = async () => {
        const user_input = userInput.value.trim();
        if (!user_input) return;

        // Add user message
        appendMessage("user", user_input);

        // Create bot message container
        const botMessageBox = appendMessage("bot", "Generating...", true); // Note the 'true' to enable markdown parsing

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
                body: JSON.stringify({
                    userInput: user_input,
                }),
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
            console.error("Error:", error);
            botMessageBox.textContent = `Error: ${error.message}`;
        } finally {
            userInput.disabled = false;
            userInput.value = "";
            userInput.focus();
            if (window.innerWidth < 768) {
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


    sendButton.addEventListener("click", () => {
        sendMessage();
        suggestedQuestionBox.remove();
        userInput.value = "";
        localStorage.removeItem("geminiApiCbTextInput");
    });

    userInput.addEventListener("keydown", (e) => {
        // Handle Enter key without Shift 
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
            suggestedQuestionBox.remove();
            userInput.value = "";
            localStorage.removeItem("geminiApiCbTextInput");
        }
    });

});

