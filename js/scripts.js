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
