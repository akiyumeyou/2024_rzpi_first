const axios = require('axios');

const openaiApiKey = 'key'
async function generateResponse(prompt, pastMessages = []) {
    const systemMessage = {
        role: 'system',
        content:'あなたはとても優しく、話し相手として最高の友人です'   };

    if (pastMessages.length === 0) {
        pastMessages.push(systemMessage);
    }

    const userMessage = {
        role: 'user',
        content: prompt
    };

    pastMessages.push(userMessage);

    const response = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
            model: 'gpt-3.5-turbo',
            messages: pastMessages
        },
        {
            headers: {
                'Authorization': `Bearer ${openaiApiKey}`,
                'Content-Type': 'application/json'
            }
        }
    );

    const responseMessage = {
        role: 'assistant',
        content: response.data.choices[0].message.content
    };

    pastMessages.push(responseMessage);
    return { responseMessage: responseMessage.content, pastMessages };
}

const prompt = process.argv[2];
const pastMessages = JSON.parse(process.argv[3] || '[]');

generateResponse(prompt, pastMessages).then(result => {
    console.log(JSON.stringify(result));
}).catch(error => {
    console.error('Error:', error);
    process.exit(1);
});
