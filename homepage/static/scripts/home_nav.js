document.addEventListener("DOMContentLoaded", () => {
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
        function updateMenuButtonIcon() {
            if ((leftAside.classList.contains("menu-close")) && (window.innerWidth > 480)) {
                menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            } else if ((!leftAside.classList.contains("menu-slide")) && (window.innerWidth < 480)) {
                menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            } else {
                menuBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
            }
        }
        updateMenuButtonIcon();

        // Close sidebar when clicking outside
        document.addEventListener('click', function (e) {
            if (!leftAside.contains(e.target) && !menuBtn.contains(e.target) && (leftAside.classList.contains("menu-slide"))) {
                leftAside.classList.remove('menu-slide');
                updateMenuButtonIcon();
            }
        });
    });



});
