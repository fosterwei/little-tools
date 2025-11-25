// Open AI embeddings from page content
//
// IMPORTANT:
// You will need to supply your API key below on line 11 which will be stored
// as part of your SEO Spider configuration in plain text. Also be mindful if 
// sharing this script that you will be sharing your API key also unless you 
// delete it before sharing.
// 
//

const OPENAI_API_KEY = 'api接口';
const userContent = document.body.innerText;
    
function chatGptRequest() {
    return fetch('https://portal.hytto.com/chatgpt/openai/v1/embeddings', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${OPENAI_API_KEY}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            model: "text-embedding-3-small",
            input: `${userContent}`,
            encoding_format: "float",
            })
    })
    .then(response => {
        if (!response.ok) {
             return response.text().then(text => {throw new Error(text)});
        }
        return response.json();
    })
    .then(data => {
        console.log(data.data[0].embedding);
        return data.data[0].embedding.toString();
    });
}


return chatGptRequest()
    .then(embeddings => seoSpider.data(embeddings))
    .catch(error => seoSpider.error(error));

