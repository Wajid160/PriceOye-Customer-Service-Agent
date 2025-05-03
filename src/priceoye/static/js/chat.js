document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWidget = document.getElementById('chat-widget');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatHistory = document.getElementById('chat-history');

    // Toggle chat widget
    chatToggle.addEventListener('click', () => {
        chatWidget.classList.toggle('hidden');
        if (!chatWidget.classList.contains('hidden')) {
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    });

    chatClose.addEventListener('click', () => {
        chatWidget.classList.add('hidden');
    });

    // Send chat message
    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message
        appendMessage('user', message);
        chatInput.value = '';
        chatInput.disabled = true;
        chatSend.disabled = true;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            if (data.error) {
                appendMessage('agent', `Error: ${data.error}`);
            } else {
                appendMessage('agent', data.response);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            appendMessage('agent', 'Unable to connect to the server. Please try again.');
        } finally {
            chatInput.disabled = false;
            chatSend.disabled = false;
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    }

    function appendMessage(sender, text) {
        const div = document.createElement('div');
        div.className = sender === 'user' ? 'flex justify-end' : 'flex justify-start';
        div.innerHTML = `
            <div class="${sender === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'} p-3 rounded-${sender === 'user' ? 'l' : 'r'}-xl rounded-b${sender === 'user' ? 'r' : 'l'}-xl max-w-[80%] animate-slide-in-${sender === 'user' ? 'right' : 'left'}">
                ${text}
            </div>
        `;
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});