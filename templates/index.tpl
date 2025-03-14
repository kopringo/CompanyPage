<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ settings.meta_title }}</title>
    
    <!-- Meta Tags SEO -->
    <meta name="description" content="{{ settings.meta_description }}">
    <meta name="keywords" content="{{ settings.meta_keywords }}">
    {% if settings.meta_author %}
    <meta name="author" content="{{ settings.meta_author }}">
    {% endif %}
    <meta name="robots" content="{{ settings.meta_robots }}">
    {% if settings.meta_canonical %}
    <link rel="canonical" href="{{ settings.meta_canonical }}">
    {% endif %}
    
    <!-- Open Graph / Social Media Meta Tags -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{{ settings.og_title or settings.meta_title }}">
    <meta property="og:description" content="{{ settings.og_description or settings.meta_description }}">
    {% if settings.og_image %}
    <meta property="og:image" content="{{ settings.og_image }}">
    {% endif %}
    {% if settings.meta_canonical %}
    <meta property="og:url" content="{{ settings.meta_canonical }}">
    {% endif %}
    
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700;900&family=Nunito:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #7e22ce;
            --primary-light: #c084fc;
            --primary-dark: #581c87;
            --secondary-color: #16a34a;
            --secondary-light: #22c55e;
            --text-dark: #1e293b;
            --text-light: #64748b;
            --bg-light: #f8fafc;
            --bg-white: #ffffff;
            --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --border-radius: 0.5rem;
            --transition: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
            scroll-padding-top: 80px;
        }
        
        body {
            font-family: 'Nunito', sans-serif;
            color: var(--text-dark);
            background-color: var(--bg-light);
            line-height: 1.6;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Merriweather', serif;
            font-weight: 700;
            line-height: 1.3;
        }
        
        img {
            max-width: 100%;
            height: auto;
        }
        
        a {
            text-decoration: none;
            color: var(--primary-color);
            transition: var(--transition);
        }
        
        a:hover {
            color: var(--primary-dark);
        }
        
        ul {
            list-style: none;
        }
        
        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }
        
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            text-align: center;
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: var(--transition);
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            color: white;
        }
        
        .btn-primary:hover {
            background-color: var(--primary-dark);
            transform: translateY(-3px);
            box-shadow: var(--shadow);
        }
        
        .btn-secondary {
            background-color: var(--secondary-color);
            color: white;
        }
        
        .btn-secondary:hover {
            background-color: var(--secondary-light);
            transform: translateY(-3px);
            box-shadow: var(--shadow);
        }
        
        .section {
            padding: 5rem 0;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .section-title h2 {
            position: relative;
            display: inline-block;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: var(--primary-color);
        }
        
        .section-title h2::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 3px;
            background-color: var(--primary-color);
        }
        
        .section-title p {
            color: var(--text-light);
            max-width: 700px;
            margin: 0 auto;
        }
        
        /* Header Styles */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: var(--bg-white);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 0;
        }
        
        .logo {
            font-family: 'Merriweather', serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-color);
            display: flex;
            align-items: center;
        }
        
        .logo img {
            height: 60px;
            margin-right: 15px;
            margin-top: -10px;
            margin-bottom: -10px;
            display: block; /* Gwarantuje, że obrazek będzie wyświetlany */
        }
        
        .logo span {
            display: block; /* Gwarantuje, że nazwa firmy będzie wyświetlana */
        }
        
        .nav-links {
            display: flex;
        }
        
        .nav-links li {
            margin-left: 2rem;
        }
        
        .nav-links a {
            color: var(--text-dark);
            font-weight: 600;
            position: relative;
        }
        
        .nav-links a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -5px;
            left: 0;
            background-color: var(--primary-color);
            transition: var(--transition);
        }
        
        .nav-links a:hover,
        .nav-links a.active {
            color: var(--primary-color);
        }
        
        .nav-links a:hover::after,
        .nav-links a.active::after {
            width: 100%;
        }
        
        /* Hero Section */
        .hero {
            position: relative;
            height: 100vh;
            display: flex;
            align-items: center;
            overflow: hidden;
            margin-top: 80px;
        }
        
        .hero-content {
            position: relative;
            z-index: 1;
            max-width: 600px;
        }
        
        .hero-title {
            font-size: 3.5rem;
            margin-bottom: 1.5rem;
            color: var(--primary-color);
        }
        
        .hero-description {
            font-size: 1.1rem;
            margin-bottom: 2rem;
            color: var(--text-light);
        }
        
        .hero-buttons {
            display: flex;
            gap: 1rem;
        }
        
        .hero-image {
            position: absolute;
            top: 0;
            right: 0;
            width: 50%;
            height: 100%;
            clip-path: polygon(25% 0%, 100% 0%, 100% 100%, 0% 100%);
            overflow: hidden;
        }
        
        .hero-slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-size: cover;
            background-position: center;
            opacity: 0;
            transition: opacity 1s ease-in-out;
        }
        
        .hero-slide.active {
            opacity: 1;
        }
        
        .hero-image-overlay {
            position: absolute;
            top: 0;
            right: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(126, 34, 206, 0.3);
            z-index: 1;
        }
        
        /* Services Section */
        .services {
            background-color: var(--bg-white);
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .service-card {
            background-color: var(--bg-light);
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: var(--shadow);
            transition: var(--transition);
        }
        
        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        /* Portfolio Section */
        .portfolio-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .portfolio-item {
            background-color: var(--bg-white);
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: var(--transition);
        }
        
        .portfolio-item:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .portfolio-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            transition: var(--transition);
        }
        
        .portfolio-item:hover .portfolio-image {
            transform: scale(1.1);
        }
        
        .portfolio-content {
            padding: 1.5rem;
        }
        
        .portfolio-title {
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: var(--primary-color);
        }
        
        .portfolio-button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: var(--border-radius);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: inline-block;
        }
        
        .portfolio-button:hover {
            background-color: var(--primary-dark);
            transform: translateY(-3px);
            box-shadow: var(--shadow);
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 2000;
            overflow-y: auto;
        }
        
        .modal-content {
            background-color: var(--bg-white);
            max-width: 900px;
            margin: 3rem auto;
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            animation: modalIn 0.3s ease-out;
        }
        
        @keyframes modalIn {
            from {opacity: 0; transform: scale(0.9);}
            to {opacity: 1; transform: scale(1);}
        }
        
        .modal-header {
            position: relative;
            padding: 2rem;
            background-color: var(--primary-color);
            color: white;
        }
        
        .modal-title {
            font-size: 1.75rem;
            margin: 0;
        }
        
        .modal-close {
            position: absolute;
            top: 1.5rem;
            right: 2rem;
            font-size: 1.75rem;
            color: white;
            cursor: pointer;
            transition: var(--transition);
        }
        
        .modal-close:hover {
            color: var(--primary-light);
            transform: rotate(90deg);
        }
        
        .modal-body {
            padding: 2rem;
        }
        
        .modal-description {
            margin-bottom: 2rem;
            line-height: 1.8;
        }
        
        .modal-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
        }
        
        .modal-gallery img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: var(--border-radius);
            transition: var(--transition);
            cursor: pointer;
        }
        
        .modal-gallery img:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow);
        }
        
        /* Footer */
        .footer {
            background-color: var(--primary-dark);
            padding: 5rem 0 1rem;
            color: white;
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .footer-heading {
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            position: relative;
            padding-bottom: 1rem;
        }
        
        .footer-heading::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            width: 50px;
            height: 2px;
            background-color: var(--primary-light);
        }
        
        .footer-list li {
            margin-bottom: 0.75rem;
        }
        
        .footer-list a {
            color: rgba(255, 255, 255, 0.8);
            transition: var(--transition);
        }
        
        .footer-list a:hover {
            color: var(--primary-light);
            padding-left: 5px;
        }
        
        .footer-text {
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 1.5rem;
        }
        
        .footer-contact-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .footer-contact-icon {
            margin-right: 1rem;
            color: var(--primary-light);
        }
        
        .footer-map {
            width: 100%;
            height: 250px;
            border-radius: var(--border-radius);
            margin-bottom: 1rem;
            border: none;
        }
        
        .footer-bottom {
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* Responsive */
        @media (max-width: 992px) {
            .hero {
                height: auto;
                padding: 5rem 0;
            }
            
            .hero-content {
                max-width: 100%;
                text-align: center;
                margin-bottom: 3rem;
            }
            
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-buttons {
                justify-content: center;
            }
            
            .hero-image {
                position: relative;
                width: 100%;
                height: 400px;
                clip-path: none;
                margin-top: 2rem;
            }
        }
        
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
            }
            
            .logo {
                margin-bottom: 1rem;
            }
            
            .nav-links li {
                margin: 0 1rem;
            }
            
            .section-title h2 {
                font-size: 2rem;
            }
            
            .hero-title {
                font-size: 2rem;
            }
            
            .modal-content {
                width: 95%;
                margin: 1rem auto;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="navbar">
                <div class="logo">
                    {% if settings.company_logo %}
                    <img src="{{ url_for('public_file', filename=settings.company_logo) }}">
                    {% endif %}
                    <span>{{ settings.company_name }}</span>
                </div>
                <ul class="nav-links">
                    <li><a href="#home" class="active">{{ settings.nav_home }}</a></li>
                    <li><a href="#services">{{ settings.services_title }}</a></li>
                    <li><a href="#portfolio">{{ settings.portfolio_title }}</a></li>
                    <li><a href="#contact">{{ settings.nav_contact }}</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <section class="hero" id="home">
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title">{{ settings.main_slogan }}</h1>
                <p class="hero-description">{{ settings.company_description }}</p>
                <div class="hero-buttons">
                    <a href="#portfolio" class="btn btn-primary">Nasze Realizacje</a>
                    <a href="#contact" class="btn btn-secondary">Skontaktuj się</a>
                </div>
            </div>
        </div>
        <div class="hero-image">
            {% for image in carousel_images %}
            <div class="hero-slide" style="background-image: url('{{ url_for('carousel_photo', filename=image) }}')"></div>
            {% endfor %}
            <div class="hero-image-overlay"></div>
        </div>
    </section>

    <section class="section services" id="services">
        <div class="container">
            <div class="section-title">
                <h2>{{ settings.services_title }}</h2>
                <p>{{ settings.services_description }}</p>
            </div>
            <div class="services-grid">
                {% if settings.services_list %}
                    {% for service in settings.services_list.split('\n') %}
                        {% if service.strip() %}
                        <div class="service-card">
                            <h3>{{ service }}</h3>
                        </div>
                        {% endif %}
                    {% endfor %}
                {% endif %}
            </div>
        </div>
    </section>

    <section class="section portfolio" id="portfolio">
        <div class="container">
            <div class="section-title">
                <h2>{{ settings.portfolio_title }}</h2>
                <p>{{ settings.portfolio_description }}</p>
            </div>
            <div class="portfolio-grid">
                {% for realization in realizations %}
                <div class="portfolio-item">
                    {% if realization.main_photo %}
                    <img src="{{ url_for('realization_thumbnail', realization_id=realization.id, filename=realization.main_photo) }}" alt="{{ realization.short_description }}" class="portfolio-image">
                    {% endif %}
                    <div class="portfolio-content">
                        <h3 class="portfolio-title">{{ realization.short_description }}</h3>
                        <button class="portfolio-button" data-realization-id="{{ realization.id }}">Zobacz Więcej</button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <div id="realizacja-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modal-title" class="modal-title"></h2>
                <span class="modal-close">&times;</span>
            </div>
            <div class="modal-body">
                <div id="modal-long-description" class="modal-description"></div>
                <div id="modal-photos" class="modal-gallery"></div>
            </div>
        </div>
    </div>

    <footer class="footer" id="contact">
        <div class="container">
            <div class="footer-grid">

                <div class="footer-column">
                    <h3 class="footer-heading">Kontakt</h3>
                    <div class="footer-contact">
                        <div class="footer-contact-item">
                            <span class="footer-contact-icon">📍</span>
                            <span>{{ settings.address }}</span>
                        </div>
                        <div class="footer-contact-item">
                            <span class="footer-contact-icon">📞</span>
                            <span>{{ settings.phone }}</span>
                        </div>
                        <div class="footer-contact-item">
                            <span class="footer-contact-icon">✉️</span>
                            <span>{{ settings.email }}</span>
                        </div>
                        <div class="footer-contact-item">
                            <span class="footer-contact-icon">🕒</span>
                            <span>{{ settings.working_hours }}</span>
                        </div>
                    </div>
                </div>
                <div class="footer-column">
                    <h3 class="footer-heading">Lokalizacja</h3>
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2325.286545087609!2d19.40626791609345!3d54.1657781801595!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46fd63b535a07c3f%3A0xf853d8eb7e21fc16!2sAl.%20Grunwaldzka%202C%2C%2082-300%20Elbl%C4%85g!5e0!3m2!1spl!2spl!4v1646919851901!5m2!1spl!2spl" class="footer-map" allowfullscreen="" loading="lazy"></iframe>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 {{ settings.company_name }}. Wszelkie prawa zastrzeżone.</p>
            </div>
        </div>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Karuzela zdjęć
            const slides = document.querySelectorAll('.hero-slide');
            let currentSlide = 0;
            
            // Funkcja pokazująca aktualny slajd
            function showSlide(n) {
                // Ukryj wszystkie slajdy
                slides.forEach(slide => {
                    slide.classList.remove('active');
                });
                
                // Pokaż aktualny slajd
                slides[n].classList.add('active');
            }
            
            // Funkcja przełączająca slajdy automatycznie
            function nextSlide() {
                currentSlide = (currentSlide + 1) % slides.length;
                showSlide(currentSlide);
            }
            
            // Pokaż pierwszy slajd na start
            showSlide(0);
            
            // Ustaw interwał przełączania slajdów co 5 sekund
            setInterval(nextSlide, 5000);
            
            // Active navigation links
            const sections = document.querySelectorAll('section');
            const navLinks = document.querySelectorAll('.nav-links a');
            
            window.addEventListener('scroll', function() {
                let current = '';
                
                sections.forEach(section => {
                    const sectionTop = section.offsetTop;
                    const sectionHeight = section.clientHeight;
                    
                    if (pageYOffset >= (sectionTop - 200)) {
                        current = section.getAttribute('id');
                    }
                });
                
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${current}`) {
                        link.classList.add('active');
                    }
                });
            });
            
            // Modal functionality
            const portfolioButtons = document.querySelectorAll('.portfolio-button');
            const modal = document.getElementById('realizacja-modal');
            const closeBtn = document.querySelector('.modal-close');
            const modalTitle = document.getElementById('modal-title');
            const modalDescription = document.getElementById('modal-long-description');
            const modalPhotos = document.getElementById('modal-photos');
            
            portfolioButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const realizationId = this.dataset.realizationId;
                    
                    fetch(`/realization/${realizationId}`)
                        .then(response => response.json())
                        .then(data => {
                            const realization = data.realization;
                            
                            modalTitle.textContent = realization.shortDescription;
                            modalDescription.innerHTML = realization.longDescription;
                            
                            modalPhotos.innerHTML = '';
                            
                            realization.photos.forEach(photo => {
                                const img = document.createElement('img');
                                img.src = `/public_data/${realization.id}/oryginalne/${photo}`;
                                img.alt = realization.shortDescription;
                                modalPhotos.appendChild(img);
                            });
                            
                            modal.style.display = 'block';
                            document.body.style.overflow = 'hidden';
                        });
                });
            });
            
            closeBtn.addEventListener('click', function() {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            });
            
            window.addEventListener('click', function(event) {
                if (event.target === modal) {
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
            });
        });
    </script>
</body>
</html>