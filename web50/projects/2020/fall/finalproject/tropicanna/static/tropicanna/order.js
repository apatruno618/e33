document.addEventListener('DOMContentLoaded', function () {
	// Calculates order
	document.querySelector('#calculate').addEventListener('click', () => calculateOrder());

	// Saves order
	document.querySelector('#save').addEventListener('click', () => saveOrder());
});

function calculateOrder() {
	// Prevent default submission
	event.preventDefault();

	// Gets the contents of the form
	const orderedItems = []
	let orderTotal = 0;

	document.querySelectorAll('input').forEach(input => {
		// ignore submit button
		if (input.getAttribute("category")) {
			const quantity = parseInt(input.value);
			// only save ordered products
			if (quantity > 0) {
				const category = parseInt(input.getAttribute("category"));
				const flavor = parseInt(input.getAttribute("flavor"));
				const price = parseInt(input.getAttribute("price"));
				const totalItemPrice = price * quantity;
				// Displays the item total
				document.querySelector(`[category-id="${category}"][flavor-id="${flavor}"]`).value = "$" + totalItemPrice;
				const orderedItem = { category: category, flavor: flavor, quantity: quantity, totalItemPrice: totalItemPrice }
				orderTotal += totalItemPrice;
				orderedItems.push(orderedItem);
			}
		}
	})
	// calculate order total
	document.querySelector('#order-total').value = "$" + orderTotal;
	return { orderTotal, orderedItems };
};

function saveOrder() {
	// Prevents default submission and aggregates ordered item information
	const { orderTotal, orderedItems } = calculateOrder();
	const customerId = parseInt(document.querySelector('select').value);

	if (orderTotal > 0) {
		fetch('/save_order', {
			method: 'POST',
			body: JSON.stringify({
				customerId: customerId,
				orderTotal: orderTotal,
				orderedItems: orderedItems
			})
		})
			// Ensure the user the order was saved
			.then(() => {
				console.log("order saved")
			})
			// Catch any errors and log them to the console
			.catch(error => {
				console.log('Error:', error);
			});
	}
	else
		console.log("An order must contain at least 1 item")
}