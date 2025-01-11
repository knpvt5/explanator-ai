const pageHeader = document.querySelector('header');
const pageNav = document.querySelector('nav');

fetch('/', {
    method: 'GET',
})
    .then(response => {
        if (!response.ok) {
            throw Error(response.statusText);
        }
        return response.text();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.log(error)
    });

    const parser = new DOMParser();
    const fetchedDocument = parser.parseFromString(data, "text/html");
