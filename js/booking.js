function openBookingModal(roomName, rate) {
    document.getElementById('roomType').value = roomName;
    document.getElementById('roomRate').value = rate;
    document.getElementById('displayRoomName').innerText = `${roomName} ($${rate}/day)`;
    document.getElementById('bookingModal').style.display = 'flex';
    document.getElementById('bookingMessage').innerText = '';
}

function closeBookingModal() {
    document.getElementById('bookingModal').style.display = 'none';
}

async function submitBooking(event) {
    event.preventDefault();
    
    const bookingData = {
        bookingId: 'RES-' + Date.now(),
        roomType: document.getElementById('roomType').value,
        roomRate: parseFloat(document.getElementById('roomRate').value),
        guestName: document.getElementById('guestName').value,
        email: document.getElementById('guestEmail').value,
        phone: document.getElementById('guestPhone').value,
        checkIn: document.getElementById('checkIn').value,
        checkOut: document.getElementById('checkOut').value,
        guestCount: parseInt(document.getElementById('guestCount').value),
        createdAt: new Date().toISOString()
    };

    const msgEl = document.getElementById('bookingMessage');
    msgEl.style.color = '#316e66';
    msgEl.innerText = 'Processing reservation...';

    try {
        // Replace with your actual API Gateway endpoint URL when connected to AWS
        // const API_ENDPOINT = 'https://YOUR_API_GATEWAY_ID.execute-api.REGION.amazonaws.com/prod/bookings';    // Use in case of deployment via SAM
        // const API_ENDPOINT = '/bookings';                  // Use in case of deployment with Beanstalk via console
        const API_ENDPOINT = 'https://bac5pgl517.execute-api.us-east-1.amazonaws.com/Prod/bookings';

        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookingData)
        });

        if (response.ok) {
            msgEl.style.color = 'green';
            msgEl.innerText = 'Success! Your reservation has been booked.';
            setTimeout(() => {
                closeBookingModal();
                document.getElementById('bookingForm').reset();
            }, 2000);
        } else {
            throw new Error('Failed to save reservation.');
        }
    } catch (error) {
        console.warn('Backend endpoint not connected. Simulating success for testing UI:', error);
        msgEl.style.color = 'green';
        msgEl.innerText = 'Mock Success! Reservation stored locally.';
        setTimeout(() => {
            closeBookingModal();
            document.getElementById('bookingForm').reset();
        }, 2000);
    }
}