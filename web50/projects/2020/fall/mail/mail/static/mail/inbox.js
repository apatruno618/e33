document.addEventListener('DOMContentLoaded', function () {

	// Use buttons to toggle between views
	document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
	document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
	document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
	document.querySelector('#compose').addEventListener('click', compose_email);

	// By default, load the inbox
	load_mailbox('inbox');

	// Submits a new email
	document.querySelector('#compose-form').onsubmit = function () {
		// Prevent default submission
		event.preventDefault();

		// Get the contents of the email
		const recipients = document.querySelector('#compose-recipients').value;
		const subject = document.querySelector('#compose-subject').value;
		const body = document.querySelector('#compose-body').value;

		// Save the email via API
		fetch('/emails', {
			method: 'POST',
			body: JSON.stringify({
				recipients: recipients,
				subject: subject,
				body: body
			})
		})
			// Load the user's sent mailbox
			.then(function () {
				load_mailbox('sent')
			})
	};

});

function compose_email() {

	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'block';

	// Clear out composition fields
	document.querySelector('#compose-recipients').value = '';
	document.querySelector('#compose-subject').value = '';
	document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#compose-view').style.display = 'none';

	// Show the mailbox name
	// document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><ul id="emails"></ul>`;
	// document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><table id="emails"><tr><th id="recipients">To</th><th id="subject">Subject</th><th id="timestamp">Sent</th></tr></table>`;
	document.querySelector('#email-header').innerHTML = `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`;
	// document.querySelector('#my-table').innerHTML = ''
	document.querySelector('#emails').innerHTML = '';


	fetch('/emails/' + mailbox)
		.then(response => response.json())
		.then(emails => {
			// Find parent container
			const parentContainer = document.getElementById("emails");
			// console.log(emails);
			emails.forEach(item => {
				const emailContainer = document.createElement('div');
				// emailContainer.setAttribute("id", item.id);
				emailContainer.addEventListener('click', () => show_email(item.id));
				emailContainer.style.display = "flex";
				emailContainer.style.borderStyle = "solid";
				emailContainer.style.borderWidth = "1px";
				emailContainer.style.borderColor = "black";
				emailContainer.style.padding = "5px";
				parentContainer.append(emailContainer);
				const read = item.read;
				if (read == true) {
					// Email was read
					emailContainer.style.backgroundColor = "gray";
				} else {
					// Email was not read
					emailContainer.style.backgroundColor = "white";
				}
				list_email(emailContainer, item.sender);
				list_email(emailContainer, item.subject);
				list_email(emailContainer, item.timestamp);

				// If the contents of an email need to be viewed
				// emailContainer.onclick = alert(`you clicked email ${item.id}`)
				// document.querySelector(`#${id}`).addEventListener('click', alert(`you clicked email ${item.id}`));
			});
		});
}

function list_email(parentContainer, field) {
	const emailFieldContainer = document.createElement('div');
	emailFieldContainer.innerHTML = field;
	parentContainer.append(emailFieldContainer);
	emailFieldContainer.style.margin = "0px 25px 0px";
	// if (field == timestamp) {
	// 	emailFieldContainer.style.alignSelf = "right";
	// }
}

function show_email(emailId) {
	console.log(emailId);
	fetch('/emails/100')
		.then(response => response.json())
		.then(email => {
			// Print email
			console.log(email);

			// ... do something else with email ...
		});
}