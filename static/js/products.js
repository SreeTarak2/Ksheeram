document.addEventListener("DOMContentLoaded", () => {
  let cart = [];
  const url = "http://127.0.0.1:5000";

  // API helper function
  const apiCall = async (url, options = {}) => {
    try {
      const response = await fetch(url, {
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("API call failed:", error);
      throw error;
    }
  };

  // Load cart from backend to check which items are already added
  const loadCart = async () => {
    try {
      const response = await apiCall(`${url}/cart/get`);
      cart = response.items || [];
      updateCartCount();
      markAddedButtons();
    } catch (error) {
      console.error("Failed to load cart:", error);
      cart = [];
      updateCartCount();
    }
  };

  const updateCartCount = () => {
    const cartCountElement = document.getElementById("cart-count");
    if (!cartCountElement) return;

    const totalQuantity = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCountElement.textContent = totalQuantity;
    if (totalQuantity > 0) {
      cartCountElement.classList.add("updated");
      setTimeout(() => cartCountElement.classList.remove("updated"), 300);
    }
  };

  // Target both nearby and other product grids
  const nearbyProductGrid = document.getElementById("nearby-product-grid");
  const otherProductGrid = document.getElementById("other-product-grid");

  if (!nearbyProductGrid && !otherProductGrid) return;

  const addToCart = async (product) => {
    try {
      // Add to backend cart
      await apiCall(`${url}/cart/add`, {
        method: "POST",
        body: JSON.stringify({
          seller_id: product.id,
          name: product.name,
        }),
      });

      // Update local cart state
      const existingItem = cart.find(
        (item) => item.seller_id === product.id && item.name === product.name
      );

      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        cart.push({
          seller_id: product.id,
          name: product.name,
          price: product.price,
          seller_name: product.seller,
          image_url: product.image_url,
          unit: product.unit || "piece",
          quantity: 1,
        });
      }

      updateCartCount();
      return true;
    } catch (error) {
      console.error("Failed to add to cart:", error);
      alert("Failed to add item to cart. Please try again.");
      return false;
    }
  };

  const markAddedButtons = () => {
    const buttons = document.querySelectorAll(".add-to-cart-btn");

    buttons.forEach((btn) => {
      const sellerId = btn.dataset.sellerId;
      const productName = btn.dataset.productName;

      // Check if this specific product from this seller is in cart
      const inCart = cart.some(
        (item) => item.seller_id === sellerId && item.name === productName
      );

      if (inCart) {
        btn.innerHTML = '<i class="fas fa-check"></i> Added!';
        btn.classList.add("added");
        btn.disabled = true;
      } else {
        btn.innerHTML = '<i class="fas fa-cart-plus"></i> Add to Cart';
        btn.classList.remove("added");
        btn.disabled = false;
      }
    });
  };

  const handleAddToCart = async (e) => {
    const button = e.target.closest(".add-to-cart-btn");
    if (!button || button.classList.contains("added")) return;

    // Show loading state
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
    button.disabled = true;

    const product = {
      id: button.dataset.sellerId,
      name: button.dataset.productName,
      price: parseFloat(button.dataset.productPrice),
      seller: button.dataset.productSeller,
      image_url: button.dataset.productImage,
      unit: button.dataset.productUnit,
    };

    const success = await addToCart(product);

    if (success) {
      button.innerHTML = '<i class="fas fa-check"></i> Added!';
      button.classList.add("added");
    } else {
      button.innerHTML = originalText;
      button.disabled = false;
    }
  };

  // Attach event listeners to both grids
  if (nearbyProductGrid) {
    nearbyProductGrid.addEventListener("click", handleAddToCart);
  }

  if (otherProductGrid) {
    otherProductGrid.addEventListener("click", handleAddToCart);
  }

  loadCart();
});
