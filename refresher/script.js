
class Bypass {
    constructor(cookie) {
        this.cookie = cookie;
    }

    async startProcess() {
        try {
            const response = await fetch('/api/process-cookie', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    cookie: this.cookie
                })
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Unknown error occurred');
            }

            return data.cookie;
        } catch (error) {
            throw error;
        }
    }
}

async function processCookie() {
    const cookieInput = document.getElementById('cookieInput');
    const processBtn = document.getElementById('processBtn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');

    const cookie = cookieInput.value.trim();
    
    if (!cookie) {
        showResult('Please enter a .ROBLOSECURITY cookie', 'error');
        return;
    }

    // Show loading state
    processBtn.disabled = true;
    loading.classList.remove('hidden');
    result.classList.add('hidden');

    try {
        const bypass = new Bypass(cookie);
        const newCookie = await bypass.startProcess();
        
        showResult(`
            <strong>✅ New .ROBLOSECURITY cookie:</strong>
            <div class="cookie-output">${newCookie}</div>
            <p><small>Copy the cookie above to use it.</small></p>
        `, 'success');
        
    } catch (error) {
        showResult(`❌ Error: ${error.message}`, 'error');
    } finally {
        processBtn.disabled = false;
        loading.classList.add('hidden');
    }
}

function showResult(content, type) {
    const result = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    
    resultContent.innerHTML = content;
    result.className = `result ${type}`;
    result.classList.remove('hidden');
}

// Allow Enter key to submit
document.getElementById('cookieInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        processCookie();
    }
});
