// Toggle Check/Ex for complete/incomplete habits in table
document.addEventListener('DOMContentLoaded', function() {
    const btns = document.querySelectorAll('.habit-btn');
    
    btns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault(); // prevents form from doing a normal submission

            const form = this.closest('form');
            
            // Send data to server
            fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            });

            // Toggle symbol
            this.textContent = this.textContent === '✗' ? '✓' : '✗';

        })
    })
})