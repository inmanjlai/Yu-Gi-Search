const decklistContainer = document.querySelector('.decklist-container')
const cardTypes = document.querySelectorAll('.card-types');

function adjustMaxHeight() {

    let aboveMidThreshold = (currentValue) => currentValue >= 10
    let numberOfTypes = []

    cardTypes.forEach((ele, idx) => {
        if (idx !== 3) numberOfTypes.push(ele.children.length)
    })

    let count = 0
    numberOfTypes.forEach((ele) => {
        if (ele > 6) count+=1
    })

    if (count > 2) {
        if (numberOfTypes.some(aboveMidThreshold) && window.innerWidth > 600) decklistContainer.style.maxHeight = "1500px"
        else decklistContainer.style.maxHeight = "900px"
    }

}

window.addEventListener('resize', (e) => {
    adjustMaxHeight()
})

cardTypes.forEach((ele) => {
    adjustMaxHeight()
})
