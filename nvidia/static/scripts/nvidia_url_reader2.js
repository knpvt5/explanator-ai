const fileInput = document.getElementById('input_file');
const fileNameDisplay = document.getElementById('file-name');


fileInput.addEventListener('change', (event) => {
    const fileName = event.target.files[0]?.name || "No file chosen";
    if(fileName){
        fileNameDisplay.style.cssText = `
        width: 50px;
        overflow-x: auto;
        border: 1px solid #ccc;
    `;
    }
    fileNameDisplay.textContent = fileName;
});
