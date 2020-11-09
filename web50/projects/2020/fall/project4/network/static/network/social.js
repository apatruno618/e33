document.addEventListener('DOMContentLoaded', function () {

	console.log('loaded');

	// Use buttons to toggle between views
	// document.querySelector('#compose').addEventListener('click', compose_post);

	// Submits a new post
	document.querySelector('#compose-form').onsubmit = function () {
		// Prevent default submission
		event.preventDefault();


		// Gets the content of the post
		const body = document.querySelector('#compose-body').value;
		console.log(body);

		// Saves the post via API
		fetch('/posts', {
			method: 'POST',
			body: JSON.stringify({
				body: body
			})
		})
			// Load response
			.then(response => response.json())
			// Catch any errors and log them to the console
			.catch(error => {
				console.log('Error:', error);
			});
	};
});