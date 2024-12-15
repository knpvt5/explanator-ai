// Initialize CodeMirror for Python Editor
const pythonEditor = CodeMirror.fromTextArea(document.getElementById("python-code-editor"), {
    mode: "python",
    theme: "dracula",
    lineWrapping: false,
    lineNumbers: true,
    matchBrackets: true,
    autoCloseBrackets: true,
});

// Get the Python file URL from the data-container element
const pythonFileUrl = document.getElementById('python-data-container').getAttribute('data-python-url');

// Fetch the external Python file and load it into the CodeMirror editor
if (pythonFileUrl) {
    fetch(pythonFileUrl)
        .then((response) => response.text())
        .then((code) => {
            pythonEditor.setValue(code); // Load fetched content into CodeMirror
        })
        .catch((error) => {
            console.error('Error fetching the Python file:', error);
        });
} else {
    console.error("Python file URL is not defined.");
}

// Copy Code Button
document.getElementById("copy-code-btn").addEventListener("click", function () {
    const copyButton = document.getElementById("copy-code-btn");
    const codeContent = pythonEditor.getValue(); // Get content from CodeMirror
    const tempElement = document.createElement("textarea");
    tempElement.value = codeContent;

    document.body.appendChild(tempElement);
    tempElement.select();
    document.execCommand("copy");
    document.body.removeChild(tempElement);

    copyButton.innerHTML = "<i class='fa-solid fa-copy'></i>";

});


document.querySelectorAll(".suggested-question").forEach((question) => {
    const sendButton = document.getElementById("send-button");
    const userInput = document.getElementById("user-input");


    question.addEventListener("click", function () {
        const question = this.textContent.trim(); // Get the clicked question's text
        const chatBoxTextarea = document.querySelector(".chat-box textarea");

        chatBoxTextarea.value = question; // Set the text area value to the question

        // Manually trigger the input event
        const inputEvent = new Event("input", { bubbles: true });
        chatBoxTextarea.dispatchEvent(inputEvent);
        sendButton.click();
    });

    // Enable/Disable send button based on input
    userInput.addEventListener("input", () => {
        sendButton.disabled = userInput.value.trim() === "";
    });

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && e.shiftKey) {
            e.preventDefault();
            e.stopPropagation();
            return;
        }

        // Handle Enter key without Shift 
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
        }
    });

    // Initialize send button state
    sendButton.disabled = true; // Initially disabled
});


// Chat Box Update
const chatBoxTextarea = document.querySelector(".chat-box textarea");
chatBoxTextarea.addEventListener("input", (event) => {
    const userInput = event.target.value;
    const existingCode = pythonEditor.getValue();

    // Update `user_question` in CodeMirror
    const updatedCode = existingCode.replace(
        /user_input = .*/,
        `user_input = "${userInput}"`
    );
    pythonEditor.setValue(updatedCode);
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
