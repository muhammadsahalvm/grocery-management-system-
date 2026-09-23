/**
 * SalamMart - User Base JavaScript
 * Handles sticky header shadow, mobile navigation drawer, account dropdown,
 * toast message dismissal, and back-to-top button.
 */
(function () {
    'use strict';

    // 1. Sticky Header Shadow on Scroll
    const header = document.getElementById('user-main-header');
    const backToTopBtn = document.getElementById('back-to-top');

    function handleScroll() {
        const scrollY = window.scrollY || window.pageYOffset;
        if (header) {
            if (scrollY > 15) {
                header.classList.add('is-scrolled');
            } else {
                header.classList.remove('is-scrolled');
            }
        }

        if (backToTopBtn) {
            if (scrollY > 350) {
                backToTopBtn.classList.add('is-visible');
            } else {
                backToTopBtn.classList.remove('is-visible');
            }
        }
    }

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    // 2. Back to Top Click
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', function () {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // 3. Mobile Drawer Navigation
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navDrawer = document.getElementById('mobile-nav-drawer');
    const overlay = document.getElementById('mobile-overlay');

    function toggleMobileNav(open) {
        if (!navDrawer || !overlay || !menuToggle) return;
        const isOpen = typeof open === 'boolean' ? open : !navDrawer.classList.contains('is-open');

        navDrawer.classList.toggle('is-open', isOpen);
        overlay.classList.toggle('is-open', isOpen);
        navDrawer.hidden = !isOpen;
        overlay.hidden = !isOpen;
        menuToggle.setAttribute('aria-expanded', String(isOpen));
        document.body.style.overflow = isOpen ? 'hidden' : '';
    }

    if (menuToggle) {
        menuToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            toggleMobileNav();
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function () {
            toggleMobileNav(false);
        });
    }

    if (navDrawer) {
        navDrawer.addEventListener('click', function (e) {
            if (e.target.closest('a')) {
                toggleMobileNav(false);
            }
        });
    }

    // 4. Account Profile Dropdown
    const accountTrigger = document.querySelector('.account-trigger-btn');
    const accountMenu = document.getElementById('user-account-menu');

    function toggleAccountMenu(open) {
        if (!accountTrigger || !accountMenu) return;
        const isOpen = typeof open === 'boolean' ? open : accountMenu.hidden;

        accountMenu.hidden = !isOpen;
        accountTrigger.setAttribute('aria-expanded', String(isOpen));
    }

    if (accountTrigger && accountMenu) {
        accountTrigger.addEventListener('click', function (e) {
            e.stopPropagation();
            toggleAccountMenu();
        });

        document.addEventListener('click', function (e) {
            if (!accountTrigger.parentElement.contains(e.target)) {
                toggleAccountMenu(false);
            }
        });
    }

    // 5. Keyboard Navigation (Escape key handling)
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            if (navDrawer && navDrawer.classList.contains('is-open')) {
                toggleMobileNav(false);
            }
            if (accountMenu && !accountMenu.hidden) {
                toggleAccountMenu(false);
            }
        }
    });

    // 6. Toast Message Dismissal & Auto-fade
    document.querySelectorAll('.user-toast-message').forEach(function (toast) {
        const closeBtn = toast.querySelector('.toast-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(20px)';
                toast.style.transition = 'all 0.25s ease';
                setTimeout(function () {
                    toast.remove();
                }, 250);
            });
        }

        // Auto dismiss after 6 seconds
        setTimeout(function () {
            if (toast && toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(20px)';
                toast.style.transition = 'all 0.3s ease';
                setTimeout(function () {
                    if (toast && toast.parentElement) toast.remove();
                }, 300);
            }
        }, 6000);
    });

    // =========================================================================
    // 7. Premium 0 to 100% Page Preloader
    // =========================================================================
    const preloader = document.getElementById('sm-preloader');
    const preloaderCounter = document.getElementById('sm-preloader-counter');
    const preloaderBar = document.getElementById('sm-preloader-bar');
    const preloaderStepText = document.getElementById('sm-preloader-step-text');

    if (preloader) {
        let currentProgress = 0;
        const duration = 1200; // Smooth 1.2s load experience
        const startTime = performance.now();

        const phrases = [
            { limit: 25, text: 'Connecting to farm gardens...' },
            { limit: 60, text: 'Selecting organic harvests...' },
            { limit: 88, text: 'Stocking fresh essentials...' },
            { limit: 100, text: 'Welcome to SalamMart!' }
        ];

        function updatePhrase(val) {
            if (!preloaderStepText) return;
            for (let i = 0; i < phrases.length; i++) {
                if (val <= phrases[i].limit) {
                    if (preloaderStepText.textContent !== phrases[i].text) {
                        preloaderStepText.textContent = phrases[i].text;
                    }
                    break;
                }
            }
        }

        function finishPreloader() {
            if (!preloader.classList.contains('is-loaded')) {
                preloader.classList.add('is-loaded');
                document.body.classList.add('page-ready');
                setTimeout(() => {
                    if (preloader.parentNode) {
                        preloader.style.display = 'none';
                    }
                }, 600);
            }
        }

        function animateLoader(timestamp) {
            const elapsed = timestamp - startTime;
            const progressRatio = Math.min(elapsed / duration, 1);
            
            // Ease out cubic
            const easedProgress = 1 - Math.pow(1 - progressRatio, 3);
            currentProgress = Math.floor(easedProgress * 100);

            if (preloaderCounter) {
                preloaderCounter.textContent = currentProgress + '%';
            }
            if (preloaderBar) {
                preloaderBar.style.width = currentProgress + '%';
            }
            updatePhrase(currentProgress);

            if (progressRatio < 1) {
                requestAnimationFrame(animateLoader);
            } else {
                setTimeout(finishPreloader, 180);
            }
        }

        requestAnimationFrame(animateLoader);

        // Fallback safety timeout (max 2.2s)
        setTimeout(finishPreloader, 2200);
    }

    // =========================================================================
    // 8. Smooth Browsing & Scroll Reveal Animations
    // =========================================================================
    const revealElements = document.querySelectorAll(
        '.category-item-card, .store-product-card, .features-pill-container, .promo-card, .why-choose-card, .section-header'
    );

    if ('IntersectionObserver' in window && revealElements.length > 0) {
        revealElements.forEach(function (el) {
            el.classList.add('reveal-fade-up');
        });

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.08,
            rootMargin: '0px 0px -30px 0px'
        });

        revealElements.forEach(function (el) {
            const parent = el.parentElement;
            if (parent && (parent.classList.contains('category-cards-grid') || parent.classList.contains('store-product-grid'))) {
                const childIndex = Array.from(parent.children).indexOf(el);
                el.style.transitionDelay = `${(childIndex % 6) * 45}ms`;
            }
            observer.observe(el);
        });
    }

    // =========================================================================
    // 9. Interactive Component Click Feedback (Ripple & Micro-bounce)
    // =========================================================================
    document.addEventListener('click', function (e) {
        const clickable = e.target.closest(
            '.btn-add-cart, .btn-hero-primary, .btn-hero-secondary, .category-item-card, .action-btn, .search-submit-btn, .footer-links-list a, .view-all-link, .app-badge-btn, .clear-filters-btn'
        );
        if (!clickable) return;

        // Tactile micro-bounce
        clickable.classList.add('btn-click-active');
        setTimeout(function () {
            clickable.classList.remove('btn-click-active');
        }, 180);

        // Subtle Ripple Effect
        const rect = clickable.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        const ripple = document.createElement('span');
        ripple.className = 'sm-ripple-circle';
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        clickable.classList.add('has-ripple');
        clickable.appendChild(ripple);

        setTimeout(function () {
            if (ripple.parentNode) ripple.remove();
        }, 600);

        // Header cart bounce if add-to-cart clicked
        if (clickable.classList.contains('btn-add-cart') || clickable.closest('.btn-add-cart')) {
            const cartBadge = document.querySelector('.cart-count-badge');
            if (cartBadge) {
                cartBadge.classList.remove('cart-badge-bounce');
                void cartBadge.offsetWidth;
                cartBadge.classList.add('cart-badge-bounce');
                setTimeout(function () {
                    cartBadge.classList.remove('cart-badge-bounce');
                }, 500);
            }
        }
    });

})();