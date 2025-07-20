document.addEventListener('DOMContentLoaded', function() {
    // Load currencies dropdown
    fetch('/api/currencies')
        .then(response => response.json())
        .then(data => {
            if (data.currencies) {
                const fromSelect = document.getElementById('from-currency');
                const toSelect = document.getElementById('to-currency');
                const historicalBase = document.getElementById('historical-base');
                
                // Clear existing options (keeping the first one)
                while (fromSelect.options.length > 1) fromSelect.remove(1);
                while (toSelect.options.length > 1) toSelect.remove(1);
                while (historicalBase.options.length > 1) historicalBase.remove(1);
                
                // Add new options
                data.currencies.forEach(currency => {
                    const option1 = new Option(`${currency}`, currency);
                    const option2 = new Option(`${currency}`, currency);
                    const option3 = new Option(`${currency}`, currency);
                    
                    fromSelect.add(option1);
                    toSelect.add(option2);
                    historicalBase.add(option3);
                });
            }
        })
        .catch(error => console.error('Error loading currencies:', error));
    
    // Currency converter form
    const converterForm = document.getElementById('converter-form');
    if (converterForm) {
        converterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const amount = document.getElementById('amount').value;
            const fromCurrency = document.getElementById('from-currency').value;
            const toCurrency = document.getElementById('to-currency').value;
            
            fetch(`/api/convert?from=${fromCurrency}&to=${toCurrency}&amount=${amount}`)
                .then(response => response.json())
                .then(data => {
                    const resultDiv = document.getElementById('conversion-result');
                    const contentDiv = document.getElementById('result-content');
                    
                    if (data.error) {
                        contentDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                    } else {
                        contentDiv.innerHTML = `
                            <p><strong>${data.amount} ${data.from_currency}</strong> equals</p>
                            <h3>${data.converted_amount} ${data.to_currency}</h3>
                            <p>Rate: 1 ${data.from_currency} = ${data.rate} ${data.to_currency}</p>
                            <small class="text-muted">Last updated: ${new Date(data.timestamp).toLocaleString()}</small>
                        `;
                    }
                    
                    resultDiv.classList.remove('d-none');
                })
                .catch(error => {
                    console.error('Conversion error:', error);
                    document.getElementById('result-content').innerHTML = 
                        `<div class="alert alert-danger">Error performing conversion</div>`;
                    document.getElementById('conversion-result').classList.remove('d-none');
                });
        });
    }
    
    // Historical rates form
    const historicalForm = document.getElementById('historical-form');
    if (historicalForm) {
        // Set default date to yesterday
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        document.getElementById('historical-date').valueAsDate = yesterday;
        
        historicalForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const date = document.getElementById('historical-date').value;
            const base = document.getElementById('historical-base').value;
            
            fetch(`/api/historical?date=${date}&base=${base}`)
                .then(response => response.json())
                .then(data => {
                    const resultDiv = document.getElementById('historical-result');
                    const contentDiv = document.getElementById('historical-content');
                    
                    if (data.error) {
                        contentDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                    } else {
                        let ratesHtml = '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>Currency</th><th>Rate</th></tr></thead><tbody>';
                        
                        for (const [currency, rate] of Object.entries(data.conversion_rates)) {
                            ratesHtml += `<tr><td>${currency}</td><td>${rate}</td></tr>`;
                        }
                        
                        ratesHtml += '</tbody></table></div>';
                        
                        contentDiv.innerHTML = `
                            <h4>Rates for ${data.date} (Base: ${data.base})</h4>
                            ${ratesHtml}
                        `;
                    }
                    
                    resultDiv.classList.remove('d-none');
                })
                .catch(error => {
                    console.error('Historical rates error:', error);
                    document.getElementById('historical-content').innerHTML = 
                        `<div class="alert alert-danger">Error fetching historical rates</div>`;
                    document.getElementById('historical-result').classList.remove('d-none');
                });
        });
    }
});