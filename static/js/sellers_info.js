document.addEventListener("DOMContentLoaded", () => {
  let cartItems = [];
  const plansContainer = document.getElementById("plans");
  const productContainer = document.getElementById("products");

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

  const fetchCartState = async () => {
    try {
      const cart = await apiCall("/cart/get");
      cartItems = cart.items || [];
      updateButtonStates();
      const cartCountEvent = new CustomEvent("cartCountUpdated", {
        detail: { count: cart.count || 0 },
      });
      document.dispatchEvent(cartCountEvent);
    } catch (error) {
      console.error("Error fetching cart state:", error);
    }
  };

  const addPlanToCartAPI = (planData) => {
    return apiCall("/cart/add-plan", {
      method: "POST",
      body: JSON.stringify(planData),
    });
  };

  const addProductToCartAPI = (productData) => {
    return apiCall("/cart/add", {
      method: "POST",
      body: JSON.stringify(productData),
    });
  };

  const removeCartItemAPI = (productKey) => {
    return apiCall("/cart/remove", {
      method: "POST",
      body: JSON.stringify({ product_key: productKey }),
    });
  };

  const updateButtonStates = () => {
    if (productContainer) {
      productContainer.querySelectorAll(".add-to-cart-btn").forEach((btn) => {
        const productKey = `${btn.dataset.sellerId}_${btn.dataset.name}`;
        const inCart = cartItems.some(
          (item) => item.product_key === productKey
        );

        btn.disabled = false;
        if (inCart) {
          btn.innerHTML = '<i class="fas fa-check"></i> Added';
          btn.classList.add("added");
          btn.disabled = true;
        } else {
          btn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
          btn.classList.remove("added");
        }
      });
    }

    if (plansContainer) {
      plansContainer.querySelectorAll(".subscribe-btn").forEach((btn) => {
        const planKey = `${btn.dataset.sellerId}_${btn.dataset.planName}`;
        const inCart = cartItems.some((item) => item.product_key === planKey);

        btn.disabled = false;
        if (inCart) {
          btn.innerHTML = '<i class="fas fa-trash-alt"></i> Remove Plan';
          btn.classList.add("in-cart");
        } else {
          btn.innerHTML = '<i class="fas fa-cart-plus"></i> Choose Plan';
          btn.classList.remove("in-cart");
        }
      });
    }
  };

  if (productContainer) {
    productContainer.addEventListener("click", async (e) => {
      const button = e.target.closest(".add-to-cart-btn");
      if (!button || button.disabled) return;

      button.disabled = true;
      button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';

      try {
        await addProductToCartAPI({
          name: button.dataset.name,
          seller_id: button.dataset.sellerId,
        });
        await fetchCartState();
      } catch (error) {
        updateButtonStates();
      }
    });
  }

  if (plansContainer) {
    plansContainer.addEventListener("click", async (e) => {
      const button = e.target.closest(".subscribe-btn");
      if (!button || button.disabled) return;

      const planKey = `${button.dataset.sellerId}_${button.dataset.planName}`;
      button.disabled = true;

      try {
        if (button.classList.contains("in-cart")) {
          button.innerHTML =
            '<i class="fas fa-spinner fa-spin"></i> Removing...';
          await removeCartItemAPI(planKey);
        } else {
          button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
          await addPlanToCartAPI({
            plan_name: button.dataset.planName,
            seller_id: button.dataset.sellerId,
          });
        }
        await fetchCartState();
      } catch (error) {
        updateButtonStates();
      }
    });
  }

  document.addEventListener("cartUpdated", fetchCartState);

  fetchCartState();
});

const tabLinks = document.querySelectorAll(".tab-link");
const tabContents = document.querySelectorAll(".tab-content");

tabLinks.forEach((link) => {
  link.addEventListener("click", () => {
    const targetId = link.dataset.tab;

    // Remove 'active' class from all tab links and contents
    tabLinks.forEach((btn) => btn.classList.remove("active"));
    tabContents.forEach((tab) => tab.classList.remove("active"));

    // Add 'active' class to clicked tab and corresponding content
    link.classList.add("active");
    document.getElementById(targetId).classList.add("active");
  });
});
