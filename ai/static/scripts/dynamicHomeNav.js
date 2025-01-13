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


document.addEventListener('DOMContentLoaded', () => {
    const observer = new MutationObserver((mutationsList, observer) => {
        document.querySelectorAll(".ai-types li a").forEach((aiType) => {
            const aiApi = aiType.dataset.api || "";
            const aiTypeValue = aiType.getAttribute("href").replace("#", "");

            // Click event for each AI type
            aiType.addEventListener("click", (e) => {
                e.preventDefault();
                const url = new URL(window.location);
                // window.location.pathname = "/";
                path = `?ai=${aiApi}&aiType=${aiTypeValue}`;
                console.log("pathname", path);
                url.pathname = '/';
                // url.search = '?ai=gemini&aiType=gemini-api-cb';
                url.search = path;
                window.location.href = url.href;
            });
        });
        observer.disconnect();
    });

    // observation target to 'header' using querySelector
    const navElement = document.querySelector('nav');

    if (navElement) {
        observer.observe(navElement, { childList: true, subtree: true });
        // console.log("Element observed:", navElement.tagName);
    } else {
        console.error("No nav element found!");
    }

});





