let cardDisplay = document.querySelector(".card-display")

console.log("HELLO WORLD")

const displayCard = (img_url) => {
    cardDisplay.children[0].src = img_url
}

// const split = window.location.href.split("/")
// let deck_id = split[split.length - 1]

const addCardQuantity = async(e) => {
    const card_id = e.target.id.split("add-card-btn-")[1]

    const card_quantity_span = document.querySelector(`.card-${card_id}-quantity`)

    const req = await (await fetch(`/decklist/add-quantity/${deck_id}/${card_id}`, {method: "POST"})).json()

    card_quantity_span.innerText = req.response
}

const delCardQuantity = async(e) => {
    const card_id = e.target.id.split("del-card-btn-")[1]
    const cardContainer = document.querySelector(`.decklist-card-${card_id}`)

    const card_quantity_span = document.querySelector(`.card-${card_id}-quantity`)

    const req = await (await fetch(`/decklist/del-quantity/${deck_id}/${card_id}`, {method: "POST"})).json()

    if(req.response === 0) {
        cardContainer.remove()
    }

    card_quantity_span.innerText = req.response
}