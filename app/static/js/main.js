/**
 * Main JavaScript for the Car Price Prediction application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Poll for crawl status updates if there's an active crawl
    const statusBadges = document.querySelectorAll('.badge');
    statusBadges.forEach(badge => {
        if (badge.textContent === 'running') {
            badge.classList.add('updating');
            
            // Find the closest row to get the log ID
            const row = badge.closest('tr');
            if (row) {
                const logId = row.querySelector('td:first-child').textContent;
                const isProcessingLog = row.querySelector('td:nth-child(2)').textContent.includes('/');
                
                // Set up polling for status updates
                const endpoint = isProcessingLog 
                    ? `/api/processing-status/${logId}`
                    : `/api/crawl-status/${logId}`;
                
                pollStatus(endpoint, badge, row);
            }
        }
    });
    
    // Also check if the latest crawl or processing is running from the cards
    const cardBadges = document.querySelectorAll('.card .badge');
    cardBadges.forEach(badge => {
        if (badge.textContent === 'running') {
            badge.classList.add('updating');
            // Refresh the page every 30 seconds if something is running
            setTimeout(() => {
                window.location.reload();
            }, 30000);
        }
    });
    
    // Set up form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

/**
 * Poll an API endpoint for status updates
 * @param {string} endpoint - The API endpoint to poll
 * @param {Element} badge - The badge element to update
 * @param {Element} row - The table row to update
 */
function pollStatus(endpoint, badge, row) {
    const interval = setInterval(() => {
        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'running') {
                    clearInterval(interval);
                    badge.classList.remove('updating');
                    
                    // Update badge class and text
                    badge.classList.remove('bg-warning');
                    badge.classList.add(data.status === 'completed' ? 'bg-success' : 'bg-danger');
                    badge.textContent = data.status;
                    
                    // Update other cells in the row
                    if (row) {
                        // Update records count
                        const recordsCell = row.querySelector('td:nth-child(6)');
                        if (recordsCell) {
                            recordsCell.textContent = data.records_count;
                        }
                        
                        // Update end time
                        const endTimeCell = row.querySelector('td:nth-child(4)');
                        if (endTimeCell && data.end_time) {
                            endTimeCell.textContent = data.end_time;
                        }
                        
                        // If it's a processing log, update output file if available
                        if (endpoint.includes('processing-status') && data.output_file) {
                            const outputFileCell = row.querySelector('td:nth-child(3)');
                            if (outputFileCell) {
                                outputFileCell.textContent = data.output_file;
                            }
                        }
                    }
                    
                    // Refresh the page after a short delay
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                }
            })
            .catch(error => {
                console.error('Error polling status:', error);
            });
    }, 5000); // Poll every 5 seconds
}