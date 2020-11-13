document.addEventListener('DOMContentLoaded', function () {


	// Don't show any posts upon logging in
	document.querySelector('#posts-view').style.display = 'none';

	// View all posts
	document.querySelector('#allPosts').addEventListener('click', () => load_posts());

	// Get user that was clicked on
	const users = document.querySelectorAll('.card-title')
	users.forEach(item => {
		item.addEventListener('click', (event) => console.log(event.target))
	})


	// Submits a new post
	document.querySelector('#compose-form').onsubmit = function () {
		// Prevent default submission
		event.preventDefault();

		// Gets the content of the post
		const body = document.querySelector('#compose-body').value;

		// Saves the post via API
		fetch('/posts', {
			method: 'POST',
			body: JSON.stringify({
				body: body
			})
		})
			// Load all posts
			.then(() => load_posts())
			// Catch any errors and log them to the console
			.catch(error => {
				console.log('Error:', error);
			});
	};
});


function load_posts() {
	// Show the posts block
	document.querySelector('#posts-view').style.display = 'block';

	// Clear previously shown posts
	document.querySelector('#posts').innerHTML = '';

	// Get all the posts and display
	fetch('posts/all')
		.then(response => response.json())
		.then(posts => {
			const parentContainer = document.getElementById("posts");
			posts.forEach(post => {
				const postContainer = document.createElement('div');
				// Use Bootstrap cards
				postContainer.className = "card"
				const postCardBody = document.createElement('div');
				postCardBody.className = "card-body"
				parentContainer.append(postContainer);
				postContainer.append(postCardBody);
				const postFieldContainer = document.createElement('div');
				postCardBody.append(postFieldContainer);
				postFieldContainer.style.margin = "0px 25px 0px";
				addPostField(postCardBody, "h5", post.user, "card-title");
				addPostField(postCardBody, "p", post.body, "card-text");
				addPostField(postCardBody, "span", post.timestamp, "card-text");

			});
		})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
}

function addPostField(parentContainer, element, field, className) {
	// console.log(field)
	// Creates parent container of each field
	const postFieldContainer = document.createElement(element);
	postFieldContainer.innerHTML = field;
	postFieldContainer.className = className;
	console.log(field);

	// Add event listener to usernames in case we want to see their profile
	if (className === "card-title") {
		let username = field
		postFieldContainer.addEventListener('click', () => showProfile(username))
	}
	parentContainer.append(postFieldContainer);

	// postFieldContainer.style.margin = "0px 25px 0px";
}

function showProfile(username) {
	// Clear previously shown posts
	document.querySelector('#posts').innerHTML = '';


	fetch('posts/' + username)
		.then(response => response.json())
		.then(posts => {
			const parentContainer = document.getElementById("posts");
			posts.forEach(post => {
				const postContainer = document.createElement('div');
				// Use Bootstrap cards
				postContainer.className = "card"
				const postCardBody = document.createElement('div');
				postCardBody.className = "card-body"
				parentContainer.append(postContainer);
				postContainer.append(postCardBody);
				const postFieldContainer = document.createElement('div');
				postCardBody.append(postFieldContainer);
				postFieldContainer.style.margin = "0px 25px 0px";
				addPostField(postCardBody, "h5", post.user, "card-title");
				addPostField(postCardBody, "p", post.body, "card-text");
				addPostField(postCardBody, "span", post.timestamp, "card-text");

			});
		})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});

}