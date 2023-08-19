document.addEventListener('DOMContentLoaded', function() {
    var checkButton = document.getElementById('check-button');
    var urlInput = document.getElementById('url-input');
    var statusDiv = document.getElementById('status');

    checkButton.addEventListener('click', function() {
        var url = urlInput.value;
        statusDiv.innerHTML = 'Checking URL...';
        statusDiv.style.color = '';

        fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'url': url
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data['prediction'] == -1) {
                statusDiv.innerHTML = 'This Site is likely to be phishing.';
                statusDiv.style.color = 'red';
            } else {
                statusDiv.innerHTML = 'This Site is likely to be legitimate.';
                statusDiv.style.color = 'green';
            }
        });
    });


    var form = document.getElementById('comment-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); 

        var commentInput = document.getElementById('comment-input');
        var acknowledgement = document.getElementById('acknowledge')

        var formData = new FormData();
        formData.append('report', commentInput.value);

        fetch('http://localhost:5000/submit', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert('Your report has been successfully submitted. Thank you for reporting!');

            } else {
                alert('Error submitting the report');
            }
        });
    });


});