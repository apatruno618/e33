document.addEventListener('DOMContentLoaded', function () {


	// Don't show any posts upon logging in
	document.querySelector('#posts-view').style.display = 'block';
	document.querySelector('#profile-view').style.display = 'none';

	loadPosts()

	// View all posts
	document.querySelector('#allPosts').addEventListener('click', () => loadPosts());

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
			.then(() => loadPosts())
			// Catch any errors and log them to the console
			.catch(error => {
				console.log('Error:', error);
			});
	};
});


function loadPosts() {
	// Show the applicable view
	document.querySelector('#posts-view').style.display = 'block';
	document.querySelector('#profile-view').style.display = 'none';

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
				addPostField(postCardBody, "a", post.user, "card-title");
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

	// Add event listener to usernames in case we want to see their profile
	if (className === "card-title") {
		const user = field
		postFieldContainer.addEventListener('click', () => showProfile(user))
	}
	parentContainer.append(postFieldContainer);

	// postFieldContainer.style.margin = "0px 25px 0px";
}

function showProfile(username) {
	// Hide other views
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#posts-view').style.display = 'none';
	document.querySelector('#profile-view').style.display = 'block';

	// Clear previously shown posts
	document.querySelector('#users-posts').innerHTML = '';

	document.querySelector('#profile').innerHTML = username;

	loadFollowers(username);
	loadFollowing(username);
	loadPosts(username);


}

function loadFollowers(username) {

	fetch('followers/' + username)
		.then(response => response.json())
		.then(followers => {
			const followersContainer = document.getElementById("followers");
			followersContainer.innerHTML = "Followers: " + followers;
		})// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
}

function loadFollowing(username) {

	fetch('following/' + username)
		.then(response => response.json())
		.then(following => {
			const followingContainer = document.getElementById("following");
			followingContainer.innerHTML = "Following: " + following;
		})// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
}


function loadPosts(username) {
	fetch('posts/' + username)
		.then(response => response.json())
		.then(posts => {
			const parentContainer = document.getElementById("users-posts");
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
				addPostField(postCardBody, "p", post.body, "card-text");
				addPostField(postCardBody, "span", post.timestamp, "card-text");

			});
		})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
}