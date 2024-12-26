let pythonEditor;

document.addEventListener("DOMContentLoaded", () => {
    // userInputTextarea and CodeMirror setup
    const textarea = document.getElementById("user-input");

    document.getElementById("expand-collapse-btn").addEventListener("click", function () {
        const content = document.querySelector(".content");
        const chatBox = document.querySelector(".chat-box");
        const chatMessages = document.querySelector(".chat-messages");
        const expandCollapseBtn = document.getElementById("expand-collapse-btn");

        function toggleExpandCollapse() {
            toggleExpandCollapse = !toggleExpandCollapse;
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
                let ExpandCollapseBtn = true
                localStorage.setItem("ExpandCollapseBtn", JSON.stringify(ExpandCollapseBtn));
            } else {
                expandCollapseBtn.innerHTML = '<i class="fa-solid fa-up-right-and-down-left-from-center"></i>';
                localStorage.removeItem("ExpandCollapseBtn");
            }
        }

        toggleExpandCollapse();

        window.addEventListener("resize", function () {
            toggleExpandCollapse();
        });

    });

    window.addEventListener("resize", function () {
        if (window.innerWidth < 480) {
            document.getElementById("expand-collapse-btn").click();
        }
    });

    if (JSON.parse(localStorage.getItem("ExpandCollapseBtn")) === true) {
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
            console.log("Code copied to clipboard!");
        }).catch((error) => {
            console.error("Error copying to clipboard:", error);
        });
    });


    // Handle file input changes
    const inputFile = document.getElementById("input_file");
    inputFile.addEventListener('change', fileInputNameChange);

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

        // Get content from CodeMirror
        const existingCode = pythonEditor.getValue();

        // Name file in codemirror
        const updatedCode = existingCode.replace(
            /files\s*=\s* .*/,
            `files = ["${nvidiaFileUploaded}"]`
        );

        StoreCodeMirrorScrollAndCursor(updatedCode)

    } catch (error) {
        console.error('Error during file input CodeMirror change:', error);
    }
}

function StoreCodeMirrorScrollAndCursor(updatedCode) {
    // Save the scroll positions
    const scrollPosition = pythonEditor.getScrollInfo().top;

    // Set the updated code
    pythonEditor.setValue(updatedCode);

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

    pythonEditor.setValue(updatedCode);


    StoreCodeMirrorScrollAndCursor(updatedCode);
});



selectModel.addEventListener('change', (event) => {
    const selectedModel = event.target.options[event.target.selectedIndex].textContent;

    const existingCode = pythonEditor.getValue();
    const updatedCode = existingCode.replace(
        /model\s*=\s* .*/,
        `model = "${selectedModel}"`
    );

    StoreCodeMirrorScrollAndCursor(updatedCode)

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

// on Load render the Markdown content
loadMarkdownContent();
