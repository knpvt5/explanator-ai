// document.addEventListener("DOMContentLoaded", () => { });
    const chatBox = document.querySelector(".chat-box");
    const messagesContainer = chatBox.querySelector(".chat-messages");
    const chatBoxTextarea = document.querySelector(".chat-box textarea");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const selectModel = document.querySelector('.select-model select');
    const suggestedQuestionBox = document.querySelector(".suggested-question-box");

    // Input event for textarea with user input
    document.querySelectorAll(".suggested-question").forEach((question) => {
        question.addEventListener("click", function () {
            const questionText = this.textContent.trim();

            chatBoxTextarea.value = questionText;
            // Trigger input event manually
            chatBoxTextarea.dispatchEvent(new Event("input", { bubbles: true }));
            sendButton.click();
        });

        // Enable/Disable send button based on input
        userInput.addEventListener("input", () => {
            sendButton.disabled = userInput.value.trim() === "";
        });

    });

    function userInputTextareaAutoResize(chatBoxTextarea) {
        if (!chatBoxTextarea) return;
        chatBoxTextarea.style.height = "auto";
        chatBoxTextarea.style.height = chatBoxTextarea.scrollHeight + "px";
    }

    // Storing and getting from local storage
    userInput.addEventListener("input", (e) => {
        localStorage.setItem("nvidiaApiCbTextInput", JSON.stringify(e.target.value));
        userInputTextareaAutoResize(chatBoxTextarea)
    });
    const nvidiaApiCbTextInput = JSON.parse(localStorage.getItem("nvidiaApiCbTextInput"));
    if (nvidiaApiCbTextInput) {
        userInput.value = nvidiaApiCbTextInput;
        userInputTextareaAutoResize(chatBoxTextarea)
    }
    // Initial send button state based on input
    sendButton.disabled = !userInput.value.trim();

    let selectedModel = selectModel.value;

    selectModel.addEventListener('change', (e) => {
        selectedModel = e.target.options[e.target.selectedIndex].textContent;
        // console.log(selectedModel)
    });


    const backendAPI = "/nvidia/nvidia-api/";

    const appendMessage = (sender, message) => {
        const messageBox = document.createElement("div");
        messageBox.classList.add("chat-message", sender);
        messageBox.textContent = message;
        messagesContainer.appendChild(messageBox);
        autoScroll();
        return messageBox;
    };

    let userIsScrolling = false;
    messagesContainer.addEventListener('scroll', () => {
        if (messagesContainer.scrollTop < messagesContainer.scrollHeight - messagesContainer.clientHeight - 50) {
            userIsScrolling = true;
        } else {
            userIsScrolling = false;
        }
    });

    function autoScroll() {
        if (!userIsScrolling) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    const sendMessage = async () => {
        const user_input = userInput.value.trim();

        appendMessage("user", user_input);
        const botMessageBox = appendMessage("bot", "Generating...");

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
                    modelName: selectedModel,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

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
                                autoScroll();
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
        localStorage.removeItem("nvidiaApiCbTextInput");
        userInputTextareaAutoResize(chatBoxTextarea)
    });

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
            suggestedQuestionBox.remove();
            userInput.value = "";
            localStorage.removeItem("nvidiaApiCbTextInput");
            userInputTextareaAutoResize(chatBoxTextarea)
        }
    });

