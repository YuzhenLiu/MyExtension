const activateButton = document.getElementById("activateButton");
const getCookiesButton = document.getElementById("getCookiesButton");
const prompt = document.getElementById("prompt");
const port = chrome.runtime.connect({ name:"connection"});
let count = 0;

activateButton.addEventListener("click", function() {
    count = count + 1;
    setPrompt(count);
})

getCookiesButton.addEventListener("click", async function() {
    const cookies = await getCookies();
    port.postMessage(cookies);
    console.log("Cookies sent.")
})

async function getCookies() {
    let cookiesFound = 0;
    let cookies = null;
    try {
        cookies = await chrome.cookies.getAll({});
        cookiesFound = cookies.length;
    } catch (error) {
        setPrompt("An unexpected error occurred!");
        console.log(error.message);
        return `Unexpected error: ${error.message}`;
    }
    setPrompt(cookiesFound + " cookies found.");
    return cookies;
}

function setPrompt(content) {
    prompt.textContent = content;
    prompt.hidden = false;
}

function initPrompt() {
    prompt.hidden = true;
    prompt.
    prompt.textContent = "";
}

port.onMessage.addListener(function(msg) {
    console.log("message received: " + msg);
})



