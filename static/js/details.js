// static/js/details.js
document.addEventListener('DOMContentLoaded', () => {
    loadDeliveryDetails();
});

async function loadDeliveryDetails() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('detailsContainer').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    try {
        // Use provided global ticketId or try common fallbacks (data attribute or query param)
        const id = (typeof ticketId !== 'undefined' && ticketId) ||
                   document.getElementById('detailsContainer')?.dataset?.ticketId ||
                   new URLSearchParams(window.location.search).get('ticket_id');

        if (!id) {
            throw new Error('Ticket ID not provided');
        }

        const response = await fetch(`/api/delivery/${encodeURIComponent(id)}`);
        
        if (!response.ok) {
            throw new Error('Delivery not found');
        }
        
        const data = await response.json();
        displayDetails(data);
        
    } catch (error) {
        document.getElementById('errorMessage').textContent = error.message;
        document.getElementById('error').classList.remove('hidden');
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

function displayDetails(delivery) {
    // Ticket Information
    document.getElementById('ticketId').textContent = delivery?.ticket_id ?? 'N/A';
    document.getElementById('userId').textContent = delivery?.user_id ?? 'N/A';
    document.getElementById('createdAt').textContent = delivery?.created_at ? formatDate(delivery.created_at) : 'N/A';
    
    // Delivery Specifications
    document.getElementById('materialType').textContent = delivery?.material_type ? capitalizeFirst(delivery.material_type) : 'N/A';
    document.getElementById('distance').textContent = (delivery?.distance != null) ? `${delivery.distance} km` : 'N/A';
    document.getElementById('urgency').textContent = delivery?.urgency ? capitalizeFirst(delivery.urgency.replace('_', ' ')) : 'N/A';
    document.getElementById('weight').textContent = (delivery?.weight != null) ? `${delivery.weight} kg` : 'N/A';
    document.getElementById('locationType').textContent = delivery?.location_type ? capitalizeFirst(delivery.location_type) : 'N/A';
    // Price Information
    document.getElementById('totalPrice').textContent = (typeof delivery?.total_price === 'number') ? `₹${delivery.total_price.toFixed(2)}` : 'N/A';

    // Status Badge
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.textContent = delivery?.status ?? 'unknown';
    statusBadge.className = `status-badge ${String(delivery?.status ?? '').replace(/\s+/g, '-').toLowerCase()}`;

    // Action Log
    const logContainer = document.getElementById('actionLog');
    logContainer.innerHTML = '';

    if (delivery?.action_log && delivery.action_log.length > 0) {
        delivery.action_log.forEach(log => {
            const logItem = document.createElement('div');
            logItem.style.padding = '8px 0';
            logItem.style.borderBottom = '1px solid var(--border-color)';
            logItem.textContent = log;
            logContainer.appendChild(logItem);
        });
    } else {
        logContainer.innerHTML = '<p style="color: var(--text-light);">No processing logs available</p>';
    }

    // Show details container
    document.getElementById('detailsContainer').classList.remove('hidden');
}

function downloadPDF() {
alert('PDF download feature coming soon!');
// In production, you would implement PDF generation here
}

function capitalizeFirst(str) {
    if (!str || typeof str !== 'string') return str ?? '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    if (Number.isNaN(date.getTime())) return 'Invalid date';
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

