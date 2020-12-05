# Final Project: Tropicanna
+ By: Anna Patruno

+ This application was intended to serve as a tool for a small business that distributes juice products to supermarkets and bodegas in the NYC area.

## Landing Page

+ For non-logged in users, this page serves as a summary of available products (defined as a combination of category and flavor).
+ For logged in users, there's an additional display of non-delivered orders containing links to each order's page.

## Controls Page

+ This page serves as a main control center for logged in users where they can add new customers, categories of products, and flavors.
+ New customers and flavors are displayed directly on the page and are saved to the database via Javascript fetch calls.
+ Adding a new category instead directs the user to the new category's page where they can associate flavors to that category. The dropdown display flavors that are not currently associated to said category. This is done via an exclusion django query in views.py.
+ This page also displays a list of all orders and links to each of the order's pages.

## Category Pages

+ Each category is display on its own page.
+ The price, already associated flavors, and non-associated flavors are listed.

## Submit an order

+ Displays a form where a customer is selected via a dropdown and "products" (categories with a flavor) are listed.
+ Each product has an input option to enter the quantity of the desired item.
+ Clicking the "Calculate" button displays the total prices of each product and the order. These calculations are accomplished via Javascript. Category prices and flavors are saved as attributes in order.html and accessed in order.js in order to perform the calculations. This is a neat feature because it allows the user to calculate an order as many times (in case a customer wants to make sure they're staying in budget while placing an order) without saving it to the database.
+ Clicking the "Save Order" button utilizes the calculateOrder() function in juice.js, assembles all the data needed related to the order and the ordered items and send that to the backend to be saved to the database in the save_order() function of views.py. The general order data is saved to the order model while each product (again, an association of category and flavor) is saved to the orderedItem model.

