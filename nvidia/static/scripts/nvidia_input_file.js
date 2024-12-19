    const inputFile = document.getElementById("input_file");
    const fileNameSpan = document.getElementById("file-name");

    const backendAPI = "/nvidia/nvidia-docs-analyzer-api/";

    let fileUploaded = false;

    // File upload event handling
    inputFile.addEventListener("change", function () {
        fileNameSpan.style.cssText = `
        width: 50px;
        overflow-x: auto;
        border: 1px solid #ccc;
    `;
        const file = inputFile.files[0];
        console.log("File being uploaded:", inputFile.files[0]);
        if (file) {
            fileNameSpan.textContent = file.name;
        }
        uploadFile();
    });

    const uploadFile = () => {
        const formData = new FormData();
        const file = inputFile.files[0];

        if (file) {
            formData.append("input_file", file); // Make sure the key matches your backend

            console.log([...formData.entries()]); // Debug: Log formData entries

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
