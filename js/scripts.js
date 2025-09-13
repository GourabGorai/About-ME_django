/*!
* Start Bootstrap - Resume v7.0.6 (https://startbootstrap.com/theme/resume)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-resume/blob/master/LICENSE)
*/

// --- Google Analytics ---
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'G-H2TRYVGY4X');

// --- PDF.js Configuration ---
// Specify the worker script location for PDF.js library
if (typeof pdfjsLib !== 'undefined') {
    pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js`;
}

// --- PDF Viewer Class ---
class PdfViewer {
    constructor(modalElement) {
        this.modalElement = modalElement;
        this.pdfDoc = null;
        this.pageNum = 1;
        this.pageRendering = false;
        this.pageNumPending = null;
        this.scale = 1.5;

        this.canvas = this.modalElement.querySelector('.pdf-render');
        this.ctx = this.canvas.getContext('2d');
        this.loader = this.modalElement.querySelector('.spinner');
        this.pageNumDisplay = this.modalElement.querySelector('.page-num');
        this.pageCountDisplay = this.modalElement.querySelector('.page-count');

        // Attach event listeners ONCE
        this.modalElement.querySelector('.prev-page').addEventListener('click', () => this.onPrevPage());
        this.modalElement.querySelector('.next-page').addEventListener('click', () => this.onNextPage());
    }

    renderPage(num) {
        this.pageRendering = true;
        this.pdfDoc.getPage(num).then(page => {
            const viewport = page.getViewport({ scale: this.scale });
            this.canvas.height = viewport.height;
            this.canvas.width = viewport.width;

            const renderContext = {
                canvasContext: this.ctx,
                viewport: viewport,
            };
            page.render(renderContext).promise.then(() => {
                this.pageRendering = false;
                if (this.pageNumPending !== null) {
                    this.renderPage(this.pageNumPending);
                    this.pageNumPending = null;
                }
            });
        });
        if(this.pageNumDisplay) this.pageNumDisplay.textContent = num;
    }

    queueRenderPage(num) {
        if (this.pageRendering) {
            this.pageNumPending = num;
        } else {
            this.renderPage(num);
        }
    }

    onPrevPage() {
        if (this.pageNum <= 1) return;
        this.pageNum--;
        this.queueRenderPage(this.pageNum);
    }

    onNextPage() {
        if (this.pageNum >= this.pdfDoc.numPages) return;
        this.pageNum++;
        this.queueRenderPage(this.pageNum);
    }

    load(pdfSrc) {
        if (!this.loader) return;
        this.loader.style.display = 'block';
        const loadingTask = pdfjsLib.getDocument(pdfSrc);
        loadingTask.promise.then(pdf => {
            this.loader.style.display = 'none';
            this.pdfDoc = pdf;
            if(this.pageCountDisplay) this.pageCountDisplay.textContent = this.pdfDoc.numPages;
            this.pageNum = 1;
            this.renderPage(this.pageNum);
        }, reason => {
            console.error(reason);
            this.loader.style.display = 'none';
        });
    }
}

// --- Global Variables ---
let internshipViewer = null;
let resumeViewer = null;


// --- Main Application Logic ---
window.addEventListener('DOMContentLoaded', event => {

    // --- Original Start Bootstrap Logic ---

    // Activate Bootstrap scrollspy on the main nav element
    const sideNav = document.body.querySelector('#sideNav');
    if (sideNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#sideNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // --- Custom Portfolio Logic ---

    // Prevent the default context menu
    document.addEventListener("contextmenu", function (e) {
        e.preventDefault();
    });

    function initializeApp() {
        // Initialize PDF viewers
        internshipViewer = new PdfViewer(document.getElementById('internshipModal'));
        resumeViewer = new PdfViewer(document.getElementById('resumeModal'));

        // --- Element Selectors ---
        const videoModal = document.getElementById('videoModal');
        const videoPlayer = document.getElementById('videoPlayer');
        const closeVideo = document.querySelector('.close-video');
        const playPauseBtn = document.getElementById('playPauseBtn');
        const muteBtn = document.getElementById('muteBtn');
        const skip10Btn = document.getElementById('skip10Btn');
        const skip20Btn = document.getElementById('skip20Btn');
        const skip30Btn = document.getElementById('skip30Btn');
        const back10Btn = document.getElementById('back10Btn');
        const back20Btn = document.getElementById('back20Btn');
        const back30Btn = document.getElementById('back30Btn');
        const progressBar = document.getElementById('progressBar');
        const progressContainer = document.getElementById('progressContainer');
        const timeDisplay = document.getElementById('timeDisplay');
        
        const geminiModal = new bootstrap.Modal(document.getElementById('geminiSummaryModal'));
        const geminiSpinner = document.getElementById('geminiSpinner');
        const geminiContent = document.getElementById('geminiSummaryContent');
        
        const contactForm = document.getElementById('contactForm');


        // --- Contact Form Logic (EmailJS) ---
        if(contactForm) {
            // IMPORTANT: Replace with your public key from EmailJS
            emailjs.init({ publicKey: 'qJsKWmg971wib924k' });

            contactForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const sendMessageButton = document.getElementById('sendMessageButton');
                const formStatus = document.getElementById('form-status');

                // Disable button to prevent multiple submissions
                sendMessageButton.disabled = true;
                sendMessageButton.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Sending...`;

                // --- IMPORTANT: Replace with your own Service ID and Template ID from EmailJS ---
                const serviceID = 'service_rs9m9mq';
                const templateID = 'template_whlfnzb';

                // Get the form data
                const templateParams = {
                    from_name: document.getElementById('name').value,
                    from_email: document.getElementById('email').value,
                    phone_number: document.getElementById('phone').value,
                    message: document.getElementById('message').value
                };
                
                // Send the email
                emailjs.send(serviceID, templateID, templateParams)
                    .then(response => {
                        console.log('SUCCESS!', response.status, response.text);
                        formStatus.innerHTML = `<div class="alert alert-success">Message sent successfully!</div>`;
                        contactForm.reset();
                    }, error => {
                        console.log('FAILED...', error);
                        formStatus.innerHTML = `<div class="alert alert-danger">Oops! Something went wrong. Please try again later.</div>`;
                    })
                    .finally(() => {
                        // Re-enable the button
                        sendMessageButton.disabled = false;
                        sendMessageButton.innerHTML = 'Send';
                    });
            });
        }


        // --- Project Details Modal Logic (iframe) ---
        const detailsModal = document.getElementById('detailsModal');
        const iframe = document.getElementById('modalIframe');
        const span = document.getElementsByClassName('close')[0];

        document.querySelectorAll('.open-modal').forEach(button => {
            button.onclick = function() {
                const page = button.getAttribute('data-page');
                iframe.src = page;
                detailsModal.style.display = 'block';
            }
        });

        if (span) {
            span.onclick = function() {
                detailsModal.style.display = 'none';
                iframe.src = '';
            }
        }

        window.onclick = function(event) {
            if (event.target == detailsModal) {
                detailsModal.style.display = 'none';
                iframe.src = '';
            }
        }

        // --- Video Player Logic ---
        document.querySelectorAll('.play-video').forEach(button => {
            button.addEventListener('click', function () {
                const videoSrc = this.getAttribute('data-video');
                videoPlayer.src = videoSrc;
                videoModal.style.display = 'flex';
                videoPlayer.play();
                updatePlayPauseButton();
                updateMuteButton();
            });
        });

        if (closeVideo) {
            closeVideo.addEventListener('click', () => {
                videoModal.style.display = 'none';
                videoPlayer.pause();
                videoPlayer.src = '';
            });
        }
        
        if (playPauseBtn) {
            playPauseBtn.addEventListener('click', () => {
                if (videoPlayer.paused) {
                    videoPlayer.play();
                } else {
                    videoPlayer.pause();
                }
                updatePlayPauseButton();
            });
        }

        const skipTime = (amount) => {
            if (videoPlayer.duration) { 
                videoPlayer.currentTime = Math.max(0, Math.min(videoPlayer.duration, videoPlayer.currentTime + amount));
            }
        };

        if(skip10Btn) skip10Btn.addEventListener('click', () => skipTime(10));
        if(skip20Btn) skip20Btn.addEventListener('click', () => skipTime(20));
        if(skip30Btn) skip30Btn.addEventListener('click', () => skipTime(30));
        if(back10Btn) back10Btn.addEventListener('click', () => skipTime(-10));
        if(back20Btn) back20Btn.addEventListener('click', () => skipTime(-20));
        if(back30Btn) back30Btn.addEventListener('click', () => skipTime(-30));

        if (muteBtn) {
            muteBtn.addEventListener('click', () => {
                videoPlayer.muted = !videoPlayer.muted;
                updateMuteButton();
            });
        }

        function updatePlayPauseButton() {
            if (playPauseBtn) playPauseBtn.textContent = videoPlayer.paused ? 'Play' : 'Pause';
        }

        function updateMuteButton() {
            if (muteBtn) muteBtn.textContent = videoPlayer.muted ? 'Unmute' : 'Mute';
        }

        if (videoPlayer) {
            videoPlayer.addEventListener('play', updatePlayPauseButton);
            videoPlayer.addEventListener('pause', updatePlayPauseButton);
            videoPlayer.addEventListener('volumechange', updateMuteButton);

            videoPlayer.addEventListener('timeupdate', () => {
                const { currentTime, duration } = videoPlayer;
                if (duration) {
                    const progressPercent = (currentTime / duration) * 100;
                    if (progressBar) progressBar.style.width = `${progressPercent}%`;
                    if (timeDisplay) timeDisplay.textContent = `${formatTime(currentTime)} / ${formatTime(duration)}`;
                }
            });
        }
        
        // --- Video Progress Bar Seeking Logic ---
        let isSeeking = false;
        const startSeek = (e) => { isSeeking = true; updateSeek(e); };
        const stopSeek = () => { isSeeking = false; };
        const updateSeek = (e) => {
            if (!isSeeking || !videoPlayer.duration) return;
            e.preventDefault(); 
            const event = e.touches ? e.touches[0] : e;
            const rect = progressContainer.getBoundingClientRect();
            const newTime = ((event.clientX - rect.left) / progressContainer.clientWidth) * videoPlayer.duration;
            videoPlayer.currentTime = Math.max(0, Math.min(newTime, videoPlayer.duration));
        };

        if (progressContainer) {
            progressContainer.addEventListener('mousedown', startSeek);
            document.addEventListener('mousemove', updateSeek);
            document.addEventListener('mouseup', stopSeek);
            progressContainer.addEventListener('touchstart', startSeek);
            document.addEventListener('touchmove', updateSeek);
            document.addEventListener('touchend', stopSeek);
        }
        
        function formatTime(seconds) {
            if (isNaN(seconds)) return "00:00";
            const minutes = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        }

        // --- Gemini AI Summary Generation ---
        async function callGeminiAPI(prompt, maxRetries = 3) {
            const apiKey = "AIzaSyBYbmBSicVfWFMTGSfnKkIyLPCfxZyZEIc";
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${apiKey}`;
            
            const payload = { contents: [{ role: "user", parts: [{ text: prompt }] }] };
            let attempt = 0;
            while (attempt < maxRetries) {
                try {
                    const response = await fetch(apiUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    
                    const result = await response.json();
                    if (result.candidates?.[0]?.content?.parts?.[0]?.text) {
                        return result.candidates[0].content.parts[0].text;
                    } else {
                        throw new Error("Invalid response structure from Gemini API");
                    }
                } catch (error) {
                    console.error(`Attempt ${attempt + 1} failed:`, error);
                    attempt++;
                    if (attempt >= maxRetries) {
                        return "Sorry, I couldn't generate a summary at this moment. Please try again later.";
                    }
                    await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
                }
            }
        }

        document.querySelectorAll('.generate-summary').forEach(button => {
            button.addEventListener('click', async function() {
                const projectTitle = this.dataset.title;
                const projectTech = this.dataset.tech;

                geminiContent.textContent = '';
                geminiSpinner.style.display = 'block';
                geminiModal.show();

                const prompt = `Generate a professional, one-paragraph project summary for a developer's portfolio. The project is titled "${projectTitle}" and uses the following technologies: ${projectTech}. The summary should be concise, highlight the project's purpose and the technologies used, and be engaging for potential employers.`;
                const summary = await callGeminiAPI(prompt);
                
                geminiSpinner.style.display = 'none';
                geminiContent.textContent = summary;
            });
        });

        // --- Initialize Libraries (AOS, tsParticles) ---
        AOS.init({ duration: 800, once: true });
        
        const particlesConfig = {
            fpsLimit: 60,
            interactivity: {
                events: { onHover: { enable: true, mode: "repulse" }, resize: true },
                modes: { repulse: { distance: 100, duration: 0.4 } },
            },
            particles: {
                color: { value: "#6c757d" },
                links: { color: "#6c757d", distance: 150, enable: true, opacity: 0.5, width: 1 },
                collisions: { enable: true },
                move: { direction: "none", enable: true, outModes: { default: "bounce" }, random: false, speed: 1.5, straight: false },
                number: { density: { enable: true, area: 800 }, value: 80 },
                opacity: { value: 0.5 },
                shape: { type: "circle" },
                size: { value: { min: 1, max: 4 } },
            },
            detectRetina: true,
        };

        tsParticles.load("tsparticles", particlesConfig).then(container => {
            const themeToggleButton = document.getElementById('theme-toggle');
            const htmlElement = document.documentElement;

            const updateParticleColors = () => {
                const isDark = htmlElement.classList.contains('dark-theme');
                const particleColor = isDark ? '#e0e0e0' : '#6c757d';
                container.options.particles.color.value = particleColor;
                container.options.particles.links.color = particleColor;
                container.refresh();
            };
            
            updateParticleColors();
            themeToggleButton.addEventListener('click', (event) => {
                event.preventDefault();
                htmlElement.classList.toggle('dark-theme');
                updateParticleColors();
            });

            // Initialize Interactive Theme Manager
            initializeInteractiveThemes(container);
        });
    }

    initializeApp();

});

// --- Global Functions for onclick Attributes ---
// These functions must be in the global scope to be called by onclick attributes in HTML.

function openModal(imgSrc, imgTitle, imgDescription) {
    document.getElementById("modalImage").src = imgSrc;
    document.getElementById("imageModalLabel").innerText = imgTitle;
    document.getElementById("modalDescription").innerText = imgDescription;
    const myModal = new bootstrap.Modal(document.getElementById('imageModal'));
    myModal.show();
}

function openHackathonDetailsModal(title, images, description) {
    document.getElementById("hackathonDetailsModalLabel").innerText = title;
    document.getElementById("hackathonDescription").innerText = description;

    const imagesContainer = document.getElementById("hackathonImages");
    imagesContainer.innerHTML = ''; // Clear previous images
    images.forEach(src => {
        const col = document.createElement("div");
        col.className = "col-md-4 mb-3";
        const img = document.createElement("img");
        img.src = src;
        img.alt = "Hackathon Detail Image";
        img.className = "img-fluid";
        col.appendChild(img);
        imagesContainer.appendChild(col);
    });

    const myModal = new bootstrap.Modal(document.getElementById('hackathonDetailsModal'));
    myModal.show();
}

function openInternshipModal(imgSrc, title, pdfSrc, description) {
    const modalElement = document.getElementById('internshipModal');
    const modal = new bootstrap.Modal(modalElement);
    
    modalElement.querySelector('#internshipImage').src = imgSrc;
    modalElement.querySelector('#internshipModalLabel').innerText = title;
    modalElement.querySelector('#internshipDescription').innerText = description;
    
    if (internshipViewer) {
        internshipViewer.load(pdfSrc);
    }
    modal.show();
}

function openResumeModal() {
    const modalElement = document.getElementById('resumeModal');
    const modal = new bootstrap.Modal(modalElement);
    if (resumeViewer) {
        resumeViewer.load('assets/pdf/resume.pdf');
    }
    modal.show();
}

// --- Interactive Theme Management ---
function initializeInteractiveThemes(particlesContainer) {
    let currentTheme = 'particles';
    let mouseX = 0, mouseY = 0;
    let lastMouseX = 0, lastMouseY = 0;
    let scrollY = 0;
    let stars = [];
    let scrollParticles = [];
    let matrixChars = [];
    let neuralNodes = [];
    let neuralConnections = [];
    let waveBars = [];
    let gravityParticles = [];

    const themeContainer = document.getElementById('theme-bg-container');
    const tsParticlesElement = document.getElementById('tsparticles');
    const floatingContainer = document.querySelector('.floating-container');

    // Theme switching function
    function switchTheme(theme) {
        // Clear current theme
        themeContainer.innerHTML = '';
        themeContainer.className = 'theme-bg-container';
        
        // Remove all theme classes from body
        document.body.classList.remove(
            'theme-particles', 'theme-constellation', 'theme-ripple', 
            'theme-scroll', 'theme-matrix', 'theme-neural', 
            'theme-sound', 'theme-gravity'
        );
        
        // Add new theme class to body for font styling
        document.body.classList.add(`theme-${theme}`);
        
        // Update active button
        document.querySelectorAll('.theme-option').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-theme="${theme}"]`).classList.add('active');
        
        // Show/hide particles and floating objects based on theme
        if (theme === 'particles') {
            tsParticlesElement.style.display = 'block';
            floatingContainer.style.display = 'block';
            themeContainer.classList.remove('interactive');
        } else {
            tsParticlesElement.style.display = 'none';
            floatingContainer.style.display = 'none';
            themeContainer.classList.add('interactive');
        }
        
        currentTheme = theme;
        initializeTheme(theme);
    }

    // Initialize specific theme
    function initializeTheme(theme) {
        switch(theme) {
            case 'particles':
                // Default particles theme - already handled
                break;
            case 'constellation':
                initConstellation();
                break;
            case 'ripple':
                initRipple();
                break;
            case 'scroll':
                initScrollParticles();
                break;
            case 'matrix':
                initMatrix();
                break;
            case 'neural':
                initNeuralNetwork();
                break;
            case 'sound':
                initSoundWave();
                break;
            case 'gravity':
                initGravityField();
                break;
        }
    }

    // Theme 1: Constellation
    function initConstellation() {
        themeContainer.className = 'theme-bg-container constellation-bg';
        stars = [];
    }

    function createStar(x, y) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = x + 'px';
        star.style.top = y + 'px';
        themeContainer.appendChild(star);
        
        setTimeout(() => star.style.opacity = '1', 50);
        
        stars.push({element: star, x: x, y: y, age: 0});
        
        if (stars.length > 50) {
            const oldStar = stars.shift();
            oldStar.element.remove();
        }
        
        updateConstellationConnections();
    }

    function updateConstellationConnections() {
        themeContainer.querySelectorAll('.constellation-line').forEach(line => line.remove());
        
        for (let i = 0; i < stars.length; i++) {
            for (let j = i + 1; j < stars.length; j++) {
                const star1 = stars[i];
                const star2 = stars[j];
                const distance = Math.sqrt(
                    Math.pow(star1.x - star2.x, 2) + 
                    Math.pow(star1.y - star2.y, 2)
                );
                
                if (distance < 100) {
                    const line = document.createElement('div');
                    line.className = 'constellation-line';
                    line.style.left = star1.x + 'px';
                    line.style.top = star1.y + 'px';
                    line.style.width = distance + 'px';
                    line.style.transformOrigin = 'left center';
                    
                    const angle = Math.atan2(star2.y - star1.y, star2.x - star1.x);
                    line.style.transform = `rotate(${angle}rad)`;
                    line.style.opacity = Math.max(0, 1 - distance / 100);
                    
                    themeContainer.appendChild(line);
                }
            }
        }
    }

    // Theme 2: Ripple Effect
    function initRipple() {
        themeContainer.className = 'theme-bg-container ripple-bg';
    }

    function createRipple(x, y) {
        const ripple = document.createElement('div');
        ripple.className = 'ripple';
        ripple.style.left = (x - 10) + 'px';
        ripple.style.top = (y - 10) + 'px';
        ripple.style.width = '20px';
        ripple.style.height = '20px';
        themeContainer.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 2000);
    }

    // Theme 3: Scroll Particles
    function initScrollParticles() {
        themeContainer.className = 'theme-bg-container scroll-particles-bg';
        scrollParticles = [];
        
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'scroll-particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            themeContainer.appendChild(particle);
            
            scrollParticles.push({
                element: particle,
                baseX: Math.random() * window.innerWidth,
                baseY: Math.random() * window.innerHeight,
                velX: 0,
                velY: 0
            });
        }
    }

    // Theme 4: Matrix
    function initMatrix() {
        themeContainer.className = 'theme-bg-container reactive-matrix-bg';
        matrixChars = [];
        
        const characters = '0123456789ABCDEFabcdef<>{}[]()';
        
        for (let i = 0; i < 100; i++) {
            const char = document.createElement('div');
            char.className = 'matrix-char';
            char.textContent = characters[Math.floor(Math.random() * characters.length)];
            char.style.left = Math.random() * 100 + '%';
            char.style.top = Math.random() * 100 + '%';
            themeContainer.appendChild(char);
            
            matrixChars.push({
                element: char,
                activated: false
            });
        }
    }

    // Theme 5: Neural Network
    function initNeuralNetwork() {
        themeContainer.className = 'theme-bg-container interactive-neural-bg';
        neuralNodes = [];
        neuralConnections = [];
        
        // Create nodes
        for (let i = 0; i < 15; i++) {
            const node = document.createElement('div');
            node.className = 'neural-node';
            const x = Math.random() * (window.innerWidth - 50) + 25;
            const y = Math.random() * (window.innerHeight - 50) + 25;
            node.style.left = x + 'px';
            node.style.top = y + 'px';
            themeContainer.appendChild(node);
            
            const nodeData = {element: node, x: x, y: y, activated: false};
            neuralNodes.push(nodeData);
            
            node.addEventListener('mouseenter', () => activateNeuralNode(nodeData));
            node.addEventListener('mouseleave', () => deactivateNeuralNode(nodeData));
        }
        
        // Create connections
        for (let i = 0; i < neuralNodes.length; i++) {
            for (let j = i + 1; j < neuralNodes.length; j++) {
                const node1 = neuralNodes[i];
                const node2 = neuralNodes[j];
                const distance = Math.sqrt(
                    Math.pow(node1.x - node2.x, 2) + 
                    Math.pow(node1.y - node2.y, 2)
                );
                
                if (distance < 200) {
                    const connection = document.createElement('div');
                    connection.className = 'neural-connection';
                    connection.style.left = node1.x + 'px';
                    connection.style.top = node1.y + 'px';
                    connection.style.width = distance + 'px';
                    
                    const angle = Math.atan2(node2.y - node1.y, node2.x - node1.x);
                    connection.style.transform = `rotate(${angle}rad)`;
                    
                    themeContainer.appendChild(connection);
                    neuralConnections.push({
                        element: connection,
                        node1: i,
                        node2: j
                    });
                }
            }
        }
    }

    function activateNeuralNode(nodeData) {
        nodeData.activated = true;
        nodeData.element.classList.add('activated');
        
        neuralConnections.forEach(conn => {
            if (neuralNodes[conn.node1] === nodeData || neuralNodes[conn.node2] === nodeData) {
                conn.element.classList.add('active');
            }
        });
    }

    function deactivateNeuralNode(nodeData) {
        nodeData.activated = false;
        nodeData.element.classList.remove('activated');
        
        neuralConnections.forEach(conn => {
            if (neuralNodes[conn.node1] === nodeData || neuralNodes[conn.node2] === nodeData) {
                conn.element.classList.remove('active');
            }
        });
    }

    // Theme 6: Sound Wave
    function initSoundWave() {
        themeContainer.className = 'theme-bg-container sound-wave-bg';
        waveBars = [];
        
        const barCount = Math.floor(window.innerWidth / 8);
        
        for (let i = 0; i < barCount; i++) {
            const bar = document.createElement('div');
            bar.className = 'wave-bar';
            bar.style.left = (i * 8) + 'px';
            bar.style.height = '5px';
            themeContainer.appendChild(bar);
            
            waveBars.push({
                element: bar,
                index: i
            });
        }
    }

    // Theme 7: Gravity Field
    function initGravityField() {
        themeContainer.className = 'theme-bg-container gravity-bg';
        gravityParticles = [];
        
        for (let i = 0; i < 40; i++) {
            const particle = document.createElement('div');
            particle.className = 'gravity-particle';
            const x = Math.random() * window.innerWidth;
            const y = Math.random() * window.innerHeight;
            particle.style.left = x + 'px';
            particle.style.top = y + 'px';
            themeContainer.appendChild(particle);
            
            gravityParticles.push({
                element: particle,
                x: x,
                y: y,
                velX: 0,
                velY: 0
            });
        }
    }

    // Event handlers
    function handleMouseMove(e) {
        lastMouseX = mouseX;
        lastMouseY = mouseY;
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        switch(currentTheme) {
            case 'constellation':
                if (Math.random() < 0.3) {
                    createStar(e.clientX, e.clientY);
                }
                break;
            
            case 'sound':
                waveBars.forEach((bar, index) => {
                    const distance = Math.abs((index * 8) - e.clientX);
                    const height = Math.max(5, 100 - distance / 5);
                    bar.element.style.height = height + 'px';
                });
                break;
            
            case 'gravity':
                gravityParticles.forEach(particle => {
                    const dx = e.clientX - particle.x;
                    const dy = e.clientY - particle.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    const force = Math.min(200 / (distance + 1), 5);
                    
                    particle.velX += (dx / distance) * force * 0.1;
                    particle.velY += (dy / distance) * force * 0.1;
                    
                    particle.velX *= 0.95;
                    particle.velY *= 0.95;
                    
                    particle.x += particle.velX;
                    particle.y += particle.velY;
                    
                    particle.element.style.left = particle.x + 'px';
                    particle.element.style.top = particle.y + 'px';
                });
                break;
            
            case 'matrix':
                matrixChars.forEach((char, index) => {
                    const charRect = char.element.getBoundingClientRect();
                    const distance = Math.sqrt(
                        Math.pow(e.clientX - (charRect.left + 8), 2) +
                        Math.pow(e.clientY - (charRect.top + 8), 2)
                    );
                    
                    if (distance < 100) {
                        char.element.classList.add('active');
                        setTimeout(() => {
                            char.element.classList.remove('active');
                        }, 500);
                    }
                });
                break;
        }
    }

    function handleClick(e) {
        if (currentTheme === 'ripple') {
            createRipple(e.clientX, e.clientY);
            setTimeout(() => createRipple(e.clientX + 20, e.clientY + 10), 100);
            setTimeout(() => createRipple(e.clientX - 15, e.clientY - 5), 200);
        }
    }

    function handleKeypress(e) {
        if (currentTheme === 'matrix') {
            const activateCount = Math.floor(Math.random() * 10) + 5;
            for (let i = 0; i < activateCount; i++) {
                const randomChar = matrixChars[Math.floor(Math.random() * matrixChars.length)];
                randomChar.element.classList.add('active');
                setTimeout(() => {
                    randomChar.element.classList.remove('active');
                }, 1000);
            }
        }
    }

    function handleScroll(e) {
        if (currentTheme === 'scroll') {
            const scrollVel = scrollY - (window.lastScrollY || 0);
            window.lastScrollY = scrollY;
            
            scrollParticles.forEach((particle, index) => {
                particle.velY += scrollVel * 0.1;
                particle.velX += (Math.random() - 0.5) * scrollVel * 0.05;
                
                particle.velX *= 0.95;
                particle.velY *= 0.95;
                
                particle.element.style.transform = `translate(${particle.velX}px, ${particle.velY}px)`;
            });
        }
    }

    // Event listeners
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('click', handleClick);
    document.addEventListener('keypress', handleKeypress);
    
    let scrollTimeout;
    document.addEventListener('scroll', (e) => {
        scrollY = window.scrollY;
        handleScroll(e);
        
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            if (currentTheme === 'scroll') {
                scrollParticles.forEach(particle => {
                    particle.element.style.transform = 'translate(0px, 0px)';
                });
            }
        }, 150);
    });

    // Theme selector event listeners
    document.querySelectorAll('.theme-option').forEach(button => {
        button.addEventListener('click', function() {
            const theme = this.getAttribute('data-theme');
            switchTheme(theme);
        });
    });

    // Resize handler
    window.addEventListener('resize', () => {
        if (currentTheme !== 'particles') {
            initializeTheme(currentTheme);
        }
    });

    // Initialize with default theme
    switchTheme('particles');
}
