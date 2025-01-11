console.log("hello homenav js");


fetch('/',{
    method: 'GET',
})
.then(response => {
    if(!response.ok){
        throw Error(response.statusText);
    }
    return response.text();
})