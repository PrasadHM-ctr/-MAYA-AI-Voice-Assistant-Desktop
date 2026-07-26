const micBtn = document.getElementById("micBtn");
const message = document.getElementById("message");

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.lang = "en-IN";
recognition.continuous = false;
recognition.interimResults = false;

micBtn.onclick = function () {
    recognition.start();
};

recognition.onstart = function () {
    micBtn.innerHTML = "🎙️";
};

recognition.onend = function () {
    micBtn.innerHTML = "🎤";
};

recognition.onresult = async function (event) {

    let text = event.results[0][0].transcript;

    message.value = text;

    let response = await fetch("/voice", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: text
        })

    });

    let data = await response.json();

    alert(data.reply);
}