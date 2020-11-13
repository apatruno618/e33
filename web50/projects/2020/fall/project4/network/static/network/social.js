document.addEventListener('DOMContentLoaded', function () {

	document.querySelector('#posts-view').style.display = 'none';

	// Use buttons to toggle between views
	document.querySelector('#allPosts').addEventListener('click', () => load_posts());
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


function load_posts() {
	// Show the mailbox and hide other views
	document.querySelector('#posts-view').style.display = 'block';

	// Clear previously shown posts
	document.querySelector('#posts').innerHTML = '';

	// Get all the posts and display
	fetch('/allposts')
		.then(response => response.json())
		.then(posts => {
			const parentContainer = document.getElementById("posts");
			posts.forEach(post => {
				const postContainer = document.createElement('div');
				// postContainer.style.display = "flex";
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
				addPostField(postCardBody, "p", post.timestamp, "card-text");
				// test = document.getElementsByClassName("card-title").innerHTML
				// console.log(test)
			});
		})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
}

function addPostField(parentContainer, element, field, className) {
	console.log(field)
	// Creates parent container of each field
	const postFieldContainer = document.createElement(element);
	postFieldContainer.innerHTML = field;
	postFieldContainer.className = className;
	// Link to user's profile page
	// if (field === post.user) {
	// 	postFieldContainer.addEventListener('click', () => console.log(hello));
	// }
	parentContainer.append(postFieldContainer);

	postFieldContainer.style.margin = "0px 25px 0px";
}

function showProfile(username) {
	console.log(username)
}