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
				fetch('/emails/sent')
					.then(response => response.json())
					.then(emails => {
						load_mailbox('sent')
						const emailList = document.querySelector('#emails');
						emails.forEach(item => {
							const recipients = item.recipients;
							const subject = item.subject;
							const timestamp = item.timestamp;
							const recipientField = document.createElement('td');
							recipientField.innerHTML = recipients;
							emailList.append(recipientField);
							const subjectField = document.createElement('td');
							subjectField.innerHTML = subject;
							emailList.append(subjectField);
							const timestampField = document.createElement('td');
							timestampField.innerHTML = timestamp;
							// let emailview = document.querySelector('#emails-view')
							emailList.append(timestampField);
						});

					})
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
	document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><table id="emails"><tr><th id="recipients">To</th><th id="subject">Subject</th><th id="timestamp">Sent</th></tr></table>`;

}