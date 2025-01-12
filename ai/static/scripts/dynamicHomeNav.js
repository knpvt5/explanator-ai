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
        // console.log(data);
        const parser = new DOMParser();
        const fetchedDocument = parser.parseFromString(data, "text/html");

        document.querySelectorAll('.dynamic-css, .dynamic-js').forEach(dynamicCSSandJS => dynamicCSSandJS.remove());

        // Loading CSS
        fetchedDocument.querySelectorAll('link[rel="stylesheet"]').forEach(newLink => {
            const newLinkEndHref = newLink.getAttribute('href').split('/').pop();
            // console.log(newLinkEndHref);

            if (!document.querySelector(`link[href="${newLink.href}"]`)) {
                if (newLinkEndHref === 'home_nav.css' || newLinkEndHref === 'home.css') {
                    const newLinkElement = document.createElement("link");
                    newLinkElement.rel = "stylesheet";
                    newLinkElement.href = newLink.href;
                    newLinkElement.className = "dynamic-css";
                    document.head.appendChild(newLinkElement);
                }
            }

            // Loading JS
            fetchedDocument.querySelectorAll('script[src]').forEach(newScript => {
                const newScriptSrc = newScript.getAttribute('src').split('/').pop();
                // console.log(newScriptSrc);

                if (!document.querySelector(`script[src="${newScript.src}"]`)) {
                    if (newScriptSrc === 'home_nav.js') {
                        const newScriptElement = document.createElement("script");
                        newScriptElement.src = newScript.src;
                        newScriptElement.defer = true;
                        newScriptElement.className = "dynamic-js";
                        document.body.appendChild(newScriptElement);
                    }
                }

            })


        });

        pageHeader.innerHTML = fetchedDocument.querySelector('header').innerHTML;
        pageNav.innerHTML = fetchedDocument.querySelector('nav').innerHTML;
    })
    .catch(error => {
        console.log(error)
    })
    .finally(() => {
        console.log('Finally called');
        document.body.id = 'home-page';
    });


    setTimeout(() => {
        document.querySelectorAll(".ai-types li a").forEach((aiType) => {
            const aiApi = aiType.dataset.api || "";
            const aiTypeValue = aiType.getAttribute("href").replace("#", "");
            console.log("eventListener registered");
    
            // Click event for each AI type
            aiType.addEventListener("click", (e) => {
                e.preventDefault();
                const url = new URL(window.location);
                const urlPathName = url.pathname;
                console.log(urlPathName);
                // window.history.pushState({}, '', '/newPath');
                window.location.pathname = "/";
            });
        });
    }, 3000);
    
            