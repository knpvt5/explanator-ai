const inputFile = document.getElementById("input_file");
const fileNameSpan = document.getElementById("file-name");
const backendAPI = "/nvidia/nvidia-docs-analyzer-api/";
const selectModel = document.querySelector('.select-model select'); // Add this line to select the model dropdown

// Default model in case no selection is made
let selectedModel = "nvidia/llama-3.1-nemotron-70b-instruct";

// Add event listener to model select to update selectedModel
selectModel.addEventListener('change', (e) => {
    selectedModel = e.target.textContent; // Use .value instead of .textContent
});

inputFile.addEventListener("change", function () {
    fileNameSpan.style.cssText = `
        width: 50px;
        overflow-x: auto;
        border: 1px solid #ccc;
    `;
    
    const file = inputFile.files[0];
    if (file) {
        fileNameSpan.textContent = file.name;
    }
    
    uploadFile();
});

function uploadFile() {
    const formData = new FormData();
    const file = inputFile.files[0];
    const userInput = document.getElementById("user-input").value || "Analyze this document";
    const botMessageBox = document.querySelector(".chat-messages .chat-message.bot") 
        || appendMessage("bot", "Generating...");

    if (file) {
        formData.append("input_file", file);
        formData.append("userInput", userInput);
        formData.append("modelName", selectedModel);

        fetch(backendAPI, {
            method: 'POST',
            body: formData,
        })
        .then(async (response) => {
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
                                // Add auto-scroll if needed
                                if (typeof autoScroll === 'function') {
                                    autoScroll();
                                }
                            } else if (jsonData.error) {
                                botMessageBox.textContent = `Error: ${jsonData.error}`;
                            }
                        } catch (parseError) {
                            console.error('JSON parsing error:', parseError);
                            botMessageBox.textContent = `Parsing Error: ${parseError.message}`;
                        }
                    }
                });
            }
        })
        .catch(error => {
            console.error("Error:", error);
            const botMessageBox = document.querySelector(".chat-messages .chat-message.bot");
            if (botMessageBox) {
                botMessageBox.textContent = `Error: ${error.message}`;
            } else {
                alert(`Error: ${error.message}`);
            }
        });
    } else {
        alert("Please select a file to upload.");
    }
}

// Helper function to append message if not already existing
function appendMessage(sender, message) {
    const messagesContainer = document.querySelector(".chat-messages");
    const messageBox = document.createElement("div");
    messageBox.classList.add("chat-message", sender);
    messageBox.textContent = message;
    messagesContainer.appendChild(messageBox);
    return messageBox;
}