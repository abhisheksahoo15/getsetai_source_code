document.addEventListener('DOMContentLoaded', () => {
    // Scroll Animations matching Framer Motion
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const elementsToAnimate = document.querySelectorAll('.animate-on-scroll');
    elementsToAnimate.forEach(el => observer.observe(el));

    // Check backend Supabase connectivity
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                console.log("✅ Backend Supabase client initialized successfully");
            }
        })
        .catch(error => {
            console.error("❌ Backend connectivity issue:", error);
        });
});
