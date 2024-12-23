let pythonEditor; 

document.addEventListener("DOMContentLoaded", () => {
    // Select textarea and CodeMirror setup
    const textarea = document.getElementById("user-input");
    pythonEditor = CodeMirror.fromTextArea(document.getElementById("python-code-editor"), {
        mode: "python",
        theme: "dracula",
        lineWrapping: false,
        lineNumbers: true,
        matchBrackets: true,
        autoCloseBrackets: true,
    });

    // Fetch external Python code and load into CodeMirror
    const pythonFileUrl = document.getElementById('python-data-container').getAttribute('data-python-url');
    if (pythonFileUrl) {
        fetch(pythonFileUrl)
            .then((response) => response.text())
            .then((code) => {
                pythonEditor.setValue(code);
            })
            .catch((error) => {
                console.error('Error fetching the Python file:', error);
            });
    }

    // Copy code button functionality
    document.getElementById("copy-code-btn").addEventListener("click", function () {
        const codeContent = pythonEditor.getValue();
        navigator.clipboard.writeText(codeContent).then(() => {
            console.log("Code copied to clipboard!");
        }).catch((error) => {
            console.error("Error copying to clipboard:", error);
        });
    });

    // Input event for textarea with user input
    document.querySelectorAll(".suggested-question").forEach((question) => {
        const sendButton = document.getElementById("send-button");

        question.addEventListener("click", function () {
            const questionText = this.textContent.trim();
            const chatBoxTextarea = document.querySelector(".chat-box textarea");

            chatBoxTextarea.value = questionText;

            // Trigger input event manually
            chatBoxTextarea.dispatchEvent(new Event("input", { bubbles: true }));
            sendButton.click();
        });

        // Enable/Disable send button based on input
        const userInput = document.getElementById("user-input");
        userInput.addEventListener("input", () => {
            sendButton.disabled = userInput.value.trim() === "";
        });

        sendButton.disabled = true;
    });

    // Handle file input changes
    const inputFile = document.getElementById("input_file");
    const removeFile = document.getElementById("remove-file");
    inputFile.addEventListener('change', fileInputNameChange);
    removeFile.addEventListener('click', fileInputNameChange);

    // Initialize MutationObserver for textarea change
    /* const observer = new MutationObserver(() => fileInputNameChange());
    observer.observe(pythonEditor, { childlist: true, characterData: true, subtree: true }); */

    setTimeout(() => {
        fileInputNameChange();
    }, 5000);

});

function fileInputNameChange() {
    try {
        const nvidiaFileUploaded = JSON.parse(localStorage.getItem('nvidiaFileUploaded'));
        if (!nvidiaFileUploaded) {
            return;
        }
        console.log(nvidiaFileUploaded);

        // Get the current content of the CodeMirror editor
        const existingCode = pythonEditor.getValue();

        // Replace the old file path with the new one
        const updatedCode = existingCode.replace(
            /files\s*=\s* .*/,
            `files = ["${nvidiaFileUploaded}"]`
        );

        // Save the current cursor and scroll positions
        const cursorPosition = pythonEditor.getCursor();
        const scrollPosition = pythonEditor.getScrollInfo().top;

        // Set the updated code
        pythonEditor.setValue(updatedCode);

        // Restore cursor and scroll positions
        pythonEditor.setCursor(cursorPosition);
        pythonEditor.scrollTo(0, scrollPosition);
    } catch (error) {
        console.error('Error during file input CodeMirror change:', error);
    }
}

// Chat Box Update
const selectModel = document.querySelector('.select-model');
const chatBoxTextarea = document.querySelector(".chat-box textarea");

chatBoxTextarea.addEventListener('input', (event) => {
    const userInput = event.target.value;

    const existingCode = pythonEditor.getValue();
    const updatedCode = existingCode.replace(
        /user_input = .*/,
        `user_input = "${userInput}"`
    );
    // Save the current cursor and scroll positions
    const cursorPosition = pythonEditor.getCursor();
    const scrollPosition = pythonEditor.getScrollInfo().top;

    // Set the updated code
    pythonEditor.setValue(updatedCode);

    // Restore cursor and scroll positions
    pythonEditor.setCursor(cursorPosition);
    pythonEditor.scrollTo(0, scrollPosition);
});

selectModel.addEventListener('change', (event) => {
    const selectedModel = event.target.options[event.target.selectedIndex].textContent;
    console.log(selectedModel);

    const existingCode = pythonEditor.getValue();
    const updatedCode = existingCode.replace(
        /model\s*=\s* .*/,
        `model = "${selectedModel}"`
    );
    // Save the current cursor and scroll positions
    const cursorPosition = pythonEditor.getCursor();
    const scrollPosition = pythonEditor.getScrollInfo().top;

    // Set the updated code
    pythonEditor.setValue(updatedCode);

    // Restore cursor and scroll positions
    pythonEditor.setCursor(cursorPosition);
    pythonEditor.scrollTo(0, scrollPosition);
});

// Initialize CodeMirror for Markdown Editor
const markdownPreviewDiv = document.getElementById("markdown-preview");
const dataContainer = document.getElementById("markdown-data-container");
const markdownUrl = dataContainer.getAttribute("data-markdown-url");

// Function to fetch and render markdown content
async function loadMarkdownContent() {
    try {
        const response = await fetch(markdownUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const markdownContent = await response.text();

        // Parse and render the Markdown content
        markdownPreviewDiv.innerHTML = marked.parse(markdownContent);
    } catch (error) {
        console.error("Error loading markdown:", error);
        markdownPreviewDiv.innerHTML = '<p class="error">Error loading documentation</p>';
    }
}

// Load and render the Markdown content on page load
loadMarkdownContent();
