let baseurl ="https://ksheeram.onrender.com"
const updateCartCountUI = (totalQuantity = 0) => {
  const cartCountElement = document.getElementById("cart-count");
  if (!cartCountElement) return;

  const currentCount = parseInt(cartCountElement.textContent);
  cartCountElement.textContent = totalQuantity;

  if (totalQuantity > 0 && totalQuantity !== currentCount) {
    cartCountElement.classList.add("updated");
    setTimeout(() => cartCountElement.classList.remove("updated"), 300);
  }
};

const loadInitialCartCount = async () => {
  try {
    const response = await fetch(`${baseurl}/cart/get`);
    if (!response.ok) throw new Error("Failed to fetch");
    const cart = await response.json();
    updateCartCountUI(cart.count || 0);
  } catch (error) {
    console.error("Failed to load initial cart count:", error);
    updateCartCountUI(0);
  }
};

document.addEventListener("DOMContentLoaded", () => {
  loadInitialCartCount();
  
  document.addEventListener('cartCountUpdated', (event) => {
    if (event.detail && typeof event.detail.count !== 'undefined') {
      updateCartCountUI(event.detail.count);
    }
  });
});
