document.getElementById("video_url").addEventListener("input", function () {
    var urlInput = this.value;
    var optionSelect = document.getElementById("option_list");
    var videoDropdown = document.getElementById("video_group");
    var audioDropdown = document.getElementById("audio_group");

    optionSelect.setAttribute("disabled", "disabled");
    videoDropdown.setAttribute("disabled", "disabled");
    audioDropdown.setAttribute("disabled", "disabled");

    // Clear existing options in both dropdowns
    clearDropdown(videoDropdown);
    clearDropdown(audioDropdown);

    updateMessage("Querying for the quality options...", "warning");

    // If the URL is valid, enable the dropdowns and fetch quality options
    if (validateYouTubeUrl(urlInput)) {
        fetch(`/get_quality?url=${encodeURIComponent(urlInput)}`)
            .then((response) => response.json())
            .then((data) => {

                // Populate video dropdown with quality options
                populateDropdown(data.video, videoDropdown);
                // Populate audio dropdown with quality options
                populateDropdown(data.audio, audioDropdown);

                var video_options = videoDropdown.getElementsByTagName("option");
                var audio_options = audioDropdown.getElementsByTagName("option");
                if (video_options.length > 0) {
                    video_options[0].selected = true;
                } else if (audio_options.length > 0) {
                    audio_options[0].selected = true;
                }

                optionSelect.removeAttribute("disabled");
                videoDropdown.removeAttribute("disabled");
                audioDropdown.removeAttribute("disabled");

                updateMessage("Successfully get quality options!", "success");
            }).catch((error) => {
                console.error("Error:", error);
            });
    } else {
        updateMessage("Check if your YouTube Video URL is valid!", "danger");
    }
});

// Function to clear dropdown options
function clearDropdown(dropdown) {
    while (dropdown.firstChild) {
        dropdown.removeChild(dropdown.firstChild);
    }
}

// Function to populate dropdown with options
function populateDropdown(optionsArray, dropdown) {
    optionsArray.forEach(function (quality) {
        var option = document.createElement("option");
        option.text = quality.label;
        option.value = quality.value;
        dropdown.appendChild(option);
    });
}

// Function to validate YouTube URL
function validateYouTubeUrl(url) {
    var pattern =
        /^(https?:\/\/)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)\/(watch\?v=|embed\/|v\/|.+\?v=)?([^&=%\?]{11})$/;
    return pattern.test(url);
}

// 更新消息显示并显示消息
function updateMessage(message, messageType) {
    var messageElement = document.getElementById("message");
    messageElement.textContent = message;
    messageElement.classList.remove("alert-warning", "alert-success", "alert-danger");

    if (messageType === "warning") {
        messageElement.classList.add("alert-warning");
    } else if (messageType === "success") {
        messageElement.classList.add("alert-success");
    } else if (messageType === "danger") {
        messageElement.classList.add("alert-danger");
    }

    // 显示消息
    messageElement.style.display = "block";
}