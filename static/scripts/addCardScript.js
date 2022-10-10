const addCardSearchbar = document.querySelector("#add-card-searchbar")

const split = window.location.href.split("/")
let deck_id = split[split.length - 1]

const deck = {id: 22}

addCardSearchbar.addEventListener("input", async(e) => {

    e.stopPropagation()

    const text = addCardSearchbar.value
    const dropdown = document.querySelector(".add-card-dropdown")

    if (text.length > 3) {
        listOfCards = await fetch(`/search/names/${text}`)
        cardList = await listOfCards.json()

        dropdown.innerHTML = ""
        dropdown.style.opacity = 1
        cardList.forEach(card => {  
            dropdown.innerHTML += `
                <form action="/decklist/${deck_id}/${card.id}" method="POST">
                    <button>${card.name}</button>
                </form>
            `
        })

    }

    if (text.length === 0) {
        dropdown.innerHTML = ""
        dropdown.style.opacity = 0
    }    
})

window.addEventListener("click", (e) => {
    let text = addCardSearchbar.value
    const dropdown = document.querySelector(".add-card-dropdown")

    console.log(e.target)

    // if(e.target !== addCardSearchbar) {
    //     dropdown.style.opacity = 0
    //     text = ""
    //     dropdown.innerHTML = ""
    // }

})
