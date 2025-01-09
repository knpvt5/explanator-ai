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
                // Parsing the fetched HTML
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, "text/html");

                document.querySelectorAll(".dynamic-css, .dynamic-js").forEach(dynamicCSSandJS => dynamicCSSandJS.remove());

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


    // Handling browser back/forward
    window.addEventListener('popstate', (event) => {
        const url = new URL(window.location);
        const urlParams = url.searchParams;
        const aiApi = event.state?.aiApi || "";
        const aiTypeValue = urlParams.get('aiType');
        if (aiApi && aiTypeValue) {
            updateContent(aiApi, aiTypeValue);
        } else {
            window.location.reload();
        }
    });

    //  initial load of this page
    const checkInitialLoad = () => {
        const { aiApi = "" } = window.history.state || {};
        const aiTypeValue = new URL(window.location).searchParams.get('aiType');
        if (aiApi && aiTypeValue) {
            updateContent(aiApi, aiTypeValue);
        }
    };
    checkInitialLoad();

});
