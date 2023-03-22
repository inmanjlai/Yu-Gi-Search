const decklistContainer = document.querySelector('.decklist-container')
const cardTypes = document.querySelectorAll('.card-types');

function adjustMaxHeight() {

    let aboveMidThreshold = (currentValue) => currentValue >= 10
    let aboveHighThreshold = (currentValue) => currentValue >= 15
    let numberOfTypes = []
    let totalCardsInDeck = 

    cardTypes.forEach((ele, idx) => {
        if (idx !== 3) numberOfTypes.push(ele.children.length)
    })

    
    
    if (numberOfTypes.some(aboveHighThreshold)) {
        decklistContainer.style.maxHeight = "1500px"
    } else if (numberOfTypes.some(aboveMidThreshold)) {
        if (window.innerWidth <= 1920) {
            decklistContainer.style.maxHeight = "1200px"
        } else {
            decklistContainer.style.maxHeight = "1500px"
        }
    } else decklistContainer.style.maxHeight = "900px"

}

window.addEventListener('resize', (e) => {
    adjustMaxHeight()
})

cardTypes.forEach((ele) => {
    adjustMaxHeight()
})