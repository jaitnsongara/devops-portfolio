// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Mobile menu toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Navbar background on scroll with shadow
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(30px)';
    section.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(section);
});

// Add active class to navigation based on scroll position
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Scroll to Top Button
const createScrollToTopButton = () => {
    const button = document.createElement('button');
    button.className = 'scroll-to-top';
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.setAttribute('aria-label', 'Scroll to top');
    document.body.appendChild(button);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            button.classList.add('visible');
        } else {
            button.classList.remove('visible');
        }
    });
    
    // Scroll to top on click
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
};

// Initialize scroll to top button
createScrollToTopButton();

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    const navbar = document.querySelector('.navbar');
    const isClickInsideNav = navbar.contains(e.target);
    
    if (!isClickInsideNav && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});

// Prevent body scroll when mobile menu is open
if (hamburger) {
    hamburger.addEventListener('click', () => {
        if (navMenu.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });
}

// Close menu and restore scroll when link is clicked
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        document.body.style.overflow = '';
    });
});

// Lazy loading for images (if any are added)
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Add touch feedback for mobile
if ('ontouchstart' in window) {
    document.querySelectorAll('.btn, .project-card, .case-study-card, .blog-card').forEach(element => {
        element.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        element.addEventListener('touchend', function() {
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });
}

// Animate stats on scroll into view
const animateStats = () => {
    const stats = document.querySelectorAll('.stat-number, .metric-value');
    
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = target.textContent;
                
                // Only animate if it's a number
                if (!isNaN(parseFloat(finalValue))) {
                    const duration = 1000;
                    const start = 0;
                    const end = parseFloat(finalValue);
                    const startTime = performance.now();
                    
                    const animate = (currentTime) => {
                        const elapsed = currentTime - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        
                        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
                        const current = start + (end - start) * easeOutQuart;
                        
                        target.textContent = Math.floor(current) + finalValue.replace(/[0-9]/g, '');
                        
                        if (progress < 1) {
                            requestAnimationFrame(animate);
                        } else {
                            target.textContent = finalValue;
                        }
                    };
                    
                    requestAnimationFrame(animate);
                }
                
                statsObserver.unobserve(target);
            }
        });
    }, { threshold: 0.5 });
    
    stats.forEach(stat => statsObserver.observe(stat));
};

// Initialize stat animations
animateStats();

// Performance: Debounce scroll events
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Apply debounce to scroll-heavy operations
const debouncedScroll = debounce(() => {
    // Any expensive scroll operations can go here
}, 100);

window.addEventListener('scroll', debouncedScroll);

// Add loading state
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Console message for developers
console.log('%c👋 Hi there, Developer!', 'font-size: 20px; color: #64ffda; font-weight: bold;');
console.log('%cInterested in the code? Check out the repo:', 'font-size: 14px; color: #8892b0;');
console.log('%chttps://github.com/jaitnsongara/devops-portfolio', 'font-size: 14px; color: #64ffda;');

// Contact Information Obfuscation (Scrape-proof)
function revealEmail(element) {
    const p = element.querySelector('.obfuscated');
    const user = p.dataset.user;
    const domain = p.dataset.domain;
    const email = user + '@' + domain;
    
    p.textContent = email;
    element.classList.add('revealed');
    
    // Make it clickable
    element.onclick = null;
    element.style.cursor = 'default';
    
    // Copy to clipboard
    navigator.clipboard.writeText(email).then(() => {
        const originalText = p.textContent;
        p.textContent = '✓ Copied to clipboard!';
        setTimeout(() => {
            p.textContent = originalText;
        }, 2000);
    });
}

function revealPhone(element) {
    const p = element.querySelector('.obfuscated');
    const phone = p.dataset.phone;
    
    p.textContent = phone;
    element.classList.add('revealed');
    
    // Make it clickable
    element.onclick = () => {
        window.location.href = 'tel:' + phone;
    };
    element.style.cursor = 'pointer';
    
    // Copy to clipboard
    navigator.clipboard.writeText(phone).then(() => {
        const originalText = p.textContent;
        p.textContent = '✓ Copied to clipboard!';
        setTimeout(() => {
            p.textContent = originalText;
        }, 2000);
    });
}

// Add DevOps Floating Icons to Hero Section
const addDevOpsIcons = () => {
    const hero = document.querySelector('.hero');
    if (!hero || window.innerWidth < 768) return;
    
    const iconsContainer = document.createElement('div');
    iconsContainer.className = 'devops-icons';
    
    const icons = [
        'fab fa-docker',
        'fab fa-aws',
        'fab fa-jenkins',
        'fab fa-git-alt',
        'fas fa-server',
        'fab fa-python'
    ];
    
    icons.forEach(iconClass => {
        const icon = document.createElement('i');
        icon.className = `devops-icon ${iconClass}`;
        iconsContainer.appendChild(icon);
    });
    
    hero.appendChild(iconsContainer);
};

