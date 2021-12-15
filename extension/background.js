//const host = "http://192.168.50.2:5555/analyser/upload/";
const host = "http://127.0.0.1:5555/analyser/";
let isActivated = true;

chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({isActivated});
});

chrome.runtime.onConnect.addListener(function(port) {
    port.onMessage.addListener(async function(msg) {
        if (msg.sender === "popup") {
            if (msg.sources === "report") {
                await getReport();
                console.log("Background received: " + msg.sources);
            } else {
                console.log("Background: Cookies received.");
                let cookies = await JSON.stringify(msg.content, null, 2);
                let maliciousCookies = await upload(cookies, msg.url, msg.domain);
                if (msg.sources === "all_sites") {
                    port.postMessage({sender: "background", sources: "all_site", content: maliciousCookies});
                    console.log("Background received: " + msg.sources);
                } else if (msg.sources === "current_site") {
                    port.postMessage({sender: "background", sources: "current_site", content: maliciousCookies});
                    console.log("Background received: " + msg.sources);
                }
                console.log("Background: Cookies uploaded.");
            }
        }
    });
});

async function upload(content, siteUrl, siteDomain) {
    const res = await fetch(host + "upload/", {
        method: 'POST',
        body: content,
        headers: {
            'Content-Type': 'application/json',
            'Site-Url': siteUrl,
            'Site-Domain': siteDomain
        }
    });

    const resText = await res.text();
    return resText;
};

async function getReport() {
    chrome.tabs.create({url: host + "report/"});
}