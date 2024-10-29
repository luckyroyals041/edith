document.addEventListener('DOMContentLoaded', function() {
    if (isMobileDevice()) {
        document.getElementById('mobile-warning').style.display = 'block';
        document.getElementById('desktop-content').style.display = 'none';
    } else {
        document.getElementById('mobile-warning').style.display = 'none';
        document.getElementById('desktop-content').style.display = 'block';
    }
});

// Detect if device is mobile
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Handle common mobile directories
function selectDownloads() {
    if (isMobileDevice()) {
        fetch('/organize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                directory: 'downloads',
                mobile: true 
            })
        })
        .then(handleResponse)
        .catch(handleError);
    }
}

function selectDCIM() {
    if (isMobileDevice()) {
        fetch('/organize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                directory: 'dcim',
                mobile: true 
            })
        })
        .then(handleResponse)
        .catch(handleError);
    }
}

function selectDocuments() {
    if (isMobileDevice()) {
        fetch('/organize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                directory: 'documents',
                mobile: true 
            })
        })
        .then(handleResponse)
        .catch(handleError);
    }
}

// Desktop folder dialog
function openFolderDialog() {
    if (!isMobileDevice()) {
        // Create a temporary file input element
        const input = document.createElement('input');
        input.type = 'file';
        // Enable directory selection
        input.setAttribute('webkitdirectory', '');
        input.setAttribute('directory', '');
        input.setAttribute('multiple', '');  // Allow multiple files to get the directory structure

        input.addEventListener('change', function(e) {
            if (this.files && this.files.length > 0) {
                const file = this.files[0];
                let folderPath;

                // Try different methods to get the folder path
                if (file.webkitRelativePath) {
                    // Get the folder path from the first file's relative path
                    folderPath = file.webkitRelativePath.split('/')[0];
                    // If we have the full path available, use it
                    if (file.path) {
                        folderPath = file.path.substring(0, file.path.lastIndexOf(file.name));
                    }
                } else if (file.path) {
                    // Direct path (some browsers)
                    folderPath = file.path.substring(0, file.path.lastIndexOf(file.name));
                } else if (file.mozFullPath) {
                    // Firefox specific
                    folderPath = file.mozFullPath.substring(0, file.mozFullPath.lastIndexOf(file.name));
                }

                // Set the folder path in the input field
                if (folderPath) {
                    document.getElementById('folder-path').value = folderPath;
                    console.log("Selected folder path:", folderPath); // Debug log
                }
            }
        });

        // Trigger the file input click
        input.click();
    }
}

// Common response handler
function handleResponse(response) {
    return response.json().then(data => {
        if (data.status === 'error') {
            throw new Error(data.message);
        }
        alert(data.message);
    });
}

// Common error handler
function handleError(error) {
    console.error('Error:', error);
    alert('Error: ' + error.message);
}

// Main organize function
function organizeFiles() {
    if (isMobileDevice()) {
        alert('Please use one of the folder options above');
        return;
    }

    const folderPath = document.getElementById('folder-path').value.trim();
    if (!folderPath) {
        alert('Please enter a folder path or select a folder');
        return;
    }

    console.log("Organizing folder:", folderPath); // Debug log

    // Clean up the path (replace backslashes with forward slashes)
    const cleanPath = folderPath.replace(/\\/g, '/');
    
    fetch('/organize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            directory: cleanPath,
            isSelected: true
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'error') {
            throw new Error(data.message);
        }
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    });
} 
