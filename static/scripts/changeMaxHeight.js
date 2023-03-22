const decklistContainer = document.querySelector('.decklist-container')
const cardTypes = document.querySelectorAll('.card-types');

function adjustMaxHeight() {

    let aboveMidThreshold = (currentValue) => currentValue >= 10
    let aboveHighThreshold = (currentValue) => currentValue >= 10
    let numberOfTypes = []

    cardTypes.forEach((ele, idx) => {
        if (idx !== 3) numberOfTypes.push(ele.children.length)
    })

    if (numberOfTypes.some(aboveMidThreshold)) decklistContainer.style.maxHeight = "1500px"
    else decklistContainer.style.maxHeight = "900px"

}

window.addEventListener('resize', (e) => {
    adjustMaxHeight()
})

cardTypes.forEach((ele) => {
    adjustMaxHeight()
})