// StockTrack Pro - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    console.log('StockTrack Pro loaded successfully!');
    
    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.flash');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                message.style.transition = 'opacity 0.5s ease';
                setTimeout(() => message.remove(), 500);
            }, 5000);
        });
    }
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#e74c3c';
                    
                    setTimeout(() => {
                        field.style.borderColor = '';
                    }, 2000);
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
    
    // Movement form validation
    const movementForm = document.querySelector('.movement-form');
    if (movementForm) {
        movementForm.addEventListener('submit', function(e) {
            const fromLocation = this.querySelector('[name="from_location"]');
            const toLocation = this.querySelector('[name="to_location"]');
            
            if (!fromLocation.value && !toLocation.value) {
                e.preventDefault();
                alert('Please specify either From Location or To Location.');
                return false;
            }
            
            if (fromLocation.value && toLocation.value && fromLocation.value === toLocation.value) {
                e.preventDefault();
                alert('From and To locations cannot be the same.');
                return false;
            }
        });
    }
    
    // Table row highlighting
    const tableRows = document.querySelectorAll('.table tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    // Print functionality for reports
    window.printReport = function() {
        window.print();
    };
    
    // Responsive navigation for mobile
    const setupMobileNav = function() {
        if (window.innerWidth < 768) {
            const nav = document.querySelector('.main-nav');
            if (nav) {
                const navToggle = document.createElement('button');
                navToggle.innerHTML = '☰ Menu';
                navToggle.style.cssText = `
                    background: #3498db;
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    margin: 1rem 0;
                    cursor: pointer;
                `;
                
                nav.parentNode.insertBefore(navToggle, nav);
                nav.style.display = 'none';
                
                navToggle.addEventListener('click', function() {
                    if (nav.style.display === 'none') {
                        nav.style.display = 'block';
                        this.innerHTML = '✕ Close';
                    } else {
                        nav.style.display = 'none';
                        this.innerHTML = '☰ Menu';
                    }
                });
            }
        }
    };
    
    setupMobileNav();
    window.addEventListener('resize', setupMobileNav);
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});