// ============================================
// SPACEX WEBSITE ADVANCED ANIMATIONS
// Version 2.0 - Enhanced Experience
// ============================================

// Check for reduced motion preference
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ============================================
// THREE.JS SPACE BACKGROUND
// ============================================
function initSpaceBackground() {
    if (prefersReducedMotion) return;

    const canvas = document.getElementById('space-bg');
    if (!canvas || typeof THREE === 'undefined') return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Create stars
    const starGeometry = new THREE.BufferGeometry();
    const starCount = 3000;
    const positions = new Float32Array(starCount * 3);
    const colors = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 2000;
        positions[i + 1] = (Math.random() - 0.5) * 2000;
        positions[i + 2] = (Math.random() - 0.5) * 2000;

        // Vary star colors (white, blue-white, yellow)
        const colorChoice = Math.random();
        if (colorChoice < 0.7) {
            colors[i] = 1; colors[i + 1] = 1; colors[i + 2] = 1; // White
        } else if (colorChoice < 0.9) {
            colors[i] = 0.8; colors[i + 1] = 0.9; colors[i + 2] = 1; // Blue-white
        } else {
            colors[i] = 1; colors[i + 1] = 0.95; colors[i + 2] = 0.8; // Yellow
        }
    }

    starGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    starGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const starMaterial = new THREE.PointsMaterial({
        size: 2,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true
    });

    const stars = new THREE.Points(starGeometry, starMaterial);
    scene.add(stars);

    // Add nebula effect
    const nebulaGeometry = new THREE.BufferGeometry();
    const nebulaCount = 300;
    const nebulaPositions = new Float32Array(nebulaCount * 3);

    for (let i = 0; i < nebulaCount * 3; i += 3) {
        nebulaPositions[i] = (Math.random() - 0.5) * 1500;
        nebulaPositions[i + 1] = (Math.random() - 0.5) * 1500;
        nebulaPositions[i + 2] = (Math.random() - 0.5) * 1500;
    }

    nebulaGeometry.setAttribute('position', new THREE.BufferAttribute(nebulaPositions, 3));

    const nebulaMaterial = new THREE.PointsMaterial({
        size: 25,
        color: 0x0066ff,
        transparent: true,
        opacity: 0.08,
        sizeAttenuation: true
    });

    const nebula = new THREE.Points(nebulaGeometry, nebulaMaterial);
    scene.add(nebula);

    camera.position.z = 500;

    // Mouse movement effect
    let mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    });

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);

        stars.rotation.x += 0.0001;
        stars.rotation.y += 0.0002;

        nebula.rotation.x += 0.00005;
        nebula.rotation.y += 0.0001;

        // Smooth camera movement based on mouse
        camera.position.x += (mouseX * 30 - camera.position.x) * 0.02;
        camera.position.y += (-mouseY * 30 - camera.position.y) * 0.02;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }

    animate();

    // Handle resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// ============================================
// SCROLL PROGRESS BAR
// ============================================
function initScrollProgress() {
    const progressBar = document.querySelector('.scroll-progress');
    if (!progressBar) return;

    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = scrollTop / docHeight;
        progressBar.style.transform = `scaleX(${scrollPercent})`;
    });
}

