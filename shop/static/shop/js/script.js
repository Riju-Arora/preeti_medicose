document.addEventListener("DOMContentLoaded", () => {
  console.log("Preeti Medicose Website Loaded 🚀");

  let cart = [];
const cartBox = document.getElementById("cart");
const cartButton = document.getElementById("cartButton");
const closeCart = document.getElementById("closeCart");

// Open cart when floating button clicked
cartButton.addEventListener("click", () => {
  cartBox.style.display = "block";
});

// Close cart when "Close" button clicked
closeCart.addEventListener("click", () => {
  cartBox.style.display = "none";
});

  // ✅ Add product to cart (with quantity)
  function addToCart(name, price) {
    let existingItem = cart.find(item => item.name === name);
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      cart.push({ name, price, quantity: 1 });
    }
    updateCart();
  }

  // ✅ Decrease quantity / remove product
  function decreaseFromCart(name) {
    let item = cart.find(item => item.name === name);
    if (item) {
      item.quantity -= 1;
      if (item.quantity <= 0) {
        cart = cart.filter(i => i.name !== name);
      }
    }
    updateCart();
  }

  // ✅ Update cart UI
  function updateCart() {
    const cartList = document.getElementById("cart-items");
    cartList.innerHTML = "";

    let total = 0;
    cart.forEach((item, index) => {
      total += item.price * item.quantity;

      let li = document.createElement("li");
      li.className = "flex justify-between items-center py-2 border-b";

      li.innerHTML = `
        <span>${item.name} - ₹${item.price} x ${item.quantity}</span>
        <div class="flex items-center gap-2">
          <button class="decrease bg-red-500 text-white px-2 rounded" data-name="${item.name}">–</button>
          <button class="increase bg-green-500 text-white px-2 rounded" data-name="${item.name}">+</button>
        </div>
      `;

      cartList.appendChild(li);
    });

    document.getElementById("cart-total").textContent = `Total: ₹${total}`;

    // Attach listeners to new buttons
    document.querySelectorAll(".increase").forEach(btn => {
      btn.addEventListener("click", () => {
        let name = btn.getAttribute("data-name");
        let item = cart.find(i => i.name === name);
        if (item) addToCart(item.name, item.price);
      });
    });

    document.querySelectorAll(".decrease").forEach(btn => {
      btn.addEventListener("click", () => {
        let name = btn.getAttribute("data-name");
        decreaseFromCart(name);
      });
    });
  }

  // ✅ Checkout with WhatsApp
  function checkout() {
    if (cart.length === 0) {
      alert("Your cart is empty!");
      return;
    }

    let orderText = "🛒 *New Order from Preeti Medicose* %0A%0A";
    cart.forEach((item, index) => {
      orderText += `${index + 1}. ${item.name} - ₹${item.price} x ${item.quantity}%0A`;
    });

    let total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    orderText += `%0A💰 *Total:* ₹${total}%0A%0A📞 Contact: 8950120349`;

    let phoneNumber = "918950120349"; // WhatsApp number
    let url = `https://wa.me/${phoneNumber}?text=${orderText}`;

    window.open(url, "_blank");
  }

  // Attach Add to Cart button listeners
  const buttons = document.querySelectorAll(".add-to-cart");
  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".product-card");
      const name = card.getAttribute("data-name");
      const price = parseInt(card.getAttribute("data-price"));
      addToCart(name, price);
    });
  });

  // Attach checkout button (make sure you have <button onclick="checkout()">Checkout</button> in HTML)
  window.checkout = checkout;
});
// Function to open cart
function openCart() {
    document.getElementById("cartSidebar").classList.remove("hidden");
    document.getElementById("cartSidebar").classList.add("show");
}

// Function to close cart
function closeCart() {
    document.getElementById("cartSidebar").classList.remove("show");
    document.getElementById("cartSidebar").classList.add("hidden");
}

// Example Add to Cart function
function addToCart(productName, price) {
    let cartItems = document.getElementById("cartItems");

    let li = document.createElement("li");
    li.textContent = productName + " - ₹" + price;
    cartItems.appendChild(li);

    // 👉 Open cart automatically after adding item
    openCart();
}

