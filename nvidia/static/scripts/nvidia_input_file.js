const fileInput = document.getElementById('input_file');
const fileNameDisplay = document.getElementById('file-name');


fileInput.addEventListener('change', (event) => {
    console.log("clicked", event.target.files);
    console.log("size", event.target.files[0]?.size, "bytes");
    console.log("type", event.target.files[0]?.type);
    
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
