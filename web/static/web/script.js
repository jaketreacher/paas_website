function showNavbar(trigger) {
    const target = document.querySelector(trigger.getAttribute("target"));

    if( target ) {
        target.classList.remove("collapsed");
        trigger.classList.add("hidden");
    } else {
        throw "Unable to find target";
    }
}

function hideNavbar(trigger) {
    const target = {
        nav: document.querySelector(trigger.getAttribute("target-nav")),
        toggle: document.querySelector(trigger.getAttribute("target-toggle"))
    }

    if( target.nav && target.toggle ) {
        target.nav.classList.add("collapsed");
        target.toggle.classList.remove("hidden");
    } else {
        throw "Unable to find target";
    }
}

function setup() {
    const toggleBtn = document.querySelector("#navbar-toggle");
    const mainNav = document.querySelector("#main-nav");
    const closeBtn = mainNav.querySelector("button.close");

    toggleBtn.addEventListener("click", () => showNavbar(toggleBtn));
    closeBtn.addEventListener("click", () => hideNavbar(closeBtn));
    window.addEventListener("keyup", (event) => {
        if( event.key === "Escape" && !mainNav.classList.contains("collapsed") ) {
            hideNavbar(closeBtn);
        }

    });
}

setup();
console.log("Loaded");