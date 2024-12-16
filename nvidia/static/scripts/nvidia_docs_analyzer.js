const fileInput = document.getElementById('input_file');
const fileNameDisplay = document.getElementById('file-name');

fileInput.addEventListener('change', (event) => {
    const fileName = event.target.files[0]?.name || "No file chosen";
    fileNameDisplay.textContent = fileName;
});
