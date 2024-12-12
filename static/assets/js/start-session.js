document.getElementById("sessionForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    // Collect form data
    const formData = {
        patientName: document.getElementById("patient-name").value,
        age: document.getElementById("age").value,
        gender: document.getElementById("gender").value,
        symptoms: document.getElementById("symptoms").value,
    };

    // Send data to the backend
    try {
        const response = await fetch("http://localhost:8000/api/diagnose", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) throw new Error("Failed to get a response");

        const result = await response.json();

        // Display results
        document.getElementById("results").classList.remove("hidden");
        document.getElementById("diagnostic-message").textContent = 
            `Potential conditions: ${result.diagnosis.join(", ")}`;
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while fetching the diagnosis.");
    }
});
