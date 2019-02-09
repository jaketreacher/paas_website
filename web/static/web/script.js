// Globals
const collapsedClass = "nav-menu--collapsed";
const hiddenClass = "fab--hidden";

function showNavbar(trigger) {
    const target = document.querySelector(trigger.getAttribute("target"));

    if( target ) {
        target.classList.remove(collapsedClass);
        trigger.classList.add(hiddenClass);
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
        target.nav.classList.add(collapsedClass);
        target.toggle.classList.remove(hiddenClass);
    } else {
        throw "Unable to find target";
    }
}

function setup() {
    const navToggle = document.querySelector("#nav-toggle");
    const navMain = document.querySelector("#nav-main");
    const closeBtn = navMain.querySelector(".nav-menu__close-btn");

    navToggle.addEventListener("click", () => showNavbar(navToggle));
    closeBtn.addEventListener("click", () => hideNavbar(closeBtn));
    window.addEventListener("keyup", (event) => {
        if( event.key === "Escape" && !navMain.classList.contains(collapsedClass) ) {
            hideNavbar(closeBtn);
        }

    });
}

setup();
