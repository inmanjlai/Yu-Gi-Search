const decklistContainer = document.querySelector('.decklist-container')
const cardTypes = document.querySelectorAll('.card-types');

window.addEventListener('resize', (e) => {
    cardTypes.forEach((ele) => {
        if (ele.children.length > 15) {
            if (window.innerWidth >= 1700) {
                decklistContainer.style.maxHeight = "1500px"
            } else if (window.innerWidth <= 650) {
                decklistContainer.style.maxHeight = "none"

            }
        } 
    })
})

cardTypes.forEach((ele) => {
    if (ele.children.length > 15) {
        if (window.innerWidth >= 1700) {
            decklistContainer.style.maxHeight = "1500px"
        }
    }
})