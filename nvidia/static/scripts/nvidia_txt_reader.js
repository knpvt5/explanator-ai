document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.querySelector(".chat-box");
    const messagesContainer = chatBox.querySelector(".chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    const backendAPI = "/nvidia/nvidia-txt-reader-api/";

    const appendMessage = (sender, message) => {
        const messageBox = document.createElement("div");
        messageBox.classList.add("chat-message", sender);
        messageBox.textContent = message;
        messagesContainer.appendChild(messageBox);
        autoScroll()
        return messageBox;
    };

    let userIsScrolling = false;
    // Add an event listener to detect when the user scrolls manually
    messagesContainer.addEventListener('scroll', () => {
        // Check if the user has scrolled up from the bottom
        if (messagesContainer.scrollTop < messagesContainer.scrollHeight - messagesContainer.clientHeight - 50) {
            userIsScrolling = true; 
        } else {
            userIsScrolling = false; 
        }
    });
    // auto-scrolling function
    function autoScroll() {
        // Check if the user is not scrolling
        if (!userIsScrolling) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    const sendMessage = async () => {
        const question = userInput.value.trim();

        // Add user message
        appendMessage("user", question);

        // Create bot message container
        const botMessageBox = appendMessage("bot", "");

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

            // Use EventSource for streaming
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let responseText = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                lines.forEach(line => {
                    if (line.startsWith('data: ')) {
                        try {
                            const jsonData = JSON.parse(line.slice(6));
                            if (jsonData.chunk) {
                                responseText += jsonData.chunk;
                                botMessageBox.innerHTML = marked.parse(responseText);
                                autoScroll()
                            }
                        } catch (parseError) {
                            console.error('JSON parsing error:', parseError);
                        }
                    }
                });
            }

        } catch (error) {
            console.error("Error:", error);
            botMessageBox.textContent = `Error: ${error.message}`;
        } finally {
            userInput.value = "";
            userInput.disabled = false;
            sendButton.disabled = true;
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