// ============================================
// GSAP SCROLL ANIMATIONS
// ============================================
function initGSAPAnimations() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
    if (prefersReducedMotion) return;

    gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

    // Hero section animation
    const heroTl = gsap.timeline();
    heroTl
        .from('.hero-title', {
            y: 100,
            opacity: 0,
            duration: 1,
            ease: 'power4.out'
        })
        .from('.hero-subtitle', {
            y: 50,
            opacity: 0,
            duration: 0.8,
            ease: 'power3.out'
        }, '-=0.5')
        .from('.stat-card', {
            y: 80,
            opacity: 0,
            duration: 0.6,
            stagger: 0.15,
            ease: 'back.out(1.7)'
        }, '-=0.3')
        .from('.hero-cta', {
            y: 30,
            opacity: 0,
            duration: 0.5,
            ease: 'power2.out'
        }, '-=0.2');

    // Section headers animation - EXCLUDE no-animate sections
    gsap.utils.toArray('.section-header').forEach(header => {
        // Skip headers in no-animate sections (SHAP, Presentation)
        if (header.closest('.no-animate') || header.closest('#shap') || header.closest('#presentation')) {
            return;
        }
        gsap.from(header, {
            scrollTrigger: {
                trigger: header,
                start: 'top 85%',
                toggleActions: 'play none none none' // Changed: don't reverse on scroll away
            },
            y: 60,
            opacity: 0,
            duration: 0.8,
            ease: 'power3.out'
        });
    });

    // Cards stagger animation - EXCLUDE cards in no-animate sections
    const cardSelectors = '.sql-card, .finding-card, .conclusion-card, .content-card, .method-card, .ml-insight-card, .geo-insight-card';
    // Note: Removed .insight-item from selectors to avoid SHAP section conflicts
    gsap.utils.toArray(cardSelectors).forEach((card, i) => {
        // Skip cards in no-animate sections
        if (card.closest('.no-animate') || card.closest('#shap') || card.closest('#presentation')) {
            return;
        }
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 90%',
                toggleActions: 'play none none none' // Changed: don't reverse on scroll away
            },
            y: 50,
            opacity: 0,
            duration: 0.6,
            delay: (i % 3) * 0.1,
            ease: 'power2.out'
        });
    });

    // Floating elements animation
    gsap.utils.toArray('.stat-card').forEach(el => {
        gsap.to(el, {
            y: 'random(-10, 10)',
            duration: 'random(3, 5)',
            ease: 'sine.inOut',
            repeat: -1,
            yoyo: true
        });
    });
}

// ============================================
// SMOOTH SCROLL NAVIGATION
// ============================================
function initSmoothScroll() {
    if (typeof gsap === 'undefined') return;

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                gsap.to(window, {
                    duration: 1,
                    scrollTo: { y: target, offsetY: 80 },
                    ease: 'power3.inOut'
                });
            }
        });
    });
}

// ============================================
// MAGNETIC BUTTONS
// ============================================
function initMagneticButtons() {
    if (prefersReducedMotion) return;

    const buttons = document.querySelectorAll('.btn-primary, .btn-glow');

    buttons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            gsap.to(btn, {
                x: x * 0.2,
                y: y * 0.2,
                duration: 0.3,
                ease: 'power2.out'
            });
        });

        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, {
                x: 0,
                y: 0,
                duration: 0.5,
                ease: 'elastic.out(1, 0.5)'
            });
        });
    });
}

// ============================================
// TILT EFFECT ON CARDS
// ============================================
function initTiltEffect() {
    if (prefersReducedMotion) return;

    const cards = document.querySelectorAll('.sql-card, .stat-card, .conclusion-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            gsap.to(card, {
                rotateX: rotateX,
                rotateY: rotateY,
                transformPerspective: 1000,
                duration: 0.3,
                ease: 'power2.out'
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                rotateX: 0,
                rotateY: 0,
                duration: 0.5,
                ease: 'elastic.out(1, 0.5)'
            });
        });
    });
}

// ============================================
// CUSTOM CURSOR (Desktop Only)
// ============================================
function initCursorFollower() {
    // Check for touch device
    if ('ontouchstart' in window || prefersReducedMotion) return;

    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);

    const cursorDot = document.createElement('div');
    cursorDot.className = 'cursor-dot';
    document.body.appendChild(cursorDot);

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;

        gsap.to(cursorDot, {
            x: mouseX,
            y: mouseY,
            duration: 0.1
        });
    });

    gsap.ticker.add(() => {
        cursorX += (mouseX - cursorX) * 0.15;
        cursorY += (mouseY - cursorY) * 0.15;
        cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;
    });

    // Hover effects
    document.querySelectorAll('a, button, .clickable, .btn, .sql-card, .nav-link').forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.classList.add('cursor-hover');
            cursorDot.classList.add('cursor-hover');
        });
        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('cursor-hover');
            cursorDot.classList.remove('cursor-hover');
        });
    });
}

