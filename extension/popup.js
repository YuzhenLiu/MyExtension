const activateButton = document.getElementById("activateButton");
const getCookiesButton = document.getElementById("getCookiesButton");
const reportButton = document.getElementById("ReportButton");
const deleteCookiesButton = document.getElementById("deleteCookiesButton");
const prompt = document.getElementById("prompt");
const domainLabel = document.getElementById("domain");
const resultLabel = document.getElementById("result");
const cookiesFoundLabel =  document.getElementById("cookiesFound");
const thirdPartyCookiesLabel =  document.getElementById("thirdPartyCookies");
const maliciousCookiesLabel = document.getElementById("maliciousCookies");
const port = await chrome.runtime.connect({ name:"connection"});
let count = 0;
let isRunning;

init();

activateButton.addEventListener("click", function() {
    if (isRunning) {
        chrome.storage.sync.set({isActivated: false});
        isRunning = false;
        setButton("#4CAF50", "Activate");
        count = count + 1;
    } else {
        chrome.storage.sync.set({isActivated: true});
        isRunning = true;
        setButton("#DC0000", "Deactivate");
        count = count - 1;
    }
    init();
    setPrompt(count);
})

getCookiesButton.addEventListener("click", async function() {
    if (isRunning) {
        const cookies = await getCookies();
        port.postMessage({sender: "popup", sources: "all_sites", content: cookies, url: '', domain: ''});
        resultLabel.style.color = "#000000";
        resultLabel.style.fontSize = "28px";
        resultLabel.textContent = "Scanning Results";
        domainLabel.textContent = "Domain: All sites visited";
        cookiesFoundLabel.textContent = "Stored Cookies: " + cookies.length;
        thirdPartyCookiesLabel.textContent = "Third Parties Cookies: --";
        maliciousCookiesLabel.textContent = "Malicious Cookies: Analysing...";

        console.log("Cookies sent.");
    } else {
        setPrompt("Not activated!")
    }
})

reportButton.addEventListener("click", async function() {
    if (isRunning) {
        port.postMessage({sender: "popup", sources: "report"});
    } else {
        setPrompt("Not activated!");
    }
})

deleteCookiesButton.addEventListener("click", async function() {
    if (isRunning) {
        getSiteCookies("delete");
    } else {
        setPrompt("Not activated!");
    }
})

port.onMessage.addListener(async function(msg) {
    if (msg.sender == "background") {
        console.log("Popup received: " + msg.sources);
        if (msg.sources == "current_site") {
            if (msg.content == 0) {
                resultLabel.style.color = "#4CAF50";
                resultLabel.textContent = "Safe";
            } else {
                resultLabel.style.color = "#DC0000";
                resultLabel.textContent = "Unsafe";
            }
        }
        maliciousCookiesLabel.textContent = "Malicious Cookies: " + msg.content;
    }
    console.log("Popup received: " + msg);
})

function getSiteResources() {
    return performance.getEntriesByType("resource").map(e => e.name);
}

async function getCookies() {
    let cookies = null;
    try {
        if (arguments[0]) {
            let url = arguments[0];
            cookies = await chrome.cookies.getAll({ "url": url });
        } else {
            cookies = await chrome.cookies.getAll({});
            let cookies_found = cookies.length;
            setPrompt(cookies_found + " cookies found.");
        }
    } catch (error) {
        setPrompt("An unexpected error occurred!");
        console.log(error.message);
        return `Unexpected error: ${error.message}`;
    }
    return cookies;
}

function setPrompt(content) {
    prompt.textContent = content;
    prompt.hidden = false;
    window.setTimeout(initPrompt, 2000);
}

function initPrompt() {
    prompt.hidden = true;
    prompt.textContent = "";
}

async function getCurrentUrl() {
    console.log("getting domain...");
    let [tab] =await chrome.tabs.query({active:true, currentWindow:true});
    let url = null;
    if (tab?.url) {
        try {
            url = new URL(tab.url);
            console.log("Current tab's ID: " + tab.id);
        } catch {
            console.error("Failed to get domain!");
        }
    }
    return url;
}

function setButton(color, value) {
    activateButton.style.setProperty("background-color", color);
    activateButton.textContent = value;
}

async function init() {
    await chrome.storage.sync.get("isActivated", async ({ isActivated }) => {
        if (isActivated == true) {
            isRunning = true;
            setButton("#DC0000", "Deactivate");
        } else {
            isRunning = false;
            setButton("#4CAF50", "Activate");
        }
        resetPanel();
        getSiteCookies("get");
    });
}

function resetPanel() {
    if (!isRunning) {
        resultLabel.style.color = "#000000";
        resultLabel.textContent = "----";
        domainLabel.textContent = "--";
        cookiesFoundLabel.textContent = "--";
        thirdPartyCookiesLabel.textContent = "--";
        maliciousCookiesLabel.textContent = "--";
    }
}

async function getSiteCookies(command) {
    let urls;
    let cookies = new Array();
    let uniqueCookies = new Array();
    if (isRunning) {
        let [tab] = await chrome.tabs.query({active: true, currentWindow: true});

        await chrome.scripting.executeScript({
            target: {tabId: tab.id},
            function: getSiteResources,
        }, async (result) => {
            let data = result[0].result;
            let currentUrl = await getCurrentUrl();
            data.push(currentUrl.toString());
            urls = data.map(url => url.split(/[#?]/)[0]);
            urls = new Set(urls);
            urls = [...urls.values()].filter(Boolean);

            for (let url of urls) {
                let temp = await getCookies(url);
                if (command == "delete") {
                    for (let cookie of temp) {
                        await chrome.cookies.remove({
                            "url": url,
                            "name": cookie.name,
                            "storeId": cookie.storeId,
                        });
                    }
                } else if (command == "get") {
                    cookies.push(...temp);
                }
            }
            ;
            cookies = [...cookies].filter(Boolean);
            uniqueCookies = cookies.reduce((prev, cur) => {
                if (!prev.find(cookie => cookie.value == cur.value && cookie.name == cur.name && cookie.domain == cur.domain)) {
                    prev.push(cur);
                }
                ;
                return prev;
            }, []);
            console.log(uniqueCookies);
            port.postMessage({sender: "popup", sources: "current_site", content: uniqueCookies, url: currentUrl, domain: currentUrl.hostname.replace("www", "")});
            console.log("Popup: Cookies sent.");
            setPrompt(uniqueCookies.length + " cookies Found.");

            resultLabel.textContent = "----";
            domainLabel.textContent = "Domain: " + currentUrl.hostname;
            cookiesFoundLabel.textContent = "Stored Cookies: " + uniqueCookies.length;
            thirdPartyCookiesLabel.textContent = "Third Parties Cookies: " + await classifyCookies(uniqueCookies, currentUrl);;
            maliciousCookiesLabel.textContent = "Malicious Cookies: Analysing...";
        });
    }
}

async function classifyCookies(cookies, currentUrl) {
    let thirdPartiesCookiesNum = 0;

    for (let cookie of cookies) {
        if (!cookie.domain.replace("www", "").match(currentUrl.hostname.replace("www", ""))) {
            thirdPartiesCookiesNum += 1;
        }
    };

    return thirdPartiesCookiesNum
}