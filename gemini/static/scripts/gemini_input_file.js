const inputFile = document.getElementById("input_file");
const fileNameSpan = document.getElementById("file-name");
const removeFile = document.getElementById("remove-file");

const backendAPI = "/gemini/gemini-docs-analyzer-api/";

// let fileUploaded = false;

// File upload event handling
inputFile.addEventListener("change", function () {
    fileNameSpan.style.cssText = `
        width: 50px;
        overflow-x: auto;
        border: 1px solid #ccc;
    `;
    removeFile.style.display = "block"
    const file = inputFile.files[0];
    const maxFileSize = 5 * 1024 * 1024; // 5 MB


    if (file) {
        fileNameSpan.textContent = file.name;
    }
    if (file.size > maxFileSize) {
        alert("File size exceeds the 5 MB limit!");
        inputFile.value = "";
        fileNameSpan.style.display = "none";
        removeFile.style.display = "none";
    }
    uploadFile();
});

const uploadFile = () => {
    const formData = new FormData();
    const file = inputFile.files[0];

    if (file) {
        formData.append("input_file", file);

        console.log([...formData.entries()]);

        fetch(backendAPI, {
            method: 'POST',
            body: formData,
        })
            .then(async response => {
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || `HTTP error! status: ${response.status}`);
                }
                console.log('File upload success:', data);
                // alert("File uploaded successfully!");
            })
            .catch(error => {
                console.error('File upload error:', error);
                // alert("File uploaded failed!");
            });
    }
};


async function removeUploadedFiles() {
    try {
        const response = await fetch("/nvidia/clear-uploaded-files-api/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                // "X-CSRFToken": getCookie("csrftoken"), 
            },
        });

        // Ensure the response is ok before processing it
        if (response.ok) {
            const data = await response.json(); 
            console.log("Uploaded files removed and session cleared:", data);
        } else {
            const errorData = await response.json();  
            console.error("Error removing files:", errorData.error || response.statusText);
        }
    } catch (error) {
        console.error("Error removing files:", error);
    }
}


removeFile.addEventListener("click", () => {
    inputFile.value = '';
    fileNameSpan.style.display = "none";
    removeFile.style.display = "none"
    removeUploadedFiles();
});

document.addEventListener("DOMContentLoaded", () => {
    removeUploadedFiles();
});