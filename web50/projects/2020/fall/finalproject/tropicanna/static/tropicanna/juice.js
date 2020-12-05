document.addEventListener('DOMContentLoaded', function () {
	// Submits a new customer
	document.querySelector('#customer-form').addEventListener('submit', () => saveNewCustomer())

	// Submits new flavor
	document.querySelector('#flavor-form').addEventListener('submit', () => saveNewFlavor())
});


function saveNewCustomer() {
	// Prevent default submission
	event.preventDefault();

	// Gets the contents of the form
	const customerName = document.querySelector('#customer-name').value;
	const customerPhone = document.querySelector('#customer-phone').value;

	// Saves the customer via API
	fetch('/customer', {
		method: 'POST',
		body: JSON.stringify({
			customerName: customerName,
			customerPhone: customerPhone
		})
	})
		// Display the new customer
		.then(() => {
			const newCustomerItem = document.createElement('li');
			newCustomerItem.innerHTML = customerName + ' - Tel: ' + customerPhone;
			document.querySelector('#new-customer-anchor').append(newCustomerItem);
			console.log('customer saved');
		})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
};


function saveNewFlavor() {
	// Prevent default submission
	event.preventDefault();

	// Gets the contents of the form
	const flavorName = document.querySelector('#flavor-name').value;
	// Saves the email via API
	fetch('/flavor', {
		method: 'POST',
		body: JSON.stringify({
			flavorName: flavorName
		})
	})
		// Display the new flavor
		.then(() => {
			const newFlavorItem = document.createElement('li');
			newFlavorItem.innerHTML = flavorName;
			document.querySelector('#new-flavor-anchor').append(newFlavorItem);
			console.log('flavor saved');
		})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
};

