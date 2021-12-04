//const host = "http://192.168.50.2:5555/analyser/upload/";
const host = "http://127.0.0.1:5555/analyser/upload/";
let isActivated = true;

chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({isActivated});
});

chrome.runtime.onConnect.addListener(function(port) {
    port.onMessage.addListener(async function(msg) {
        if (msg.sender == "popup") {
            console.log("Background: Cookies received.");
            let cookies = await JSON.stringify(msg.content, null, 2);
            let maliciousCookies = await upload(cookies);
            port.postMessage({sender: "background", content: maliciousCookies});
            console.log("Background: Cookies uploaded.");
        }
    });
});

async function upload(content) {
    const res = await fetch(host, {
        method: 'POST',
        body: content,
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const resText = await res.text();
    return resText;
};