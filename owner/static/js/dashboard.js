document.addEventListener('DOMContentLoaded', function() {
    // 1. Current Date display
    const dateElement = document.getElementById('currentDate');
    if (dateElement) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const today = new Date().toLocaleDateString('en-US', options);
        dateElement.textContent = today;
    }

    // 2. Notification Bell Dropdown
    const notificationBtn = document.getElementById('headerNotificationBtn');
    const notificationBadge = document.getElementById('notificationBadge');
    const clearBtn = document.getElementById('clearNotificationsBtn');
    const dropdownBody = document.getElementById('notificationDropdownBody');
    const dropdownFooter = document.getElementById('notificationDropdownFooter');
    const countTag = document.getElementById('notificationCountTag');

    const profileBtn = document.getElementById('headerProfileBtn');

    if (notificationBtn) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (profileBtn) {
                profileBtn.classList.remove('open');
                profileBtn.setAttribute('aria-expanded', 'false');
            }
            const isOpen = notificationBtn.classList.toggle('open');
            notificationBtn.setAttribute('aria-expanded', isOpen);
        });

        // Close when clicking anywhere else
        document.addEventListener('click', function(e) {
            if (!notificationBtn.contains(e.target)) {
                notificationBtn.classList.remove('open');
                notificationBtn.setAttribute('aria-expanded', 'false');
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && notificationBtn.classList.contains('open')) {
                notificationBtn.classList.remove('open');
                notificationBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // 2b. Store Owner Profile Dropdown
    if (profileBtn) {
        profileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (notificationBtn) {
                notificationBtn.classList.remove('open');
                notificationBtn.setAttribute('aria-expanded', 'false');
            }
            const isOpen = profileBtn.classList.toggle('open');
            profileBtn.setAttribute('aria-expanded', isOpen);
        });

        // Close when clicking anywhere else
        document.addEventListener('click', function(e) {
            if (!profileBtn.contains(e.target)) {
                profileBtn.classList.remove('open');
                profileBtn.setAttribute('aria-expanded', 'false');
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && profileBtn.classList.contains('open')) {
                profileBtn.classList.remove('open');
                profileBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // 3. Mark all as read button
    if (clearBtn) {
        clearBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (notificationBadge) {
                notificationBadge.style.display = 'none';
            }
            if (countTag) {
                countTag.remove();
            }
            if (dropdownBody) {
                dropdownBody.innerHTML = `
                    <div class="notification-empty">
                        <i class="bi bi-check-circle" style="color: var(--color-primary);"></i>
                        <p>All caught up!</p>
                        <span>No unread notifications</span>
                    </div>
                `;
            }
            if (dropdownFooter) {
                dropdownFooter.remove();
            }
        });
    }

    // 4. Floating Toast auto-dismiss after 4.5 seconds
    const toasts = document.querySelectorAll('.toast-item');
    toasts.forEach(function(toast) {
        setTimeout(function() {
            toast.style.transition = 'all 0.4s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                toast.remove();
            }, 400);
        }, 4500);
    });
});
