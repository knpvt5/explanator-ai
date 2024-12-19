const inputFile = document.getElementById("input_file");
const fileNameSpan = document.getElementById("file-name");
const removeFile = document.getElementById("remove-file");

const backendAPI = "/nvidia/nvidia-docs-analyzer-api/";

let fileUploaded = false;

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
    console.log("File being uploaded:", inputFile.files[0]);


    if (file.size > maxFileSize) {
        alert("File size exceeds the 5 MB limit!");
        this.value = "";
    }
    if (file) {
        fileNameSpan.textContent = file.name;
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
                alert('File uploaded successfully!');
            })
            .catch(error => {
                console.error('File upload error:', error);
                alert(`Failed to upload file: ${error.message}`);
            });
    } else {
        alert("Please select a file to upload.");
    }
};


removeFile.addEventListener("click", () => {
    inputFile.value = '';
    fileNameSpan.style.display = "none";
    removeFile.style.display = "none"
});