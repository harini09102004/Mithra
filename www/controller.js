$(document).ready(function () {

    // Display Speak Message
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
    console.log("DisplayMessage called with message:", message); // Debugging line
    $(".siri-message").text(message);  // Target the <p> tag
    $('.siri-message').textillate('start');  // Ensure Textillate is initialized


    }

    // Display hood (hide SiriWave and show Oval)
    eel.expose(ShowHood);
    function ShowHood() {
        $("#Oval").attr("hidden", false);   // Show Oval
        $("#SiriWave").attr("hidden", true); // Hide SiriWaves
    }

    // Display sender text in chat
    eel.expose(senderText);
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `
                <div class="row justify-content-end mb-4">
                    <div class="width-size">
                        <div class="sender_message">${message}</div>
                    </div>
                </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Display receiver text in chat
    eel.expose(receiverText);
    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `
                <div class="row justify-content-start mb-4">
                    <div class="width-size">
                        <div class="receiver_message">${message}</div>
                    </div>
                </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Hide Loader and display Face Auth animation
    eel.expose(hideLoader);
    function hideLoader() {
        $("#Loader").attr("hidden", true);   // Hide loader
        $("#FaceAuth").attr("hidden", false); // Show face authentication animation
    }

    // Hide Face Auth and display Face Auth success animation
    eel.expose(hideFaceAuth);
    function hideFaceAuth() {
        $("#FaceAuth").attr("hidden", true);  // Hide face auth animation
        $("#FaceAuthSuccess").attr("hidden", false);  // Show success animation
    }

    // Hide success and display greeting
    eel.expose(hideFaceAuthSuccess);
    function hideFaceAuthSuccess() {
        $("#FaceAuthSuccess").attr("hidden", true);  // Hide success
        $("#HelloGreet").attr("hidden", false);  // Display greeting
    }

    // Hide Start Page and display blob animation
    eel.expose(hideStart);
    function hideStart() {
        $("#Start").attr("hidden", true);  // Hide start page
        
        setTimeout(function () {
            $("#Oval").addClass("animate__animated animate__zoomIn"); // Add animation to Oval
        }, 1000);

        setTimeout(function () {
            $("#Oval").attr("hidden", false);  // Show Oval after animation
        }, 1000);
    }

});
