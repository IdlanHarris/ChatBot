// Sidebar open and close functions
function w3_open() {
    const sidebar = document.getElementById("mySidebar");
    const openNav = document.getElementById("openNav");

    sidebar.style.width = "20%"; // Adjust width as needed
    document.getElementById("main").style.marginLeft = "20%";
    sidebar.style.borderRight = "2px solid white"; // Add border when open
    openNav.style.display = "none";
}

function w3_close() {
    const sidebar = document.getElementById("mySidebar");
    const openNav = document.getElementById("openNav");

    sidebar.style.width = "0"; // Hide sidebar
    document.getElementById("main").style.marginLeft = "0%";
    sidebar.style.borderRight = "hidden"; // Add border when open
    openNav.style.display = "inline-block";
}

// Handle textarea auto-resize
document.addEventListener('input', function (e) {
    if (e.target.tagName === 'textarea') {
        e.target.style.height = 'auto'; // Reset height
        e.target.style.height = e.target.scrollHeight + 'px'; // Set height based on content
    }
});

// Handle file input change and image preview
document.querySelector('input[type="file"]').addEventListener('change', function (e) {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (event) {
            const imgPreview = document.createElement('img');
            imgPreview.src = event.target.result;
            imgPreview.style.maxWidth = '100px';
            document.getElementById('imagePreviewContainer').appendChild(imgPreview);
        };
        reader.readAsDataURL(file);
    }
});

// Function to handle AI processing when the button is clicked
function processWithAI(event) {
    event.preventDefault(); // Prevent form submission
    
    const textInput = document.querySelector('textarea[name="textInput"]').value;
    const data = { textInput: textInput };

    // Show the chat container and expand it
    const chatContainer = document.getElementById('chatContainer');
    if (chatContainer) {
        chatContainer.style.display = 'flex'; // Make chat container visible
    }

    // Add the user's message to the chat
    const userMessageElement = document.getElementById('userMessage');
    if (userMessageElement) {
        userMessageElement.textContent = textInput; // Display the user's message
    }

    // Send data to the server using fetch
    fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log("Response received:", response);
        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log("Data from server:", data);

        // Check if response contains a valid message
        if (data.response) {
            // Get the AI response and update the response div
            const responseDiv = document.getElementById('aiResponse');
            const responseText = document.getElementById('responseText');
            responseText.textContent = data.response; // Use the response from the server

            // Show the response div by changing display to 'flex'
            responseDiv.style.display = 'flex'; 
        } else if (data.error) {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred: " + error.message);
    });
}
