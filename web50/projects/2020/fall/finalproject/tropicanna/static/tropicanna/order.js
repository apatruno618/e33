document.addEventListener('DOMContentLoaded', function () {
	// Calculates order
	document.querySelector('#order-form').addEventListener('submit', () => calculateOrder())
});

function calculateOrder() {
	// Prevent default submission
	event.preventDefault();

	// Gets the contents of the form
	const customerId = document.querySelector('select').value;
	console.log(customerId);

	const orderedItems = []
	document.querySelectorAll('input').forEach(input => {
		// ignore submit button
		if (input.getAttribute("category")) {
			const quantity = input.value;
			// only save ordered products
			if (quantity > 0) {
				const category = parseInt(input.getAttribute("category"));
				const flavor = parseInt(input.getAttribute("flavor"));
				const price = parseInt(input.getAttribute("price"));
				const orderedItem = { category: category, flavor: flavor, quantity: quantity, price: price }
				const totalPrice = price * quantity;
				console.log(totalPrice);
				document.querySelector(`[category-id="${category}"][flavor-id="${flavor}"]`).value = "$" + totalPrice;
				orderedItems.push(orderedItem);
			}
		}
	})
	console.log(orderedItems);
};