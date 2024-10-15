function handleFileInput() {
    const input = document.getElementById('file-input');
    const filePath = input.value.replace('C:\\fakepath\\', '');  // Just show filename
    document.getElementById('file-path').value = filePath;
    clearLogs();  // Clear logs when a new file is selected
}

function clearLogs() {
    document.getElementById('scroll-window').textContent = '';
}

function uploadFile(event) {
    event.preventDefault();  // Prevent form from submitting normally
    
    const formData = new FormData();
    const fileInput = document.getElementById('file-input');
    
    if (fileInput.files.length === 0) {
        alert("Please select a file first.");
        return;
    }
    
    formData.append('file', fileInput.files[0]);

    // Fetch and stream the output in real-time
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        const scrollWindow = document.getElementById('scroll-window');
        
        function read() {
            reader.read().then(({ done, value }) => {
                if (done) return;  // Stop reading when finished
                scrollWindow.textContent += decoder.decode(value);
                scrollWindow.scrollTop = scrollWindow.scrollHeight;  // Auto-scroll
                read();  // Keep reading chunks
            });
        }
        read();
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('scroll-window').textContent = 'Error occurred during upload.';
    });
}
