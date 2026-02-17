// WhatsApp Chat Widget JavaScript
function toggleWhatsAppChat() {
    const chatBox = document.getElementById('whatsapp-chat-box');
    chatBox.classList.toggle('active');
}

function sendWhatsAppMessage(message) {
    const phoneNumber = '919505764142'; // CodeServe WhatsApp number with country code
    const encodedMessage = encodeURIComponent(message);
    const whatsappURL = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
    window.open(whatsappURL, '_blank');
}

// Initialize WhatsApp Widget
document.addEventListener('DOMContentLoaded', function() {
    // Close chat when clicking outside
    document.addEventListener('click', function(event) {
        const chatWidget = document.getElementById('whatsapp-chat');
        const chatBox = document.getElementById('whatsapp-chat-box');
        
        if (chatWidget && !chatWidget.contains(event.target) && chatBox && chatBox.classList.contains('active')) {
            chatBox.classList.remove('active');
        }
    });

    // Auto-show chat after 15 seconds (optional)
    setTimeout(function() {
        const chatButton = document.querySelector('.whatsapp-chat-button');
        if (chatButton) {
            chatButton.style.animation = 'pulse 1s infinite';
            
            // Show tooltip briefly
            const tooltip = chatButton.querySelector('.chat-tooltip');
            if (tooltip) {
                tooltip.style.opacity = '1';
                tooltip.style.visibility = 'visible';
                
                setTimeout(function() {
                    tooltip.style.opacity = '0';
                    tooltip.style.visibility = 'hidden';
                }, 3000);
            }
        }
    }, 15000);

    // Track WhatsApp interactions (optional analytics)
    const whatsappButtons = document.querySelectorAll('[onclick*="sendWhatsAppMessage"]');
    whatsappButtons.forEach(button => {
        button.addEventListener('click', function() {
            // You can add analytics tracking here
            console.log('WhatsApp message initiated:', this.textContent);
        });
    });
});

// Additional utility functions
function showWhatsAppNotification(message) {
    // Create a temporary notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #25d366;
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        z-index: 10000;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 5px 15px rgba(37, 211, 102, 0.4);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Custom message functions for different pages
function sendServiceInquiry(service) {
    const message = `Hello! I'm interested in your ${service} services. Can you provide more information?`;
    sendWhatsAppMessage(message);
}

function sendPortfolioInquiry(project) {
    const message = `Hi! I saw your ${project} project and I'm interested in something similar. Can we discuss?`;
    sendWhatsAppMessage(message);
}

function sendQuoteRequest() {
    const message = `Hello CodeServe! I would like to get a quote for my project. Can we schedule a discussion?`;
    sendWhatsAppMessage(message);
}

// Keyboard shortcuts (optional)
document.addEventListener('keydown', function(event) {
    // Press 'W' to toggle WhatsApp chat
    if (event.key === 'w' || event.key === 'W') {
        if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            toggleWhatsAppChat();
        }
    }
});
