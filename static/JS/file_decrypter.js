document.getElementById('file').addEventListener('change', function () {
    var fileLabel = document.getElementById('file-label-text');
    var file = this.files[0];
    if (file && !file.name.endsWith('.enc')) {
        alert('Only ENC files are allowed!');
        return "";
    }
    if (file) {
        fileLabel.textContent = file.name;
    } else {
        fileLabel.textContent = 'Choose file';
    }
    
});


// Function to get URL parameters
function getUrlParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const regex = /([^&=]+)=([^&]*)/g;
    var match;
    while ((match = regex.exec(queryString))) {
        params[decodeURIComponent(match[1])] = decodeURIComponent(match[2]);
    }
    return params;
}

// Function to send GET request if 'result' parameter is 'true'
function checkAndSendRequest() {
    const params = getUrlParams();
    if (params.result == 'true') {
        const url = `/download/${params.id}/${params.filename}`;
        const originalUrl = `/clean-up/${params.id}/encrypter`;
        window.location.href = url;
        setTimeout(() => {
            window.location.href = originalUrl;
        }, 3500);
         }
}

// Execute the function when the page loads
window.onload = checkAndSendRequest;