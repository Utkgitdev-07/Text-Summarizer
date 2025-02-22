document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("summaryForm").addEventListener("submit", async function (event) {
        event.preventDefault();  // Prevent page refresh

        const textInput = document.getElementById("textInput").value.trim();
        const summaryOutput = document.getElementById("summaryOutput");

        // Clear previous output
        summaryOutput.textContent = "";

        if (!textInput) {
            alert("⚠️ Please enter some text to summarize.");
            return;
        }

        try {
            console.log("📤 Sending request to /summarize...");
            const response = await fetch("/summarize", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ text: textInput })
            });

            console.log("📥 Received response:", response);

            const data = await response.json();
            console.log("✅ API Response Data:", data);

            if (response.ok) {
                summaryOutput.textContent = data.summary;  // Display summary
            } else {
                summaryOutput.textContent = "❌ Error: " + (data.error || "Something went wrong.");
            }
        } catch (error) {
            summaryOutput.textContent = "❌ Error connecting to server!";
            console.error("🚨 Fetch error:", error);
        }
    });
});

// ✅ Copy Summary Function
function copySummary() {
    const summaryText = document.getElementById("summaryOutput").textContent;
    if (!summaryText) {
        alert("⚠️ Nothing to copy!");
        return;
    }

    // Create a temporary textarea to copy text
    const tempTextArea = document.createElement("textarea");
    tempTextArea.value = summaryText;
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    document.execCommand("copy");
    document.body.removeChild(tempTextArea);

    alert("✅ Summary copied to clipboard!");
}
