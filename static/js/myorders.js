document.addEventListener('DOMContentLoaded', () => {
    const ordersTableBody = document.querySelector('table tbody');
    const contentPanel = document.querySelector('.content-panel');
    const statusFilter = document.getElementById('status-filter');
    let allOrders = [];

    const renderOrders = (orders) => {
        ordersTableBody.innerHTML = '';

        if (orders.length === 0) {
            const emptyRow = `
                <tr>
                    <td colspan="6" class="empty-state-cell">
                        You have no orders matching this filter.
                    </td>
                </tr>
            `;
            ordersTableBody.innerHTML = emptyRow;
            return;
        }

        orders.forEach(order => {
            const statusClass = `status-${order.status.toLowerCase().replace(/\s+/g, '-')}`;
            const row = `
                <tr>
                    <td data-label="Order ID">${order.order_id}</td>
                    <td data-label="Date">${order.order_date}</td>
                    <td data-label="Items">${order.item_count}</td>
                    <td data-label="Total">₹${order.total_amount.toFixed(2)}</td>
                    <td data-label="Status"><span class="status-badge ${statusClass}">${order.status}</span></td>
                    <td data-label="Actions">
                        <div class="action-dropdown">
                            <button class="dots-btn" aria-label="Order Actions" data-order-id="${order._id}">
                                <i class="fas fa-ellipsis-v"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
            ordersTableBody.insertAdjacentHTML('beforeend', row);
        });
    };

    const filterAndRenderOrders = () => {
        const selectedStatus = statusFilter.value;

        if (selectedStatus === 'all') {
            renderOrders(allOrders);
        } else {
            const filteredOrders = allOrders.filter(order =>
                order.status.toLowerCase().replace(/\s+/g, '-') === selectedStatus
            );
            renderOrders(filteredOrders);
        }
    };

    const fetchOrders = async () => {
        try {
            ordersTableBody.innerHTML = `<tr><td colspan="6" class="loading-cell">Loading your orders...</td></tr>`;

            const response = await fetch('http://127.0.0.1:5000/orders/get');
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Could not fetch your orders.');
            }

            const data = await response.json();
            allOrders = data.orders;

            if (allOrders.length === 0) {
                contentPanel.innerHTML = `
                    <div class="empty-state">
                        <h2>You Have No Order History</h2>
                        <p>Once you place an order, it will appear here.</p>
                        <a href="/products" class="btn btn-primary">Start Shopping</a>
                    </div>
                `;
            } else {
                filterAndRenderOrders();
            }

        } catch (error) {
            console.error('Error fetching orders:', error);
            contentPanel.innerHTML = `<div class="error-state"><h2>Error</h2><p>${error.message}</p></div>`;
        }
    };

    statusFilter.addEventListener('change', filterAndRenderOrders);
    fetchOrders();
});
