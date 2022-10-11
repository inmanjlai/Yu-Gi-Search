let cardDisplay = document.querySelector(".hover-card-display")

console.log(cardDisplay.children[0].src)

window.addEventListener("mouseover", async(e) => {
    if(e.target.classList.contains("decklist-card") || e.target.classList.contains("cardnamespan") || e.target.classList.contains("cardnamep")) {
        let card_to_fetch = e.target.children[0].children[0].innerText
        let img = await (await fetch(`/card/${card_to_fetch}/img`)).json()
        console.log(img.img_url)

        // cardDisplay.style.visibility = "visible"
        cardDisplay.style.left = e.pageX
        cardDisplay.style.top = e.pageY

        cardDisplay.children[0].src = img.img_url

        console.log(e.pageX)
        console.log(cardDisplay.style.left)
    }
    else {
        cardDisplay.style.visibility = "hidden"
    }
})