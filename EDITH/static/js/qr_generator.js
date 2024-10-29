function generateQR() {
    const text = document.getElementById('qr-text').value;
    if (!text) {
        alert('Please enter text for the QR code');
        return;
    }
    
    fetch('/generate-qr', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({text: text})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        const qrResult = document.getElementById('qr-result');
        const qrImage = document.getElementById('qr-image');
        const downloadLink = document.getElementById('download-link');
        
        qrImage.src = data.qr_image;
        downloadLink.href = data.qr_image;
        qrResult.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to generate QR code: ' + error.message);
    });
} 