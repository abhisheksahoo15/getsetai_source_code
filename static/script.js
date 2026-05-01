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

    // Supabase Initialization
    // Wait for the Supabase library to load from CDN
    if (typeof supabase !== 'undefined' && window.SUPABASE_URL && window.SUPABASE_KEY) {
        window.supabaseClient = supabase.createClient(window.SUPABASE_URL, window.SUPABASE_KEY);
        console.log("Supabase Client Initialized");
    }
});
