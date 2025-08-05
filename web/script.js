async function predictMood() {
    const userInput = document.getElementById("user-input").value;

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: userInput })
        });

        const result = await response.json();
        document.getElementById("prediction-result").innerText = `Predicted mood: ${result.mood}`;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("prediction-result").innerText = "Error predicting mood.";
    }
}
