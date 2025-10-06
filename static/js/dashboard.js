// static/js/dashboard.js
let deliveriesData = [];

// Load deliveries on page load
document.addEventListener('DOMContentLoaded', () => {
    loadDeliveries();
});

async function loadDeliveries() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('deliveriesTable').classList.add('hidden');
    document.getElementById('noData').classList.add('hidden');
    
    try {
        const response = await fetch('/api/deliveries?limit=100');
        const data = await response.json();
        
        deliveriesData = data;
        
        if (data.length === 0) {
            document.getElementById('noData').classList.remove('hidden');
        } else {
            displayDeliveries(data);
            updateStats(data);
            document.getElementById('deliveriesTable').classList.remove('hidden');
        }
        
    } catch (error) {
        console.error('Error loading deliveries:', error);
        document.getElementById('noData').classList.remove('hidden');
        document.querySelector('#noData p').textContent = '❌ Error loading deliveries';
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

function displayDeliveries(deliveries) {
    const tbody = document.getElementById('deliveriesBody');
    tbody.innerHTML = '';
    
    deliveries.forEach(delivery => {
        const row = document.createElement('tr');
        
        const statusClass = delivery.status === 'completed' ? 'completed' : 
                           delivery.status === 'failed' ? 'failed' : 'pending';
        
        row.innerHTML = `
            <td><strong>${delivery.ticket_id}</strong></td>
            <td>${delivery.user_id}</td>
            <td>${capitalizeFirst(delivery.material_type)}</td>
            <td>${delivery.distance} km</td>
            <td>₹${delivery.total_price ? delivery.total_price.toFixed(2) : 'N/A'}</td>
            <td><span class="status-badge ${statusClass}">${delivery.status}</span></td>
            <td>${formatDate(delivery.created_at)}</td>
            <td>
                <a href="/delivery/${delivery.ticket_id}" class="btn-secondary" style="padding: 8px 16px; font-size: 14px;">
                    View
                </a>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

function updateStats(deliveries) {
    const total = deliveries.length;
    const completed = deliveries.filter(d => d.status === 'completed').length;
    const totalRevenue = deliveries
        .filter(d => d.total_price)
        .reduce((sum, d) => sum + d.total_price, 0);
    const avgPrice = total > 0 ? totalRevenue / completed : 0;
    
    document.getElementById('totalDeliveries').textContent = total;
    document.getElementById('completedDeliveries').textContent = completed;
    document.getElementById('totalRevenue').textContent = `₹${totalRevenue.toFixed(2)}`;
    document.getElementById('avgPrice').textContent = `₹${avgPrice.toFixed(2)}`;
}

function refreshDeliveries() {
    loadDeliveries();
}

function filterTable() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filtered = deliveriesData.filter(d => 
        d.ticket_id.toLowerCase().includes(searchTerm) ||
        d.user_id.toLowerCase().includes(searchTerm)
    );
    displayDeliveries(filtered);
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}