document.addEventListener("DOMContentLoaded", () => {
    const menuBtn = document.querySelector(".menu-btn");
    const leftAside = document.querySelector(".left-aside");

    menuBtn.addEventListener("click", (e) => {
        if (window.innerWidth > 480) {
            leftAside.classList.toggle("menu-close");
        } else {
            e.stopPropagation();
            leftAside.classList.toggle("menu-slide");
        }

        // Update the menu button icon
        function updateMenuButtonIcon() {
            if ((leftAside.classList.contains("menu-close")) && (window.innerWidth > 480)) {
                menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            } else if ((!leftAside.classList.contains("menu-slide")) && (window.innerWidth < 480)) {
                menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            } else {
                menuBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
            }
        }
        updateMenuButtonIcon();

        // Close sidebar when clicking outside
        document.addEventListener('click', function (e) {
            if (!leftAside.contains(e.target) && !menuBtn.contains(e.target) && (leftAside.classList.contains("menu-slide"))) {
                leftAside.classList.remove('menu-slide');
                updateMenuButtonIcon();
            }
        });
    });

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

    });

    function aiOptionMenu() {
        const aiOptionBtn = document.querySelectorAll(".ai-options-btn");
        const aiOptions = document.querySelectorAll(".ai-options");

        aiOptionBtn.forEach((btn, index) => {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                const currentOptions = aiOptions[index];
                currentOptions.style.display = currentOptions.style.display === "block" ? "none" : "block";
                function updateAiOptionsBtnIcon() {
                    if (currentOptions.style.display === "block") {
                        btn.innerHTML = "<i class='fa-regular fa-circle-xmark'></i>";
                    } else {
                        btn.innerHTML = "<i class='fa-solid fa-ellipsis-vertical'></i>";
                    }
                }
                updateAiOptionsBtnIcon();
                document.addEventListener('click', (e) => {
                    if (!currentOptions.contains(e.target) && !btn.contains(e.target)) {
                        currentOptions.style.display = "none";
                        updateAiOptionsBtnIcon();
                    }
                });
            });
        });
    }

    aiOptionMenu();


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
        MDdataContainer.style.display = MDdataContainer.style.display === "block" ? "none" : "block";
        if (MDdataContainer.style.display === "block") {
            viewDocsBtn.innerHTML = "<i class='fa-solid fa-chevron-up'></i>";
        } else {
            viewDocsBtn.innerHTML = "<i class='fa-solid fa-chevron-down'></i>";
        }
    })

});
