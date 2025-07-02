document.addEventListener("DOMContentLoaded", () => {
    // --- "View All Products" Button Logic ---
    const viewAllBtn = document.getElementById("view-all-btn");
    const otherProductsSection = document.getElementById("other-products-section");
    const viewAllContainer = document.getElementById("view-all-container");

    if (viewAllBtn && otherProductsSection) {
        viewAllBtn.addEventListener("click", () => {
            otherProductsSection.classList.remove("hidden");
            if (viewAllContainer) {
                viewAllContainer.style.display = "none";
            }
        });
    }

    // --- Filtering and Sorting Logic ---
    const categoryFilter = document.getElementById("category-filter");
    const sortFilter = document.getElementById("sort-filter");

    const applyFiltersAndSort = () => {
        const selectedCategory = categoryFilter.value;
        const selectedSort = sortFilter.value;

        // Apply category filter first
        document.querySelectorAll(".product-card").forEach(card => {
            const cardCategory = card.dataset.category;
            const categoryMatch = (selectedCategory === 'all' || cardCategory === selectedCategory);
            card.style.display = categoryMatch ? 'flex' : 'none';
        });

        // Apply sorting to each grid separately
        document.querySelectorAll('.card-grid').forEach(grid => {
            const cards = Array.from(grid.querySelectorAll('.product-card'))
                .filter(card => card.style.display !== 'none'); // Only sort visible cards

            cards.sort((a, b) => {
                const priceA = parseFloat(a.dataset.price);
                const priceB = parseFloat(b.dataset.price);
                const ratingA = parseFloat(a.dataset.rating);
                const ratingB = parseFloat(b.dataset.rating);

                switch (selectedSort) {
                    case 'price_asc':  return priceA - priceB;
                    case 'price_desc': return priceB - priceA;
                    case 'rating':     return ratingB - ratingA;
                    default:           return 0;
                }
            });

            // Re-append sorted cards to their grid
            cards.forEach(card => grid.appendChild(card));
        });
    };

    if (categoryFilter && sortFilter) {
        categoryFilter.addEventListener('change', applyFiltersAndSort);
        sortFilter.addEventListener('change', applyFiltersAndSort);
    }
});