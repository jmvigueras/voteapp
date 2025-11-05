// Simple voting app JavaScript
console.log('App loaded');

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ready');
    updateResults();
    setInterval(updateResults, 5000);
});

// Cast a vote
function castVote(vote) {
    console.log('Voting:', vote);
    
    const yesBtn = document.getElementById('vote-yes');
    const noBtn = document.getElementById('vote-no');
    
    yesBtn.disabled = true;
    noBtn.disabled = true;
    
    fetch('/api/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vote: vote })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Vote response:', data);
        showMessage('Thank you for voting!', 'success');
        updateResults();
        setTimeout(() => {
            yesBtn.disabled = false;
            noBtn.disabled = false;
        }, 2000);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error voting. Please try again.', 'danger');
        yesBtn.disabled = false;
        noBtn.disabled = false;
    });
}

// Show message
function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = 'alert alert-' + type;
    msg.style.display = 'block';
    
    setTimeout(() => {
        msg.style.display = 'none';
    }, 3000);
}

// Update results
function updateResults() {
    fetch('/api/results')
    .then(response => response.json())
    .then(data => {
        console.log('Results:', data);
        
        // Update counts
        document.getElementById('yes-count').textContent = data.yes || 0;
        document.getElementById('no-count').textContent = data.no || 0;
        
        // Calculate percentages
        const total = data.total || 0;
        const yesPercent = total > 0 ? Math.round((data.yes / total) * 100) : 0;
        const noPercent = total > 0 ? Math.round((data.no / total) * 100) : 0;
        
        // Update percentages
        document.getElementById('yes-percentage').textContent = yesPercent;
        document.getElementById('no-percentage').textContent = noPercent;
        
        // Update progress bars
        const yesBar = document.getElementById('yes-progress');
        const noBar = document.getElementById('no-progress');
        
        yesBar.style.width = yesPercent + '%';
        yesBar.setAttribute('aria-valuenow', yesPercent);
        
        noBar.style.width = noPercent + '%';
        noBar.setAttribute('aria-valuenow', noPercent);
    })
    .catch(error => {
        console.error('Error fetching results:', error);
    });
}

