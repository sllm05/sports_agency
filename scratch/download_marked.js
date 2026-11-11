const https = require('https');
const fs = require('fs');

https.get('https://cdn.jsdelivr.net/npm/marked/marked.min.js', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        fs.writeFileSync('scratch/marked.js', data);
        console.log('Saved marked.js');
    });
});
