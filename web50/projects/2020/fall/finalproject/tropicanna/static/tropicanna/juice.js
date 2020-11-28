document.addEventListener('DOMContentLoaded', function () {
	// Submits a new customer
	document.querySelector('#customer-form').addEventListener('submit', () => saveNewCustomer())
	// Submits new category of products
	document.querySelector('#category-form').addEventListener('submit', () => saveNewCategory())
});

function saveNewCustomer() {
	// Prevent default submission
	event.preventDefault();

	// Gets the contents of the form
	const customerName = document.querySelector('#customer-name').value;
	const customerPhone = document.querySelector('#customer-phone').value;

	// Saves the email via API
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
			newCustomerItem.innerHTML = customerName, customerPhone;
			document.querySelector('#new-customer-anchor').append(newCustomerItem);
			console.log('customer saved');
		})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
}

function saveNewCategory() {
	// Prevent default submission
	event.preventDefault();

	// Gets the contents of the form
	const categoryName = document.querySelector('#category-name').value;
	const categoryPrice = document.querySelector('#category-price').value;

	// Saves the email via API
	fetch('/category', {
		method: 'POST',
		body: JSON.stringify({
			categoryName: categoryName,
			categoryPrice: categoryPrice
		})
	})
		// Display the new category
		.then(() => {
			const newCategoryItem = document.createElement('li');
			newCategoryItem.innerHTML = categoryName, categoryPrice;
			document.querySelector('#new-category-anchor').append(newCategoryItem);
			console.log('category saved');
		})
		// Catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
		});
}