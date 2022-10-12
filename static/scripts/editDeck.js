modal = document.querySelector(".editDeckModal")

const openEditDeckModal = () => {
    modal.style.visibility = "visible"
    console.log(modal)
}

window.addEventListener("click", (e) => {
    if (e.target == modal) {
        modal.style.visibility = "hidden"
        console.log("hide")
    }
})