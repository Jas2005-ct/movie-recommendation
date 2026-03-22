// Add click event to movie posters (handled by template links now)
const closeButton = document.querySelector('.close-button');
if (closeButton) {
    closeButton.addEventListener('click', () => {
        const modal = document.getElementById('movieModal');
        if (modal) modal.style.display = 'none';
    });
}

// Close modal
closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
});

document.getElementById("capture-emotion").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent default link behavior

    // Access the camera
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            let video = document.getElementById("camera-stream");
            video.style.display = "block"; // Show video
            video.srcObject = stream;

            // Show Capture button
            document.getElementById("capture-button").style.display = "block";
        })
        .catch(function(error) {
            console.error("Camera access denied!", error);
        });
});

document.getElementById("capture-button").addEventListener("click", function() {
    let video = document.getElementById("camera-stream");
    let canvas = document.getElementById("capture-canvas");
    let context = canvas.getContext("2d");

    // Set canvas size to match the video frame
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current frame from the video onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Stop the camera stream after capturing
    let stream = video.srcObject;
    let tracks = stream.getTracks();
    tracks.forEach(track => track.stop());

    video.style.display = "none"; // Hide video
    this.style.display = "none"; // Hide capture button

    // Convert image to Base64 (can be sent to Django)
    let imageData = canvas.toDataURL("image/png");

    // TODO: Send `imageData` to Django backend for emotion detection
    console.log("Captured Image: ", imageData);
});