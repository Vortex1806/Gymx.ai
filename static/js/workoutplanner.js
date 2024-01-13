const submitBtn = document.querySelector('.submit-btn');
const inputField = document.querySelector('.workout-input');

submitBtn.addEventListener('click', async () => {
    const inputText = inputField.value;
    responseContainer.innerHTML = "";
    try {
            const response = await fetch('http://127.0.0.1:4000/getworkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: inputText }),
                mode: 'cors'
            });
            console.log("Calling data");
            const data = await response.json();
            responseContainer.innerHTML = data.response;

    } catch (error) {
        console.error('Error fetching response from API:', error);
    }

});