// Add Code Rain Effect
const addCodeRain = () => {
    const hero = document.querySelector('.hero');
    if (!hero || window.innerWidth < 768) return;
    
    const codeRain = document.createElement('div');
    codeRain.className = 'code-rain';
    
    const codeSnippets = [
        'kubectl', 'docker', 'terraform', 'ansible', 'jenkins',
        'aws', 'ci/cd', 'devops', 'k8s', 'helm', 'git',
        'python', 'bash', 'nginx', 'prometheus', 'grafana'
    ];
    
    for (let i = 0; i < 15; i++) {
        const span = document.createElement('span');
        span.textContent = codeSnippets[Math.floor(Math.random() * codeSnippets.length)];
        span.style.left = Math.random() * 100 + '%';
        span.style.animationDuration = (Math.random() * 10 + 10) + 's';
        span.style.animationDelay = Math.random() * 5 + 's';
        span.style.fontSize = (Math.random() * 8 + 10) + 'px';
        codeRain.appendChild(span);
    }
    
    hero.appendChild(codeRain);
};

// Initialize DevOps animations
if (window.innerWidth >= 768) {
    addDevOpsIcons();
    addCodeRain();
}

// Hire Me Button Click Tracking
document.querySelectorAll('.hire-me-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        console.log('Hire Me button clicked');
        
        // Add a visual feedback
        const ripple = document.createElement('span');
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.6)';
        ripple.style.width = '20px';
        ripple.style.height = '20px';
        ripple.style.animation = 'ripple 0.6s ease-out';
        
        const rect = btn.getBoundingClientRect();
        ripple.style.left = (e.clientX - rect.left - 10) + 'px';
        ripple.style.top = (e.clientY - rect.top - 10) + 'px';
        
        btn.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Enhanced Mobile Menu with Better Animation
if (hamburger && navMenu) {
    hamburger.addEventListener('click', (e) => {
        e.stopPropagation();
        const isActive = navMenu.classList.contains('active');
        
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
        
        // Prevent body scroll when menu is open
        if (!isActive) {
            document.body.style.overflow = 'hidden';
            document.body.style.position = 'fixed';
            document.body.style.width = '100%';
        } else {
            document.body.style.overflow = '';
            document.body.style.position = '';
            document.body.style.width = '';
        }
    });
    
    // Close menu when clicking a link
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
            document.body.style.overflow = '';
            document.body.style.position = '';
            document.body.style.width = '';
        });
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (navMenu.classList.contains('active') && 
            !navMenu.contains(e.target) && 
            !hamburger.contains(e.target)) {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
            document.body.style.overflow = '';
            document.body.style.position = '';
            document.body.style.width = '';
        }
    });
}

// Add ripple animation CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            width: 200px;
            height: 200px;
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Timeline Animation on Scroll
const timelineObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateX(0)';
        }
    });
}, { threshold: 0.2 });

document.querySelectorAll('.timeline-item').forEach((item, index) => {
    item.style.opacity = '0';
    item.style.transform = 'translateX(-30px)';
    item.style.transition = `all 0.6s ease ${index * 0.1}s`;
    timelineObserver.observe(item);
});

// Add particle effect on Hire Me button hover
document.querySelectorAll('.hire-me-btn').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.style.position = 'absolute';
                particle.style.width = '4px';
                particle.style.height = '4px';
                particle.style.background = 'var(--accent)';
                particle.style.borderRadius = '50%';
                particle.style.pointerEvents = 'none';
                particle.style.left = '50%';
                particle.style.top = '50%';
                
                const angle = (Math.random() * 360) * Math.PI / 180;
                const velocity = 50 + Math.random() * 50;
                const tx = Math.cos(angle) * velocity;
                const ty = Math.sin(angle) * velocity;
                
                particle.style.animation = `particle-${i} 0.8s ease-out forwards`;
                
                const keyframes = `
                    @keyframes particle-${i} {
                        to {
                            transform: translate(${tx}px, ${ty}px);
                            opacity: 0;
                        }
                    }
                `;
                
                const styleSheet = document.createElement('style');
                styleSheet.textContent = keyframes;
                document.head.appendChild(styleSheet);
                
                this.appendChild(particle);
                
                setTimeout(() => {
                    particle.remove();
                    styleSheet.remove();
                }, 800);
            }, i * 50);
        }
    });
});

console.log('%c🚀 DevOps Portfolio Loaded!', 'font-size: 16px; color: #64ffda; font-weight: bold;');
console.log('%c✨ All animations and interactions are ready', 'font-size: 12px; color: #8892b0;');
