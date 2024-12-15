// Initialize CodeMirror for each code box dynamically
const editors = []; // To store all CodeMirror instances
document.querySelectorAll(".code-box").forEach((codeBox, index) => {
    // Create a unique ID for the textarea if not already defined
    const textArea = codeBox.querySelector("textarea");
    if (textArea) {
        textArea.id = `python-code-editor-${index}`;
    }

    // Initialize CodeMirror for the current code box
    const pythonEditor = CodeMirror.fromTextArea(textArea, {
        mode: "python",
        theme: "dracula",
        lineWrapping: false,
        lineNumbers: true,
        matchBrackets: true,
        autoCloseBrackets: true,
    });

    // Store the editor instance
    editors.push(pythonEditor);

    // Get the Python file URL from the data-python-url attribute
    const pythonDataContainer = codeBox.querySelector("[data-python-url]");
    const pythonFileUrl = pythonDataContainer?.getAttribute("data-python-url");

    // Fetch and load the external Python file into the CodeMirror editor
    if (pythonFileUrl) {
        fetch(pythonFileUrl)
            .then((response) => response.text())
            .then((code) => {
                pythonEditor.setValue(code); // Load fetched content into the editor
            })
            .catch((error) => {
                console.error(`Error fetching the Python file for code box ${index}:`, error);
            });
    } else {
        console.error(`Python file URL is not defined for code box ${index}.`);
    }

    // Add event listener to the copy button inside this code box
    const copyButton = codeBox.querySelector(".copy-code-btn");
    copyButton.addEventListener("click", function () {
        const codeContent = pythonEditor.getValue(); // Get content from the current CodeMirror editor
        const tempElement = document.createElement("textarea");
        tempElement.value = codeContent;

        document.body.appendChild(tempElement);
        tempElement.select();
        document.execCommand("copy");
        document.body.removeChild(tempElement);

        // Update button appearance or show a success message
        copyButton.innerHTML = "<i class='fa-solid fa-check'></i>";
        setTimeout(() => {
            copyButton.innerHTML = "<i class='fa-regular fa-copy'></i>";
        }, 2000); 
    });
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
