# IT Solutions Website - Django Project

A beautiful, responsive IT solutions company website built with Django. This website is designed to convert visitors into clients with a modern design and comprehensive features.

## Features

- **Modern & Responsive Design**: Fully responsive design that works perfectly on mobile, tablet, and desktop
- **Admin Panel**: Complete admin interface to manage all website content
- **Service Showcase**: Display your services with icons and descriptions
- **Portfolio**: Showcase your projects with images and details
- **Team Section**: Display your team members with photos and social links
- **Testimonials**: Client testimonials with ratings
- **Project Request Form**: Contact form for clients to submit project requests
- **Beautiful UI**: Modern color scheme with smooth animations

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/ehsanahmad/Documents/mySolutions
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (for admin panel):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the website:**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Admin Panel Usage

### Accessing Admin Panel
1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials

### Managing Content

#### Services
- Add your services (Web Development, Mobile Apps, etc.)
- Set order for display
- Enable/disable services
- Use Font Awesome icon classes (e.g., `fa-code`, `fa-mobile-alt`)

#### Projects
- Add portfolio projects
- Upload project images
- Set featured projects (shown on homepage)
- Add technologies used

#### Team Members
- Add team members with photos
- Add designations and bios
- Link social media profiles

#### Testimonials
- Add client testimonials
- Set ratings (1-5 stars)
- Mark as featured for homepage display
- Upload client photos (optional)

#### Project Requests
- View all project requests submitted through the contact form
- Update status (New, Contacted, In Progress, Completed, Closed)
- Add internal notes
- Contact information of potential clients

#### Site Settings
- Update company information
- Set email, phone, address
- Add social media links
- Update tagline

## Project Structure

```
mySolutions/
├── it_solutions/          # Django project settings
├── website/               # Main app
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── admin.py          # Admin configuration
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JS, images
├── manage.py
├── requirements.txt
└── db.sqlite3            # Database (created after migration)
```

## Color Scheme

- Primary: Indigo (#6366f1)
- Secondary: Green (#10b981)
- Accent: Amber (#f59e0b)
- Dark Background: Slate (#1e293b)

## Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Notes

- All images are stored in the `media/` directory
- Static files are collected to `staticfiles/` directory
- The website is optimized for conversion and user experience
- All forms have validation and user feedback

## Support

For any issues or questions, please refer to Django documentation or contact support.

# worklinksolution
