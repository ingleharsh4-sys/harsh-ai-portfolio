const API_URL = "http://127.0.0.1:8000";

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");


function addMessage(message, type) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    if (type === "user") {

        messageDiv.classList.add("user-message");

        messageDiv.innerHTML = `
            <p>${message}</p>
        `;

    } else {

        messageDiv.classList.add("ai-message");

        messageDiv.innerHTML = `
    <div class="message-label">
        HARSH'S AI
    </div>

    <div class="ai-response">
        ${marked.parse(message)}
    </div>
    `;
    }

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) {
        return;
    }


    addMessage(message, "user");

    userInput.value = "";

    sendButton.disabled = true;

    sendButton.textContent = "Thinking...";

    const loadingMessage = document.createElement("div");

loadingMessage.classList.add("message", "ai-message");

loadingMessage.innerHTML = `
    <div class="message-label">
        HARSH'S AI
    </div>

    <div class="typing">
        <span></span>
        <span></span>
        <span></span>
    </div>
`;

chatBox.appendChild(loadingMessage);

chatBox.scrollTop = chatBox.scrollHeight;


    try {

        const response = await fetch(
            `${API_URL}/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data = await response.json();

        loadingMessage.remove();

        addMessage(data.response, "ai");


    } catch (error) {

        console.error(error);

        loadingMessage.remove();

        addMessage(
            "Sorry, I couldn't connect to the AI backend.",
            "ai"
        );

    }


    sendButton.disabled = false;

    sendButton.textContent = "Send";
}


sendButton.addEventListener(
    "click",
    sendMessage
);


userInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);

function askQuestion(question) {

    userInput.value = question;

    sendMessage();

}