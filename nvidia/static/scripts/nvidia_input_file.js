const inputFile = document.getElementById("input_file");
const fileNameSpan = document.getElementById("file-name");

inputFile.addEventListener("change", function () {
    fileNameSpan.style.cssText = `
        width: 50px;
        overflow-x: auto;
        border: 1px solid #ccc;
    `;
    const file = inputFile.files[0];
    if (file) {
        fileNameSpan.textContent = file.name;
    }
});

function uploadFile() {
    const formData = new FormData();
    const file = inputFile.files[0];

    if (file) {
        formData.append("input_file", file);

        fetch('/upload/', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        alert("Please select a file to upload.");
    }
}
