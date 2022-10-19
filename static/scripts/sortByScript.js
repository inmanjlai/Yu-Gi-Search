const select = document.querySelector(".sort-by-select")
const form = document.querySelector(".sort-by-form")
const sortInput = form.children[1]

select.addEventListener("change", (e) => {
    sortInput.value = e.target.value
    form.submit()
})