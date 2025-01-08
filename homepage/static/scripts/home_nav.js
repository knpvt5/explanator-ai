document.addEventListener("DOMContentLoaded", () => {
    const GlobalFunction = {};
    const menuBtn = document.querySelector(".menu-btn");
    const leftAside = document.querySelector(".left-aside");

    menuBtn.addEventListener("click", (e) => {
        if (window.innerWidth > 480) {
            leftAside.classList.toggle("menu-close");
        } else {
            e.stopPropagation();
            leftAside.classList.toggle("menu-slide");
        }

        // Update the menu button icon
        GlobalFunction.updateMenuButtonIcon = function () {
            if ((leftAside.classList.contains("menu-close")) && (window.innerWidth > 480)) {
                menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            } else if ((!leftAside.classList.contains("menu-slide")) && (window.innerWidth < 480)) {
                menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            } else {
                menuBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
            }
        }
        GlobalFunction.updateMenuButtonIcon();

        // Close sidebar when clicking outside
        document.addEventListener('click', function (e) {
            if (!leftAside.contains(e.target) && !menuBtn.contains(e.target) && (leftAside.classList.contains("menu-slide"))) {
                leftAside.classList.remove('menu-slide');
                GlobalFunction.updateMenuButtonIcon();
            }
        });
    });


    const mainContent = document.querySelector("#main-content");

    document.querySelectorAll(".ai-types li a").forEach((aiType) => {
        const aiApi = aiType.dataset.api;
        const aiTypeValue = aiType.getAttribute("href").replace("#", "");

        aiType.addEventListener("click", (e) => {
            e.preventDefault();
            updateContent(aiApi, aiTypeValue);
            updateUrl(aiApi, aiTypeValue);

            // menu button closing on click
            if (window.innerWidth < 480) {
                leftAside.classList.toggle("menu-slide");
                GlobalFunction.updateMenuButtonIcon();
            }

        });
    });


    function updateContent(aiApi, aiTypeValue) {

        fetch(`${aiApi}/${aiTypeValue}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
                return response.text();
            })
            .then(data => {
                // console.log(data);
                // Parse the fetched HTML
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, "text/html");

                document.querySelectorAll(".dynamic-css").forEach(dynamicCss => dynamicCss.remove());
                document.querySelectorAll(".dynamic-js").forEach(dynamicJs => dynamicJs.remove());

                // Load CSS
                doc.querySelectorAll("link[rel='stylesheet']").forEach(newLink => {
                    if (!document.querySelector(`link[href="${newLink.href}"]`)) {
                        const newLinkElement = document.createElement("link");
                        newLinkElement.rel = "stylesheet";
                        newLinkElement.href = newLink.href;
                        newLinkElement.className = "dynamic-css";
                        document.head.appendChild(newLinkElement);
                    }
                });

                // Load JS
                doc.querySelectorAll("script[src]").forEach(newScript => {
                    // Remove any existing script with the same base src
                    /* document.querySelectorAll(`script[src^="${newScript.src}"]`).forEach(oldScript => {
                        oldScript.parentNode.removeChild(oldScript);
                        console.log("Removed old script:", oldScript.src);
                    }); */

                    const newSrc = newScript.src.split("?")[0];
                    const oldScriptElements = document.querySelectorAll(`script[src^="${newSrc}"]`);
                    oldScriptElements.forEach(oldScript => {
                        oldScript.parentNode.removeChild(oldScript);
                        console.log("Removed old script:", oldScript.src);
                    });

                    const newScriptElement = document.createElement("script");
                    if (newScript.src) {
                        const timestampedSrc = `${newScript.src}?t=${Date.now()}`;
                        newScriptElement.src = timestampedSrc;
                        // newScriptElement.src = newScript.src;
                        newScriptElement.className = "dynamic-js";
                        newScriptElement.type = "module";
                        newScriptElement.defer = true;
                        newScriptElement.onload = () => {
                            console.log('Script loaded successfully!', newScript.src);
                            // document.body.style.backgroundColor = "red";
                        };
                        newScriptElement.onerror = (e) => {
                            console.error('Failed to load script:', newScript.src, e);
                        };
                    } else {
                        newScriptElement.textContent = newScript.textContent;
                        newScriptElement.className = "dynamic-js";
                        newScriptElement.type = "module";
                        newScriptElement.defer = true;
                    }
                    document.body.appendChild(newScriptElement);
                    console.log("new script added", newScriptElement);
                });

                // Update main content
                const fetchedContent = doc.querySelector("#main-content");
                if (fetchedContent) {
                    mainContent.innerHTML = fetchedContent.innerHTML;
                    document.title = doc.title;
                } else {
                    console.error("Main content not found in the fetched HTML.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
            })
            .finally(() => {
                console.log("calling finally");
            })
    };

    // updating/manipulating URL
    const updateUrl = (aiApi, aiTypeValue) => {
        const url = new URL(window.location);
        const urlParams = url.searchParams;
        urlParams.set('aiType', aiTypeValue);
        const urlParameters = urlParams.toString();
        console.log("url params", urlParameters);
        history.pushState({ aiApi: aiApi }, '', `?${urlParameters}`);
        console.log(history.state);
    };


    // Handle browser back/forward
    window.addEventListener('popstate', (event) => {
        const url = new URL(window.location);
        const urlParams = url.searchParams;
        const aiApi = event.state?.aiApi || "";
        const aiTypeValue = urlParams.get('aiType');
        if (aiApi && aiTypeValue) {
            updateContent(aiApi, aiTypeValue);
        } else {
            console.warn("Missing data in state or query parameters");
            window.location.reload();
        }
    });

    const url = new URL(window.location);
    const urlParams = url.searchParams;
    const aiApiTest = window.history.state?.aiApi || "";
    const aiTypeValueTest = urlParams.get('aiType');
    if (aiApiTest && aiTypeValueTest) {
        updateContent(aiApiTest, aiTypeValueTest)
    }

    /* const urlParams = new URLSearchParams(window.location.search);
       const aiTypeValueTest = urlParams.get('aiType');
       console.log("url params", aiTypeValue);
       console.log(history.state);
       updateContent(aiApi, aiTypeValueTest); */

    /*  fetch('/')
         .then(response => {
             if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
             return response.text();
         })
         .then(data => {
             // console.log(data);
             const parser = new DOMParser();
             const doc = parser.parseFromString(data, 'text/html')
             const mainContent = doc.querySelector('#main-content')
             console.log(mainContent.innerHTML);
         }) */



    /*  window.addEventListener('popstate', () => {
         // updateContent(window.location);
         const aiTypeValue = window.location.pathname.replace("/", "");
         console.log(aiTypeValue);
         const aiApi = window.history.state.api;
         console.log(aiApi);
         updateContent(aiApi, aiTypeValue);
         console.log("called updateContent");
 
     }); */

    /* window.addEventListener('load', () => {
       const aiTypeValue = window.location.pathname.replace("/", "");
       const aiApi = window.history.state?.api; 
       if (aiApi) {
           updateContent(aiApi, aiTypeValue);
       }
   }); */

    //    const originalSrc = newScript.src.replace(/\?.*$/, "");

    /* const originalSrc = newScript.src.split("?")[0];
    const oldScriptElements = document.querySelectorAll(`script[src^="${originalSrc}"]`);
    oldScriptElements.forEach(oldScript => {
        oldScript.parentNode.removeChild(oldScript);
        console.log("Removed old script:", oldScript.src);
    }); */

    /* const url = new URL(window.location.origin);
    url.pathname = `${aiTypeValue}`.replace(/\/+/g, '/');
    if (window.location.pathname !== url.pathname) {
        window.history.pushState({ api: aiApi }, '', url);

    } else {
        window.history.replaceState({ api: aiApi }, '', url);
    } */



    // -------------------------------------------------------------

    /* document.querySelectorAll("script").forEach(script => {
        const scriptValue = script.getAttribute("src");
        // const onlyJsName = scriptValue.split('/').pop();
        // console.log("scripts value is: ",scriptValue);

        if (scriptValue === "home.js") {
            console.log("home.js script found");

        } else {
            console.log("home.js script not found");
            // console.log(script.src);
        }
    }); */


    /* document.querySelectorAll("link[rel='stylesheet']").forEach(link => {
        const linkValue = link.getAttribute("href");
        // const onlyCssName = linkValue.split('/').pop();
        // console.log("link value is: ",linkValue);

        if (linkValue === "home.css") {
            console.log("home.css link found");
            // link.remove();

        } else {
            console.log("home.css link not found");
            // console.log(link.href);
        }
    }); */

    /* const urlParams = new URLSearchParams(window.location.search);
    console.log(urlParams);
    const categoryFromUrl = urlParams.get('category') || 'all';
    const pageFromUrl = parseInt(urlParams.get('page')) || 1;
    displayPostsByCategory(categoryFromUrl, pageFromUrl); */

    // ------------------------------------------------------------

});
