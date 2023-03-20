const menuBtn = document.querySelector(".menu-btn")
const menuDropdown = document.querySelector(".menu-btn-dropdown")
const body = document.querySelector('body')

menuBtn.addEventListener("click", (e) => {
    menuDropdown.style.visibility = "visible"
    menuDropdown.style.height = '100vh'
    body.style.overflow = "hidden"
})

window.addEventListener("click", (e) => {
    if (e.target == menuDropdown) {
        menuDropdown.style.visibility = "hidden"
        menuDropdown.style.height = '100%'
        body.style.overflow = "auto"
    }
})