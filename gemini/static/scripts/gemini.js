let pythonEditor;

// document.addEventListener("DOMContentLoaded", () => {
// Select textarea and CodeMirror setup
const textarea = document.getElementById("user-input");

document.getElementById("expand-collapse-btn").addEventListener("click", function () {
    const content = document.querySelector(".content");
    const chatBox = document.querySelector(".chat-box");
    const chatMessages = document.querySelector(".chat-messages");
    const expandCollapseBtn = document.getElementById("expand-collapse-btn");

    function toggleExpandCollapse() {
        if (window.innerWidth > 480) {
            content.classList.toggle("content-expand");
            chatBox.classList.toggle("chat-box-expand");
            chatMessages.classList.toggle("chat-messages-expand");
        } else {
            content.classList.remove("content-expand");
            chatBox.classList.remove("chat-box-expand");
            chatMessages.classList.remove("chat-messages-expand");
        }

        if (chatBox.classList.contains("chat-box-expand")) {
            expandCollapseBtn.innerHTML = '<i class="fa-solid fa-down-left-and-up-right-to-center"></i>';
            sessionStorage.setItem("ExpandCollapseBtn", true);
        } else {
            expandCollapseBtn.innerHTML = '<i class="fa-solid fa-up-right-and-down-left-from-center"></i>';
            sessionStorage.removeItem("ExpandCollapseBtn");
        }
    }

    toggleExpandCollapse();

    window.addEventListener("resize", function () {
        if (window.innerWidth < 480) {
            toggleExpandCollapse();
        }
    });

});

if (JSON.parse(sessionStorage.getItem("ExpandCollapseBtn")) === true) {
    document.getElementById("expand-collapse-btn").click();
}

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
        this.innerHTML = '<i class="fa-solid fa-copy"></i>';
        console.log("Code copied to clipboard!");
        setTimeout(() => {
            this.innerHTML = '<i class="fa-regular fa-copy"></i>';
        }, 3000);
    }).catch((error) => {
        console.error("Error copying to clipboard:", error);
    });
});


// Handle file input changes
const inputFile = document.getElementById("input_file");
if (inputFile) {
    inputFile.addEventListener('change', fileInputNameChange);
}

// Initialize MutationObserver for textarea change
/* const observer = new MutationObserver(() => fileInputNameChange());
observer.observe(pythonEditor, { childlist: true, characterData: true, subtree: true }); */

if (inputFile) {
    setTimeout(() => {
        fileInputNameChange();
    }, 5000);
}


// });

function fileInputNameChange() {
    try {
        const geminiFileUploaded = JSON.parse(localStorage.getItem('geminiFileUploaded'));
        if (!geminiFileUploaded) {
            return;
        }
        console.log(geminiFileUploaded);

        // Get content from CodeMirror  
        const existingCode = pythonEditor.getValue();

        // Name file in codemirror
        const updatedCode = existingCode.replace(
            /files\s*=\s* .*/,
            `files = ["${geminiFileUploaded}"]`
        );

        StoreCodeMirrorScrollAndCursor(updatedCode);

    } catch (error) {
        console.error('Error during file input CodeMirror change:', error);
    }
}

function StoreCodeMirrorScrollAndCursor(updatedCode) {
    // Save the scroll positions
    const scrollPosition = pythonEditor.getScrollInfo().top;

    // Set the updated code
    pythonEditor.setValue(updatedCode);

    // Restore scroll positions
    pythonEditor.scrollTo(0, scrollPosition);
}

// CodeBox Update
const selectModel = document.querySelector('.select-model');
const chatBoxTextarea = document.querySelector(".chat-box textarea");

chatBoxTextarea.addEventListener('input', (event) => {
    const userInput = event.target.value;

    const existingCode = pythonEditor.getValue();
    const updatedCode = existingCode.replace(
        /user_input = .*/,
        `user_input = "${userInput}"`
    );

    StoreCodeMirrorScrollAndCursor(updatedCode);
});

selectModel.addEventListener('change', (event) => {
    const selectedModel = event.target.options[event.target.selectedIndex].textContent;
    console.log(selectedModel);

    const existingCode = pythonEditor.getValue();
    const updatedCode = existingCode.replace(
        /model\s*=\s* .*/,
        `model = "${selectedModel}"`
    );

    StoreCodeMirrorScrollAndCursor(updatedCode);
});

// Initialize CodeMirror for Markdown Editor
const markdownPreviewDiv = document.getElementById("markdown-preview");
const MDdataContainer = document.getElementById("markdown-data-container");
const markdownUrl = MDdataContainer.getAttribute("data-markdown-url");
const viewDocsBtn = document.querySelector(".view-docs-btn");

// Function to fetch and render markdown content
async function loadMarkdownContent() {
    try {
        const response = await fetch(markdownUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const markdownContent = await response.text();

        // Parse and render the Markdown content
        MDdataContainer.innerHTML = marked.parse(markdownContent);
    } catch (error) {
        console.error("Error loading markdown:", error);
        MDdataContainer.innerHTML = '<p class="error">Error loading documentation</p>';
    }
}
loadMarkdownContent();

viewDocsBtn.addEventListener("click", () => {
    console.log("viewDocsBtn clicked");
    MDdataContainer.style.display = MDdataContainer.style.display === "block" ? "none" : "block";
    if (MDdataContainer.style.display === "block") {
        viewDocsBtn.innerHTML = "<i class='fa-solid fa-chevron-up'></i>";
    } else {
        viewDocsBtn.innerHTML = "<i class='fa-solid fa-chevron-down'></i>";
    }
})
