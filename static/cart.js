let cartIcon = document.querySelector('#cart-icon')
let cart = document.querySelector('.cart')
let cartBTNClose = document.querySelector('#btn-cart-close')

// Add the "active" class to the cart when the cart icon is clicked
cartIcon.onclick = () => {
    cart.classList.add("active")
}

// Remove the "active" class from the cart when the close button is clicked
cartBTNClose.onclick = () => {
    cart.classList.remove("active")
}

if (document.readyState == 'loading') {
    // If the page is still loading, add an event listener for when it finishes loading
    document.addEventListener('DOMContentLoaded', ready)
    updateTotal(); // Update the total while we wait
} else {
    ready(); // The page is already finished loading, so run the ready() function
    updateTotal(); // Update the total
}

function ready() {
    // Get all the elements with the "cart-remove" class and add an event listener to each of them
    var removeCartButtons = document.getElementsByClassName('cart-remove')
    console.log(removeCartButtons)
    for (var i = 0; i < removeCartButtons.length; i++) {
        var button = removeCartButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    // Get all the elements with the "cart-quantity" class and add an event listener to each of them
    var quantityInputs = document.getElementsByClassName('cart-quantity')
    for (var i = 0; i < quantityInputs.length; i++) {
        var input = quantityInputs[i]
        input.addEventListener('change', quantityChanged);
    }

    // Get all the elements with the "add-cart" class and add an event listener to each of them
    var addCart = document.getElementsByClassName('add-cart')
    for (var i = 0; i < addCart.length; i++) {
        var button = addCart[i]
        button.addEventListener('click', addCartClicked);

    }
    updateTotal(); // Update the total after all the event listeners are added
}

function removeCartItem(event) {
    // When a "cart-remove" element is clicked, remove the parent element (which is the whole cart item)
    var buttonClicked = event.target
    buttonClicked.parentElement.remove()
    updateTotal(); // Update the total after an item is removed
}

function purchaseButton(event) {
    // When the purchase button is clicked, show an alert
    alert('Items Purchased')
}

function quantityChanged(event) {
    var input = event.target
    // If the input value is not a number or is less than or equal to 0, set it to 1
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateTotal(); // Update the total after a quantity is changed
}

function addCartClicked(event) {
    var button = event.target
    var shopProducts = button.parentElement
    var title = shopProducts.getElementsByClassName('product-title')[0].innerText;
    var price = shopProducts.getElementsByClassName('price')[0].innerText;
    var productImg = shopProducts.getElementsByClassName('product-img')[0].src;
    // Add the product to the cart by calling the addProductToCart() function
    addProductToCart(title, price, productImg);
    updateTotal(); // Update the total after a product is added to the cart
}

function addProductToCart(title, price, productImg) {
    // Create a new div element to hold the cart item
    var cartShopBox = document.createElement('div');
    cartShopBox.classList.add('cart-box');
    var cartItems = document.getElementsByClassName('cart-content')[0];
    // Check if the product is already in the cart
    var cartItemsNames = cartItems.getElementsByClassName('cart-product-title');
    for (var i = 0; i < cartItemsNames.length; i++) {
        if (cartItemsNames[i].innerText == title) {
            // If the product is already in the cart, show an alert and do not add it again
            alert('Item is already in cart.');
            return;
        }
    }

    // If the product is not already in the cart, add it
    var cartBoxContent = `
                    <img src='${productImg}' alt="cover art" class="cart-img">
                    <div class="detail-box">
                        <div class="cart-product-title">${title}</div>
                        <div class="cart-price">${price}</div>
                    <input type="number" value="1" class="cart-quantity">
                    </div>
                    <!-- Cart Remove-->
                    <i class="bx bxs-trash-alt cart-remove"></i>`;
    cartShopBox.innerHTML = cartBoxContent
    cartItems.append(cartShopBox)

    // Add event listeners to the new cart item
    cartShopBox.getElementsByClassName('cart-remove')[0].addEventListener('click', removeCartItem);
    cartShopBox.getElementsByClassName('cart-quantity')[0].addEventListener('change', quantityChanged);
    updateTotal(); // Update the total after the new item is added
}

function updateTotal(){
    var cartContent = document.getElementsByClassName('cart-content')[0];
    var cartBoxes = cartContent.getElementsByClassName('cart-box');
    var total = 0;

    for (var i = 0; i < cartBoxes.length; i++){
        var cartBox = cartBoxes[i]
        var priceElement = cartBox.getElementsByClassName('cart-price')[0];
        var quantityElement = cartBox.getElementsByClassName('cart-quantity')[0];
        var price = parseFloat(priceElement.innerText.replace( "£", ""));
        var quantity = quantityElement.value
        total = total + (price * quantity);

        total = Math.round(total *100)/100;
        document.getElementsByClassName('cart-total-price')[0].innerText = "£" + total;
        
    }
    if (cartBoxes.length == 0)
    {
        document.getElementsByClassName('cart-total-price')[0].innerText = "£0"; 
    }
}
// This code is for a shopping cart system. It adds event listeners to various elements on the page, such as the "add to cart" buttons, "remove item" buttons, and quantity inputs. It also contains functions for adding and removing items from the cart, and for updating the total price of all items in the cart.