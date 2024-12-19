document.addEventListener("DOMContentLoaded", () => {
    const inputFile = document.getElementById("input_file");
    const fileNameSpan = document.getElementById("file-name");
    const chatBox = document.querySelector(".chat-box");
    const messagesContainer = chatBox.querySelector(".chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const selectModel = document.querySelector('.select-model select');
    const suggestedQuestionBox = document.querySelector(".suggested-question-box");

    let selectedModel = selectModel.value; // Set initial global model
    const backendAPI = "/nvidia/nvidia-docs-analyzer-api/";

    let fileUploaded = false;

    // File upload event handling
    inputFile.addEventListener("change", function () {
        fileNameSpan.style.cssText = `
            width: 50px;
            overflow-x: auto;
            border: 1px solid #ccc;
        `;
        const file = inputFile.files[0];
        console.log("File being uploaded:", inputFile.files[0]);
        if (file) {
            fileNameSpan.textContent = file.name;
        }
        uploadFile();
    });

    const uploadFile = () => {
        const formData = new FormData();
        const file = inputFile.files[0];
    
        if (file) {
            formData.append("input_file", file); // Make sure the key matches your backend
    
            console.log([...formData.entries()]); // Debug: Log formData entries
    
            fetch(backendAPI, {
                method: 'POST',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"), // Only include CSRF token
                },
                body: formData,
            })
                .then(async response => {
                    const data = await response.json();
                    if (!response.ok) {
                        throw new Error(data.error || `HTTP error! status: ${response.status}`);
                    }
                    console.log('File upload success:', data);
                    alert('File uploaded successfully!');
                })
                .catch(error => {
                    console.error('File upload error:', error);
                    alert(`Failed to upload file: ${error.message}`);
                });
        } else {
            alert("Please select a file to upload.");
        }
    };
    

    // Model selection handling
    selectModel.addEventListener('change', (e) => {
        selectedModel = e.target.options[e.target.selectedIndex].textContent;
    });

    // ChatBox functionality
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

    const autoScroll = () => {
        if (!userIsScrolling) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    };

    const sendMessage = async () => {
        const question = userInput.value.trim();

        appendMessage("user", question);
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
                    userInput: question,
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
            // sendButton.disabled = false;
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
    });

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
            suggestedQuestionBox.remove();
            userInput.value = "";
        }
    });
});
