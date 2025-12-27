// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
        });
    });

    // Smooth scrolling for anchor links (only on home page)
    const currentPath = window.location.pathname;
    const isHomePage = currentPath === '/' || currentPath === '';
    
    if (isHomePage) {
        document.querySelectorAll('a[href*="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
                const hashIndex = href.indexOf('#');
                
                if (hashIndex !== -1) {
                    const hash = href.substring(hashIndex);
                    if (hash && hash !== '#') {
                e.preventDefault();
                        const target = document.querySelector(hash);
                if (target) {
                    const offset = 80; // Account for fixed navbar
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - offset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
                }
            });
        });
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });

    // Close alert messages
    const closeAlerts = document.querySelectorAll('.close-alert');
    closeAlerts.forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.alert').style.display = 'none';
        });
    });

    // Auto-hide success messages after 5 seconds
    const successAlerts = document.querySelectorAll('.alert-success');
    successAlerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
    
    // Handle anchor hash on page load (for redirects from careers page)
    if (isHomePage && window.location.hash) {
        const hash = window.location.hash;
        const target = document.querySelector(hash);
        if (target) {
            setTimeout(() => {
                const offset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }, 300);
        }
    }
});

// Job Modal Functions
function openJobModal(jobId) {
    const modal = document.getElementById('jobModal');
    const modalBody = document.getElementById('jobModalBody');
    
    // Show loading
    modalBody.innerHTML = '<div style="text-align: center; padding: 2rem;"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    modal.style.display = 'block';
    
    // Fetch job details
    fetch(`/job-details/${jobId}/`)
        .then(response => response.json())
        .then(data => {
            modalBody.innerHTML = `
                <div class="job-modal-content">
                    <h2>${data.title}</h2>
                    ${data.department ? `<p class="job-dept">${data.department}</p>` : ''}
                    <div class="job-meta-info">
                        <span><i class="fas fa-briefcase"></i> ${data.job_type}</span>
                        <span><i class="fas fa-map-marker-alt"></i> ${data.location}</span>
                        <span><i class="fas fa-user-graduate"></i> ${data.experience_level}</span>
                        ${data.salary_range ? `<span><i class="fas fa-dollar-sign"></i> ${data.salary_range}</span>` : ''}
                    </div>
                    
                    <div class="job-details-section">
                        <h3>Job Description</h3>
                        <p>${data.full_description.replace(/\n/g, '<br>')}</p>
                    </div>
                    
                    <div class="job-details-section">
                        <h3>Requirements</h3>
                        <p>${data.requirements.replace(/\n/g, '<br>')}</p>
                    </div>
                    
                    <div class="job-details-section">
                        <h3>Responsibilities</h3>
                        <p>${data.responsibilities.replace(/\n/g, '<br>')}</p>
                    </div>
                    
                    ${data.preferred_qualifications ? `
                    <div class="job-details-section">
                        <h3>Preferred Qualifications</h3>
                        <p>${data.preferred_qualifications.replace(/\n/g, '<br>')}</p>
                    </div>
                    ` : ''}
                    
                    ${data.technologies ? `
                    <div class="job-details-section">
                        <h3>Technologies</h3>
                        <p>${data.technologies}</p>
                    </div>
                    ` : ''}
                    
                    ${data.benefits ? `
                    <div class="job-details-section">
                        <h3>Benefits</h3>
                        <p>${data.benefits.replace(/\n/g, '<br>')}</p>
                    </div>
                    ` : ''}
                    
                    ${data.application_deadline ? `
                    <div class="job-deadline">
                        <strong>Application Deadline:</strong> ${data.application_deadline}
                    </div>
                    ` : ''}
                    
                    <div class="job-application-form">
                        <h3>Apply for this Position</h3>
                        <form method="post" action="/apply-job/${jobId}/" enctype="multipart/form-data" id="jobApplicationForm">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="full_name">Full Name *</label>
                                    <input type="text" id="full_name" name="full_name" required>
                                </div>
                                <div class="form-group">
                                    <label for="email">Email *</label>
                                    <input type="email" id="email" name="email" required>
                                </div>
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="phone">Phone *</label>
                                    <input type="tel" id="phone" name="phone" required>
                                </div>
                                <div class="form-group">
                                    <label for="current_location">Current Location</label>
                                    <input type="text" id="current_location" name="current_location">
                                </div>
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="current_position">Current Position</label>
                                    <input type="text" id="current_position" name="current_position">
                                </div>
                                <div class="form-group">
                                    <label for="current_company">Current Company</label>
                                    <input type="text" id="current_company" name="current_company">
                                </div>
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="years_of_experience">Years of Experience</label>
                                    <input type="number" id="years_of_experience" name="years_of_experience" min="0" value="0">
                                </div>
                                <div class="form-group">
                                    <label for="resume">Resume * (PDF, DOC, DOCX - Max 5MB)</label>
                                    <input type="file" id="resume" name="resume" accept=".pdf,.doc,.docx" required>
                                </div>
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="linkedin_url">LinkedIn Profile URL</label>
                                    <input type="url" id="linkedin_url" name="linkedin_url">
                                </div>
                                <div class="form-group">
                                    <label for="portfolio_url">Portfolio/GitHub URL</label>
                                    <input type="url" id="portfolio_url" name="portfolio_url">
                                </div>
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group"> 
                                    <label for="availability">Availability (When can you start?)</label>
                                    <input type="text" id="availability" name="availability" placeholder="e.g., Immediately, 2 weeks">
                                </div>
                                <div class="form-group">
                                    <label for="expected_salary">Expected Salary</label>
                                    <input type="text" id="expected_salary" name="expected_salary" placeholder="e.g., PKR 50k - 70k">
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label for="notice_period">Notice Period</label>
                                <input type="text" id="notice_period" name="notice_period" placeholder="e.g., 2 weeks, 1 month">
                            </div>
                            
                            <div class="form-group">
                                <label for="cover_letter">Cover Letter</label>
                                <textarea id="cover_letter" name="cover_letter" rows="5" placeholder="Tell us why you're interested in this position..."></textarea>
                            </div>
                            
                            <button type="submit" class="btn btn-primary btn-large btn-block">Submit Application</button>
                        </form>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            modalBody.innerHTML = '<div style="text-align: center; padding: 2rem; color: red;">Error loading job details. Please try again.</div>';
        });
}

function closeJobModal() {
    document.getElementById('jobModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('jobModal');
    if (event.target == modal) {
        closeJobModal();
    }
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

