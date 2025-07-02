document.addEventListener("DOMContentLoaded", () => {
  let cart = [];

  const apiCall = async (url, options = {}) => {
    try {
      const response = await fetch(url, {
        headers: { "Content-Type": "application/json", ...options.headers },
        ...options,
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(
          result.error || `HTTP error! status: ${response.status}`
        );
      }
      return result;
    } catch (error) {
      console.error("API call failed:", error.message);
      alert(error.message);
      throw error;
    }
  };

  const loadCart = async () => {
    try {
      const response = await apiCall(`/cart/get`);
      cart = response.items || [];
      renderCartItems();
      updateCartCount(response.count);
    } catch (error) {
      cart = [];
      renderCartItems();
      updateCartCount(0);
    }
  };

  const updateCartItemQuantity = async (productKey, quantity) => {
    try {
      await apiCall(`/cart/update`, {
        method: "POST",
        body: JSON.stringify({
          product_key: productKey,
          quantity: quantity,
        }),
      });
      const item = cart.find((i) => i.product_key === productKey);
      if (item) {
        item.quantity = quantity;
      }
      await loadCart();
    } catch (error) {
      alert("Failed to update cart. Please refresh and try again.");
      loadCart();
    }
  };

  const removeCartItem = async (productKey) => {
    try {
      await apiCall(`/cart/remove`, {
        method: "POST",
        body: JSON.stringify({ product_key: productKey }),
      });
      await loadCart();
    } catch (error) {
      alert("Failed to remove item from cart. Please try again.");
    }
  };

  const updateCartCount = (count) => {
    const cartCountElement = document.getElementById("cart-count");
    if (!cartCountElement) return;
    cartCountElement.textContent = count;
    if (count > 0) {
      cartCountElement.classList.add("updated");
      setTimeout(() => cartCountElement.classList.remove("updated"), 300);
    }
  };

  const debounce = (func, delay = 350) => {
    let timeoutId;
    return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
  };

  const cartLayout = document.getElementById("cart-layout");
  const emptyCartMsg = document.getElementById("empty-cart-message");
  const cartList = document.getElementById("cart-item-list");

  if (!cartLayout || !cartList) return;

  const updateSummary = () => {
    const subtotalElem = document.getElementById("summary-subtotal");
    const deliveryElem = document.getElementById("summary-delivery");
    const totalElem = document.getElementById("summary-total");
    const deliveryFee = cart.length > 0 ? 20.0 : 0.0;

    const subtotal = cart.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );
    const total = subtotal + deliveryFee;

    if (subtotalElem) subtotalElem.textContent = `₹${subtotal.toFixed(2)}`;
    if (deliveryElem) deliveryElem.textContent = `₹${deliveryFee.toFixed(2)}`;
    if (totalElem) totalElem.textContent = `₹${total.toFixed(2)}`;
  };

  const renderCartItems = () => {
    if (cart.length === 0) {
      if (cartLayout) cartLayout.style.display = "none";
      if (emptyCartMsg) emptyCartMsg.style.display = "block";
      updateSummary();
      return;
    }

    if (cartLayout) cartLayout.style.display = "flex";
    if (emptyCartMsg) emptyCartMsg.style.display = "none";
    cartList.innerHTML = "";

    cart.forEach((item) => {
      const li = document.createElement("li");
      li.className = "cart-item";
      li.dataset.productKey = item.product_key;

      li.innerHTML = `
        <img src="${item.image_url || "default_image_url.jpg"}" alt="${
        item.name
      }" class="item-image" />
        <div class="item-details">
          <h4>${item.name}</h4>
          <p class="item-seller">From: ${item.seller_name}</p>
          <p class="item-unit">Unit: ${item.unit}</p>
        </div>
        <div class="item-quantity">
          <button class="quantity-btn js-quantity-minus" aria-label="Decrease quantity" ${
            item.type === "plan" ? "disabled" : ""
          }>-</button>
          <input type="text" value="${
            item.quantity
          }" class="quantity-input" aria-label="Quantity" ${
        item.type === "plan" ? "readonly" : ""
      } />
          <button class="quantity-btn js-quantity-plus" aria-label="Increase quantity" ${
            item.type === "plan" ? "disabled" : ""
          }>+</button>
        </div>
        <div class="item-price">₹${(item.price * item.quantity).toFixed(
          2
        )}</div>
        <button class="item-remove js-remove-item" aria-label="Remove item">
          <i class="fas fa-trash-alt"></i>
        </button>
      `;
      cartList.appendChild(li);
    });

    updateSummary();
  };

  const debouncedQuantityUpdate = debounce((productKey, newQuantity) => {
    updateCartItemQuantity(productKey, newQuantity);
  });

  cartList.addEventListener("click", (e) => {
    const target = e.target;
    const cartItemEl = target.closest(".cart-item");
    if (!cartItemEl) return;

    const productKey = cartItemEl.dataset.productKey;
    const item = cart.find((i) => i.product_key === productKey);
    if (item && item.type === "plan") {
      if (target.matches(".js-remove-item, .js-remove-item *")) {
        if (
          confirm(`Remove subscription plan "${item.name}" from your cart?`)
        ) {
          removeCartItem(productKey);
        }
      }
      return;
    }

    if (target.matches(".js-quantity-plus")) {
      const input = cartItemEl.querySelector(".quantity-input");
      const newValue = parseInt(input.value) + 1;
      debouncedQuantityUpdate(productKey, newValue);
    } else if (target.matches(".js-quantity-minus")) {
      const input = cartItemEl.querySelector(".quantity-input");
      const currentValue = parseInt(input.value);
      if (currentValue > 1) {
        const newValue = currentValue - 1;
        debouncedQuantityUpdate(productKey, newValue);
      }
    }

    if (target.matches(".js-remove-item, .js-remove-item *")) {
      if (confirm(`Remove "${item.name}" from your cart?`)) {
        removeCartItem(productKey);
      }
    }
  });

  cartList.addEventListener("input", (e) => {
    if (e.target.classList.contains("quantity-input")) {
      const cartItemEl = e.target.closest(".cart-item");
      const productKey = cartItemEl.dataset.productKey;
      let value = parseInt(e.target.value);
      if (isNaN(value) || value < 1) {
        value = 1;
      }
      debouncedQuantityUpdate(productKey, value);
    }
  });

  const checkoutBtn = document.getElementById("checkout-btn");
  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", async () => {
      const selectedPaymentMethod = document.querySelector(
        'input[name="payment-method"]:checked'
      );
      if (!selectedPaymentMethod) {
        alert("Please select a payment method.");
        return;
      }

      // Show a loading state
      checkoutBtn.disabled = true;
      checkoutBtn.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> Contacting Bank...';

      try {
        // *** THE ONLY CHANGE IS THIS URL ***
        const response = await fetch("/fake_payment/initiate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          // You can still send data if your fake endpoint needs it
          body: JSON.stringify({
            payment_method: selectedPaymentMethod.value,
          }),
        });

        const result = await response.json();

        if (response.ok && result.success) {
          // Handle success from the backend
          alert(result.message);
          // Redirect on success
          window.location.href = result.redirect;
        } else {
          // Handle failure from the backend (using the 'error' key)
          throw new Error(result.error || "An unknown error occurred.");
        }
      } catch (error) {
        // Display the error message and restore the button
        alert(error.message);
        checkoutBtn.disabled = false;
        checkoutBtn.innerHTML = "Proceed to Checkout";
      }
    });
  }

  loadCart();
});
