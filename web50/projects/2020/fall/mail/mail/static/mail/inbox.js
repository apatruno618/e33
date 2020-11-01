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

		// Gets the contents of the email
		const recipients = document.querySelector('#compose-recipients').value;
		const subject = document.querySelector('#compose-subject').value;
		const body = document.querySelector('#compose-body').value;

		// Saves the email via API
		fetch('/emails', {
			method: 'POST',
			body: JSON.stringify({
				recipients: recipients,
				subject: subject,
				body: body
			})
		})
			// Load the user's sent mailbox
			.then(() => load_mailbox('sent'))
	};

});

function compose_email() {

	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'none';
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
	document.querySelector('#email-view').style.display = 'none';

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
				// Displays content of email when clicked
				emailContainer.addEventListener('click', () => showEmail(item.id));
				emailContainer.style.display = "flex";
				emailContainer.style.borderStyle = "solid";
				emailContainer.style.borderWidth = "1px";
				emailContainer.style.borderColor = "black";
				emailContainer.style.padding = "5px";
				// Adds each email line to the parent div
				parentContainer.append(emailContainer);
				const read = item.read;
				if (read == true) {
					// Email was read
					emailContainer.style.backgroundColor = "gray";
				} else {
					// Email was not read
					emailContainer.style.backgroundColor = "white";
				}
				// Appends fields to each email line
				addEmailField(emailContainer, item.sender);
				addEmailField(emailContainer, item.subject);
				addEmailField(emailContainer, item.timestamp);
			});
		});
}

function addEmailField(parentContainer, field) {
	// Creates parent container of each field
	const emailFieldContainer = document.createElement('div');
	emailFieldContainer.innerHTML = field;
	parentContainer.append(emailFieldContainer);
	emailFieldContainer.style.margin = "0px 25px 0px";
}

function showEmail(emailId) {
	// Show the email and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'block';

	// Finds email contents based on its id
	fetch('/emails/' + emailId)
		.then(response => response.json())
		.then(email => {
			document.querySelector('#sender').innerHTML = `From: ${email.sender}`;
			document.querySelector('#recipients').innerHTML = `To: ${email.recipients}`;
			document.querySelector('#subject').innerHTML = `Subject: ${email.subject}`;
			document.querySelector('#timestamp').innerHTML = `Timestamp: ${email.timestamp}`;
			document.querySelector('#email-body').innerHTML = `${email.body}`;
			const archiveButton = document.querySelector('#archive');
			// Decides content of archive button
			if (email.archived == true) {
				archiveButton.innerHTML = "Unarchive";
			} else {
				archiveButton.innerHTML = "Archive";
			}
			// Updates read status
			if (email.read == false) {
				fetch('/emails/' + emailId, {
					method: 'PUT',
					body: JSON.stringify({
						read: true
					})
				})
			}
			const archiveStatus = document.querySelector('#archive').innerHTML.toLowerCase();
			// console.log(archiveStatus);
			// console.log(document.querySelector('#archive').innerHTML);
			document.querySelector('#archive').addEventListener('click', () => setArchive(email.id, archiveStatus));
			document.querySelector('#reply').addEventListener('click', () => preFillComposeEmail(email.sender, email.subject, email.timestamp, email.body));
		})
};

function setArchive(emailId, archiveStatus) {
	let archiveBool;
	console.log(archiveBool);
	if (archiveStatus == 'archive') {
		archiveBool = true
	} else {
		archiveBool = false
	}
	fetch('/emails/' + emailId, {
		method: 'PUT',
		body: JSON.stringify({
			archived: archiveBool
		})
	}).then(() => load_mailbox('inbox'))
};

function preFillComposeEmail(sender, subject, timestamp, body) {
	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'block';

	// Clear out composition fields
	document.querySelector('#compose-recipients').value = sender;
	document.querySelector('#compose-subject').value = subject;
	document.querySelector('#compose-body').value = `On ${timestamp} ${sender} wrote: "${body}"`;
};