const searchbar = document.querySelector("#nav-search-form")

searchbar.addEventListener("input", async(e) => {
    const text = searchbar.elements[0].value
    const dropdown = document.querySelector("#nav-search-dropdown")

    if (text.length > 3) {
        listOfCards = await fetch(`/search/names/${text}`)
        cardList = await listOfCards.json()

        dropdown.innerHTML = ""
        dropdown.style.opacity = 1
        cardList.forEach(card => {  
            dropdown.innerHTML += `<a href='/card/${card.id}'>${card.name}</a>`
        })

    }

    if (text.length === 0) {
        dropdown.innerHTML = ""
        dropdown.style.opacity = 0
    }    
})

window.onclick = (e) => {
let text = searchbar.elements[0].value
const dropdown = document.querySelector("#nav-search-dropdown")
const modal = document.querySelector(".deck-modal")
const deckbtn = document.querySelector(".deckbtn")

    if(e.target === deckbtn){
        modal.style.opacity = 1
        modal.style.pointerEvents = 'auto'
    } else if (e.target === modal) {
        modal.style.opacity = 0
        modal.style.pointerEvents = 'none'
    }

    if(e.target !== searchbar || e.target !== dropdown) {
        dropdown.style.opacity = 0
        text = ""
        dropdown.innerHTML = ""
    }

} 