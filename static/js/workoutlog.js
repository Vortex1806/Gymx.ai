const submitBtn = document.querySelector('.submit-btn');
const inputField = document.querySelector('.workout-input');
const responseContainer = document.querySelector('.output-container');
const loadingIndicator = document.querySelector('.loading-indicator');
loadingIndicator.style.display = 'none';
const firstname = "shubh";

submitBtn.addEventListener('click', async () => {
    const inputText = inputField.value;
    responseContainer.innerHTML = "";
    loadingIndicator.style.display = 'block';

    try {
        console.log("inside maki");
        const response = await fetch('http://127.0.0.1:4000/logworkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: firstname }),
            mode: 'cors'
        });

        console.log("Calling data");

        // Check if the response is successful (status code 200)
        if (response.ok) {
            const data = await response.json(); // Parse the JSON from the response
            print(data)
            responseContainer.innerHTML = data.response;
        } else {
            console.error('Error fetching response from API:', response.status);
        }
    } catch (error) {
        console.error('Error fetching response from API:', error);
    } finally {
        loadingIndicator.style.display = 'none';
    }
});
