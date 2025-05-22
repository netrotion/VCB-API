function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + days*24*60*60*1000);
    const expires = "expires=" + d.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}
async function getFingerprint() {
    const fpPromise = FingerprintJS.load({ monitoring: false });
    const fp = await fpPromise;
    const result = await fp.get();
    setCookie("visitorId", result.visitorId, 7);
    document.getElementById('visitor-id').textContent = result.visitorId;
}
getFingerprint();
document.getElementById('copy-btn').onclick = function() {
    const visitorId = document.getElementById('visitor-id').textContent;
    navigator.clipboard.writeText(visitorId).then(function() {
    const msg = document.getElementById('copied-msg');
    msg.style.display = 'inline';
    setTimeout(() => { msg.style.display = 'none'; }, 1200);
    });
};