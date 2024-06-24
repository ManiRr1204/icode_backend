const apiUrl = 'https://397vncv6uh.execute-api.us-west-2.amazonaws.com/test/employee/get/68f9bafc-2390-11ef-82b6-02d83582ee22'; // Replace with your actual API URL
const outputElement = document.getElementById('output');

function getApiData() {
  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        // throw new Error(⁠ "Error: ${response.status}" ⁠);
      }
      return response.json();
    })
    .then(data => {
      // Process the API data here
      console.log(data);
      outputElement.textContent = JSON.stringify(data, null, 2); // Display data in the paragraph
    })
    .catch(error => {
      console.error('Error:', error);
      outputElement.textContent = 'Error fetching data.';
    });
}

getApiData();