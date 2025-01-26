function checkAvailability() {
  const date = document.getElementById('date').value;
  const time = document.getElementById('time').value;
  const vehicleType = document.getElementById('vehicleType').value;

  fetch('http://127.0.0.1:5000/api/check-availability', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ date, time, vehicleType }),
  })
    .then(response => response.json())
    .then(data => {
      const slotsDiv = document.getElementById('slots');
      slotsDiv.innerHTML = '<h3>Available Slots:</h3>';
      data.slots.forEach(slot => {
        slotsDiv.innerHTML += `<p>${slot}</p>`;
      });
      document.getElementById('bookingForm').style.display = 'block';
    });
}

function bookSlot() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const slotId = document.getElementById('slots').querySelector('p').innerText; // Get the first available slot

  fetch('http://127.0.0.1:5000/api/book-slot', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, email, slotId, date: document.getElementById('date').value, time: document.getElementById('time').value }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById('bookingForm').style.display = 'none';
        document.getElementById('paymentForm').style.display = 'block';
      }
    });
}

function processPayment() {
  const cardNumber = document.getElementById('cardNumber').value;
  const expiry = document.getElementById('expiry').value;
  const cvv = document.getElementById('cvv').value;

  fetch('http://127.0.0.1:5000/api/process-payment', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ cardNumber, expiry, cvv }),
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById('paymentForm').style.display = 'none';
      document.getElementById('confirmation').style.display = 'block';
    });
}