// static/js/main.js
let currentTicketId = null;

document.getElementById('deliveryForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = {
        user_id: document.getElementById('user_id').value,
        user_email: document.getElementById('user_email').value || null,
        material_type: document.getElementById('material_type').value,
        distance: parseFloat(document.getElementById('distance').value),
        urgency: document.getElementById('urgency').value,
        weight: parseFloat(document.getElementById('weight').value),
        location_type: document.getElementById('location_type').value
    };
    
    // Show loading, hide results and errors
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('submitBtn').disabled = true;
    
    try {
        const response = await fetch('/api/calculate-price', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail?.message || data.detail || 'Calculation failed');
        }
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('submitBtn').disabled = false;
    }
});

function displayResults(data) {
    currentTicketId = data.ticket_id;
    
    // Update result values
    document.getElementById('ticketId').textContent = data.ticket_id;
    document.getElementById('totalPrice').textContent = `₹${data.total_price.toFixed(2)}`;
    document.getElementById('basePrice').textContent = `₹${data.breakdown.base_price.toFixed(2)}`;
    document.getElementById('urgencyMult').textContent = `${data.breakdown.urgency_multiplier}x`;
    document.getElementById('weightSurcharge').textContent = `₹${data.breakdown.weight_surcharge.toFixed(2)}`;
    document.getElementById('locationAdj').textContent = `₹${data.breakdown.location_adjustment.toFixed(2)}`;
    
    // Update action log
    const actionLog = document.getElementById('actionLog');
    actionLog.innerHTML = '';
    data.action_log.forEach(log => {
        const li = document.createElement('li');
        li.textContent = log;
        actionLog.appendChild(li);
    });
    
    // Show results
    document.getElementById('results').classList.remove('hidden');
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').classList.remove('hidden');
    document.getElementById('error').scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function resetForm() {
    document.getElementById('deliveryForm').reset();
    document.getElementById('results').classList.add('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function viewDetails() {
    if (currentTicketId) {
        window.location.href = `/delivery/${currentTicketId}`;
    }
}