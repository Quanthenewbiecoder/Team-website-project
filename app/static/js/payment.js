// Format card number input with spaces
document.getElementById('card-number').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    let formattedValue = '';
    
    for(let i = 0; i < value.length; i++) {
        if(i > 0 && i % 4 === 0) {
            formattedValue += ' ';
        }
        formattedValue += value[i];
    }
    
    e.target.value = formattedValue;
});

// Format expiry date input
document.getElementById('expiry').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    if (value.length >= 2) {
        value = value.slice(0,2) + '/' + value.slice(2);
    }
    
    e.target.value = value;
});

// Validate CVV to only allow numbers
document.getElementById('cvv').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/\D/g, '');
});

// Form submission handling
document.querySelector('.payment-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Basic validation
    const cardNumber = document.getElementById('card-number').value.replace(/\s/g, '');
    const expiry = document.getElementById('expiry').value;
    const cvv = document.getElementById('cvv').value;
    
    if (cardNumber.length !== 16) {
        alert('Please enter a valid card number');
        return;
    }
    
    if (!expiry.match(/^(0[1-9]|1[0-2])\/([0-9]{2})$/)) {
        alert('Please enter a valid expiry date (MM/YY)');
        return;
    }
    
    if (cvv.length !== 3) {
        alert('Please enter a valid CVV');
        return;
    }
    
    // If validation passes, submit the form
    this.submit();
});