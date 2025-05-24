document.addEventListener('DOMContentLoaded', () => {
    const userQueryInput = document.getElementById('user-query');
    const askBtn = document.getElementById('ask-btn');
    const loadingIndicator = document.getElementById('loading-indicator');
    const chatBox = document.getElementById('chat-box');

    // Disable button initially if input is empty
    askBtn.disabled = !userQueryInput.value.trim();

    // Update button state on input
    userQueryInput.addEventListener('input', () => {
        askBtn.disabled = !userQueryInput.value.trim();
    });

    askBtn.addEventListener('click', sendQuery);
    userQueryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !askBtn.disabled) sendQuery();
    });

    async function sendQuery() {
        const userQuery = userQueryInput.value.trim();
        if (!userQuery) return;

        userQueryInput.value = '';
        askBtn.disabled = true;
        loadingIndicator.classList.remove('hidden');

        chatBox.classList.add('loading');
        chatBox.scrollTop = 44;

        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user');
        userMessage.innerHTML = `<div class="response">${userQuery}</div>`;
        chatBox.insertBefore(userMessage, chatBox.firstChild);

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: userQuery })
            });

            const data = await response.json();
            console.log('API Response:', data);

            const agentMessage = document.createElement('div');
            agentMessage.classList.add('message', 'agent');
            
            // tools info generation
            let toolsInfo = '';
            if (data.tools_used && data.tools_used.length > 0) {
                toolsInfo = `<div class="tools-info">Tools used: ${data.tools_used.join(', ')}</div>`;
                console.log('Rendering tools:', data.tools_used);
            } else {
                console.log('No tools used in response');
            }

            agentMessage.innerHTML = `
                <div class="agent-name">${data.agent_used}:</div>
                <div class="response">${formatAnswer(data.answer)}</div>
                ${toolsInfo}
            `;
            chatBox.insertBefore(agentMessage, chatBox.firstChild);
            
        } catch (error) {
            console.error('Error fetching response:', error);
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('message', 'agent');
            errorMessage.innerHTML = `<div class="agent-name">Error:</div><div class="response">Sorry, something went wrong. Please try again.</div>`;
            chatBox.insertBefore(errorMessage, chatBox.firstChild);
        } finally {
            loadingIndicator.classList.add('hidden');
            chatBox.classList.remove('loading');
            chatBox.scrollTop = 0;
            askBtn.disabled = !userQueryInput.value.trim();
        }
    }

    function formatAnswer(answer) {
        let formattedAnswer = answer.replace(/\n/g, '<br/>');
        formattedAnswer = formattedAnswer.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
        formattedAnswer = formattedAnswer.replace(/\* (.*?)(?=<br\/>|$)/g, '<li>$1</li>');
        if (formattedAnswer.includes('<li>')) {
            formattedAnswer = '<ul>' + formattedAnswer + '</ul>';
        }
        return formattedAnswer;
    }
});