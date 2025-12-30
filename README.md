# NEPSE Trade Journal

A comprehensive trading journal and portfolio management platform designed specifically for Nepali traders. Track your trades, analyze performance, manage your portfolio, and learn from educational content - all in one place.

## Features

- **Trade Journaling**: Log trades with detailed entry/exit points, emotions, and strategies
- **Portfolio Management**: Track your complete portfolio with real-time position monitoring
- **Advanced Analytics**: Visualize performance with interactive charts and comprehensive statistics
- **Learning Hub**: Access trading courses, tutorials, and educational content
- **User Management**: Secure authentication and user profiles
- **Admin Dashboard**: Comprehensive admin panel for user and trade management
- **Export Functionality**: Export trades and generate PDF reports
- **Responsive Design**: Modern UI that works on all devices

## Technology Stack

- **Backend**: Django 5.1+ (Python Web Framework)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Image Processing**: Pillow
- **PDF Generation**: ReportLab
- **Static Files**: WhiteNoise (Production)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation & Setup

### Windows Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SunilNeupane77/NepseJournal.git
   cd NepseJournal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   .venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Linux/macOS Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SunilNeupane77/NepseJournal.git
   cd NepseJournal
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## Access the Application

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Project Structure

```
NepseJournal/
├── accounts/           # User authentication and profiles
├── core/              # Main app with home, dashboard, admin features
├── journal/           # Trade journaling functionality
├── portfolio/         # Portfolio management
├── learning/          # Educational content and courses
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── media/            # User uploaded files
├── nepse_trade_journal/  # Django project settings
├── manage.py         # Django management script
├── requirements.txt  # Python dependencies
└── db.sqlite3       # SQLite database (development)
```

## Key Applications

### Core App
- Home page and landing
- User dashboard with analytics
- Admin dashboard
- Export functionality
- PDF report generation

### Accounts App
- User registration and authentication
- Custom user model
- Profile management

### Journal App
- Trade logging and management
- Strategy tracking
- Emotion analysis
- Trade performance metrics

### Portfolio App
- Portfolio overview
- Position tracking
- Balance management
- Performance analytics

### Learning App
- Course management
- Lesson content
- Educational resources

## UI Components

- **Modern Design**: Glass morphism effects and gradients
- **Responsive Layout**: Bootstrap 5 grid system
- **Interactive Charts**: Performance visualization
- **Animations**: Smooth fade-in effects
- **Icons**: Bootstrap Icons integration

## Security Features

- CSRF protection
- User authentication
- Secure password validation
- Session management
- XFrame protection

## Database Models

### User Model (Custom)
- Extended Django user with additional fields
- Profile information and preferences

### Trade Model
- Comprehensive trade tracking
- Entry/exit points, P&L calculation
- Emotion and strategy tagging

### Portfolio Model
- Portfolio balance tracking
- Position management

### Course/Lesson Models
- Educational content structure
- Progress tracking

## Deployment

### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

### Production Settings
- Use PostgreSQL for production database
- Configure static file serving
- Set up proper logging
- Enable security middleware

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Version History

- **v1.0.0** - Initial release with core functionality
- Trade journaling, portfolio management, user authentication
- Admin dashboard and analytics
- Educational content system

---

**Made for Nepali Traders**
