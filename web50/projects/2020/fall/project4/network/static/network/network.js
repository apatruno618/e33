document.addEventListener('DOMContentLoaded', function () {

	let parentEditElement;
	let parentLikeElement;

	document.addEventListener('click', event => {
		const originalButton = event.target;

		// User is trying to edit
		if (originalButton.className.includes("btn-secondary")) {
			const postId = originalButton.getAttribute("post");
			// Replace content of button
			originalButton.innerHTML = "Save"
			parentEditElement = originalButton.parentElement;
			// Get the hidden anchor to attach text area to
			const anchor = parentEditElement.querySelector(".edit-anchor");
			const currentPostBodyElement = parentEditElement.querySelector("#post-body");
			const textArea = document.createElement('textarea');
			textArea.value = currentPostBodyElement.innerHTML;
			anchor.append(textArea);
			// Remove previous text
			currentPostBodyElement.remove()

			document.addEventListener('click', event => {
				const element = event.target;

				if (element.innerHTML === "Save") {
					const updatedPostContent = document.querySelector("textarea").value;
					saveUpdatedPost(postId, updatedPostContent, parentEditElement, originalButton);
				}
			})
		}

		// User is trying to like
		if (originalButton.className.includes("btn-link")) {
			const postId = originalButton.getAttribute("post");
			fetch('/like/' + postId, {
				method: 'PUT',
			}).then(() => {
				parentLikeElement = originalButton.parentElement;
				const updateLikes = parentLikeElement.querySelector('.likes')
				updateLikes.innerHTML += 1
				// Update button
				originalButton.innerHTML = "Unlike";
			})
				// Catch any errors and log them to the console
				.catch(error => {
					console.log('Error:', error);
				});
		}
	})
});

function saveUpdatedPost(postId, updatedPostContent, parentEditElement, originalButton) {
	// Make fetch call using put method
	fetch('/edit/' + postId, {
		method: 'PUT',
		body: JSON.stringify({
			body: updatedPostContent
		})
	}).then(() => {
		const newBodyElement = document.createElement('p');
		newBodyElement.innerHTML = updatedPostContent;
		const anchor = parentEditElement.querySelector('.edit-anchor');
		anchor.append(newBodyElement);
		const editPostBodyElement = document.querySelector('textarea');
		editPostBodyElement.remove();

		// Update button
		originalButton.innerHTML = "Edit";

	})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
}



