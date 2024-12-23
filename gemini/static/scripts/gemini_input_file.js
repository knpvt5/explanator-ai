document.addEventListener("DOMContentLoaded", () => {
    const inputFile = document.getElementById("input_file");
    const fileNameSpan = document.getElementById("file-name");
    const removeFile = document.getElementById("remove-file");

    if (!inputFile || !fileNameSpan || !removeFile) {
        console.error("Required DOM elements not found.", error);
        return;
    }

    const backendAPI = "/gemini/gemini-docs-analyzer-api/";

    inputFile.addEventListener("change", function () {
        removeUploadedFiles();
        const file = inputFile.files[0];
        const maxFileSize = 5 * 1024 * 1024; // 5 MB        

        if (file) {
            fileNameSpan.textContent = file.name;
            fileNameSpan.style.cssText = `
                width: 50px;
                overflow-x: auto;
                border: 1px solid #fff;
            `;
            removeFile.style.display = "block";
            localStorage.setItem("geminiFileUploaded", JSON.stringify(file.name));
            console.log("geminiFileUploaded saved to localStorage:", file.name);


            if (file.size > maxFileSize) {
                alert("File size exceeds the 5 MB limit!");
                inputFile.value = "";
                fileNameSpan.style.display = "none";
                removeFile.style.display = "none";
                localStorage.removeItem("geminiFileUploaded");
            } else {
                uploadFile();
            }
        }
    });

    const uploadFile = () => {
        const file = inputFile.files[0];
        if (file) {
            const formData = new FormData();
            formData.append("input_file", file);

            fetch(backendAPI, {
                method: "POST",
                body: formData,
            })
                .then(async (response) => {
                    const data = await response.json();
                    if (!response.ok) {
                        throw new Error(
                            data.error || `HTTP error! status: ${response.status}`
                        );
                    }
                    console.log("File upload success:", data);
                })
                .catch((error) => {
                    console.error("File upload error:", error);
                });
        }
    };

    async function removeUploadedFiles() {
        try {
            const response = await fetch("/nvidia/clear-uploaded-files-api/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Uploaded files removed and session cleared:", data);
            } else {
                const errorData = await response.json();
                console.error(
                    "Error removing files:",
                    errorData.error || response.statusText
                );
            }
        } catch (error) {
            console.error("Error removing files:", error);
        }
    }

    removeFile.addEventListener("click", () => {
        console.log("Remove file button clicked.");
        inputFile.value = "";
        fileNameSpan.style.display = "none";
        removeFile.style.display = "none";
        removeUploadedFiles();
        localStorage.removeItem("geminiFileUploaded");
    });


    const geminiFileUploaded = JSON.parse(localStorage.getItem("geminiFileUploaded"));
    if (geminiFileUploaded) {
        // console.log("Restoring from localStorage:", geminiFileUploaded);
        fileNameSpan.textContent = geminiFileUploaded;
        fileNameSpan.style.cssText = `
                width: 50px;
                overflow-x: auto;
                border: 1px solid #fff;
                margin-bottom:5px ;
            `;
        fileNameSpan.style.display = "block";
        removeFile.style.display = "block";
    }else{
        removeUploadedFiles();
    }
});
