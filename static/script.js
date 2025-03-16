document.getElementById("fileInput").addEventListener("change", function(event) {
    let file = event.target.files[0];

    if (file) {
        let reader = new FileReader();
        reader.onload = function(e) {
            let preview = document.getElementById("imagePreview");
            preview.src = e.target.result;
            document.querySelector(".preview-container").style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById("predictButton").addEventListener("click", async function() {
    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select an image first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    try {
        let response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        if (result.error) {
            throw new Error(result.error);
        }

        let resultDiv = document.getElementById("result");
        resultDiv.innerHTML = `Prediction: <strong>${result.class}</strong> (${(result.confidence * 100).toFixed(2)}%)`;
        resultDiv.style.display = "block";
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred! Check the console.");
    }
});
