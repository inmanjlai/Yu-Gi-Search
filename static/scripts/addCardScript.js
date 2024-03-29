const addCardSearchbar = document.querySelector("#add-card-searchbar")

const split = window.location.href.split("/")
let deck_id = split[split.length - 1]

addCardSearchbar.addEventListener("input", async(e) => {

    const text = addCardSearchbar.value
    const dropdown = document.querySelector(".add-card-dropdown")

    listOfCards = await fetch(`/search/names/${text}`)
    cardList = await listOfCards.json()

    dropdown.innerHTML = ""
    dropdown.style.display = "flex"
    cardList.forEach(card => {  
        dropdown.innerHTML += `
            <form action="/decklist/${deck_id}/${card.id}" method="POST">
                <button>${card.name}</button>
            </form>
        `
    })

    adjustMaxHeight()


    if (text.length === 0) {
        dropdown.innerHTML = ""
        dropdown.style.display = "none"
    }    
})

window.addEventListener("click", (e) => {
    let text = addCardSearchbar.value
    const dropdown = document.querySelector(".add-card-dropdown")

})
