document.addEventListener("DOMContentLoaded", function () {
    const inputFile = document.getElementById("input_file");
    const fileNameSpan = document.getElementById("file-name");
    const removeFile = document.getElementById("remove-file");

    const backendAPI = "/nvidia/nvidia-docs-analyzer-api/";

    // File upload event handling
    inputFile.addEventListener("change", function () {
        removeUploadedFiles();
        fileNameSpan.style.cssText = `
        width: 50px;
        overflow-x: auto;
        border: 1px solid #ccc;
    `;
        removeFile.style.display = "block"
        const file = inputFile.files[0];
        localStorage.setItem("nvidiaFileUploaded", JSON.stringify(file.name));
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

            // console.log([...formData.entries()]);

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
                })
                .catch(error => {
                    console.error('File upload error:', error);
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
        localStorage.removeItem("nvidiaFileUploaded");
    });

    // Get uploaded file name from localStorage on reload
    const nvidiaFileUploaded = JSON.parse(localStorage.getItem("nvidiaFileUploaded"));
    if (nvidiaFileUploaded) {
        fileNameSpan.style.display = "none";
        fileNameSpan.textContent = nvidiaFileUploaded;
        fileNameSpan.style.cssText = `
         width: 50px;
         overflow-x: auto;
         border: 1px solid #ccc;
     `;
        removeFile.style.display = "block";
    } else {
        removeUploadedFiles();
    }
});