// ============================================
// PARALLAX EFFECT
// ============================================
function initParallax() {
    if (prefersReducedMotion) return;

    const morphElements = document.querySelectorAll('.morph-bg');

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        morphElements.forEach((el, i) => {
            const speed = 0.1 + (i * 0.05);
            el.style.transform = `translateY(${scrollY * speed}px)`;
        });
    });
}

// ============================================
// COUNTER ANIMATION ENHANCEMENT
// ============================================
function initEnhancedCounters() {
    if (prefersReducedMotion) return;

    const counters = document.querySelectorAll('.stat-value[data-count]');

    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                entry.target.dataset.animated = 'true';

                const target = parseFloat(entry.target.dataset.count);
                const suffix = entry.target.textContent.includes('%') ? '%' :
                               entry.target.textContent.includes('+') ? '+' : '';

                if (typeof anime !== 'undefined') {
                    anime({
                        targets: entry.target,
                        innerHTML: [0, target],
                        easing: 'easeOutExpo',
                        round: target % 1 === 0 ? 1 : 10,
                        duration: 2000,
                        update: function(anim) {
                            const val = parseFloat(entry.target.innerHTML);
                            entry.target.innerHTML = (target % 1 === 0 ? Math.round(val) : val.toFixed(1)) + suffix;
                        }
                    });
                }
            }
        });
    }, observerOptions);

    counters.forEach(counter => observer.observe(counter));
}

// ============================================
// NAVBAR SCROLL EFFECT
// ============================================
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;

        if (currentScroll > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Hide/show navbar on scroll direction
        if (currentScroll > lastScroll && currentScroll > 300) {
            navbar.classList.add('nav-hidden');
        } else {
            navbar.classList.remove('nav-hidden');
        }

        lastScroll = currentScroll;
    });
}

// ============================================
// SECTION REVEAL ANIMATION
// ============================================
function initSectionReveal() {
    if (prefersReducedMotion) return;

    // EXCLUDE no-animate sections from reveal animation
    const sections = document.querySelectorAll('.section:not(.no-animate):not(#shap):not(#presentation)');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '-50px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('section-visible');
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        section.classList.add('section-hidden');
        observer.observe(section);
    });

    // Ensure problem sections are ALWAYS visible
    document.querySelectorAll('.no-animate, #shap, #presentation').forEach(section => {
        section.classList.remove('section-hidden');
        section.classList.add('section-visible');
        section.style.opacity = '1';
        section.style.visibility = 'visible';
    });
}

// ============================================
// GLOW EFFECT ON CARDS
// ============================================
function initGlowEffect() {
    if (prefersReducedMotion) return;

    const glowCards = document.querySelectorAll('.stat-card, .conclusion-card, .presentation-preview');

    glowCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;

            card.style.setProperty('--glow-x', `${x}%`);
            card.style.setProperty('--glow-y', `${y}%`);
        });
    });
}

// ============================================
// INITIALIZE ALL ANIMATIONS
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all animations
    initSpaceBackground();
    initScrollProgress();
    initGSAPAnimations();
    initSmoothScroll();
    initMagneticButtons();
    initTiltEffect();
    initCursorFollower();
    initParallax();
    initEnhancedCounters();
    initNavbarScroll();
    initSectionReveal();
    initGlowEffect();

    console.log('SpaceX Advanced Animations Initialized');
});

// Accessibility: Listen for reduced motion preference changes
window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
    if (e.matches) {
        // Disable animations
        document.body.classList.add('reduced-motion');
        if (typeof gsap !== 'undefined') {
            gsap.globalTimeline.pause();
        }
    } else {
        document.body.classList.remove('reduced-motion');
        if (typeof gsap !== 'undefined') {
            gsap.globalTimeline.resume();
        }
    }
});
