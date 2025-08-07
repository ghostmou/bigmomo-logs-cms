# BigMomo Logs CMS

A comprehensive Content Management System for managing server logs sources, destinations in BigQuery, and ETL pipelines to transfer logs from sources to BigQuery.

## Features

### 🔐 Authentication & Authorization
- **Role-based access control**: Admin and Editor users with distinct permissions
- **User management**: Create, edit, block/unblock users
- **Password policies**: Force password change on first login
- **Secure authentication**: Custom login with status validation

### 🏢 Client Management
- **Organizational hierarchy**: Clients → Projects structure
- **CRUD operations**: Create, read, update, delete clients
- **Expandable view**: Google Cloud-style client/project tree view
- **Search functionality**: Find clients quickly

### 📁 Project Management
- **Project configuration**: Set up log sources, filters, and schedules
- **FTP/SFTP support**: Configure server log sources
- **File filtering**: Multiple filter types (starts with, contains, regex)
- **Cron scheduling**: Configure log synchronization frequency
- **Visual status indicators**: See configuration completeness at a glance

### 👥 User Management (Admin Only)
- **User administration**: Centralized user management panel
- **Random password generation**: Secure temporary passwords
- **User blocking**: Prevent access for blocked users
- **Password reset**: Admin can reset user passwords
- **Role assignment**: Set users as admin or editor

## Technology Stack

- **Backend**: Django 5.2.5 with Python 3.12
- **Database**: SQLite (configurable for production)
- **Frontend**: Bootstrap 5 with responsive design
- **Forms**: Django Crispy Forms with Bootstrap 5 styling
- **Dependency Management**: uv (modern Python package manager)
- **Icons**: Bootstrap Icons

## Installation

### Prerequisites
- Python 3.12+
- uv package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bigmomo-logs-cms
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run migrations**
   ```bash
   source .venv/bin/activate
   python manage.py migrate
   ```

4. **Create initial admin user**
   ```bash
   python manage.py create_admin
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - URL: http://localhost:8000
   - Login with: `admin` / `admin`
   - **Important**: Change the password on first login

## Project Structure

```
bigmomo-logs-cms/
├── accounts/                 # User authentication & management
│   ├── models.py            # Custom User model
│   ├── views.py             # Authentication views
│   ├── forms.py             # User forms
│   └── management/          # Management commands
├── clients/                 # Client management
│   ├── models.py            # Client model
│   ├── views.py             # Client CRUD views
│   └── forms.py             # Client forms
├── projects/                # Project & ETL configuration
│   ├── models.py            # Project, LogSource, FileFilter, Schedule
│   ├── views.py             # Project management views
│   └── forms.py             # Configuration forms
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Authentication templates
│   ├── clients/             # Client templates
│   └── projects/            # Project templates
└── static/                  # Static files (CSS, JS)
```

## Usage

### For Admin Users

1. **User Management**
   - Navigate to "Users" in the main menu
   - Create new users with random passwords
   - Set user roles (Admin/Editor)
   - Block/unblock users as needed
   - Reset user passwords

2. **Client Management**
   - Create organizational clients
   - View clients with expandable project lists
   - Edit client information

3. **Project Management**
   - Create projects linked to clients
   - Configure log sources (FTP/SFTP)
   - Set up file filters and schedules
   - Monitor project configuration status

### For Editor Users

1. **Client Management**
   - Create and manage clients
   - View client projects

2. **Project Management**
   - Create and configure projects
   - Set up ETL configurations
   - Monitor project status

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration

The application uses SQLite by default. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Security Features

- **Custom User Model**: Extended with role and status fields
- **Password Policies**: Force password change on first login
- **User Blocking**: Prevent access for blocked users
- **Role-based Permissions**: Admin vs Editor access control
- **CSRF Protection**: Built-in Django CSRF protection
- **Secure Forms**: Django Crispy Forms with Bootstrap styling

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

## Future Enhancements

### Phase 5: ETL Integration
- BigQuery connection setup
- ETL job orchestration system
- Log transfer mechanisms for FTP/SFTP
- Job monitoring and status tracking

### Phase 6: Advanced Features
- API endpoints for external integrations
- Logging and monitoring
- Backup and recovery systems
- Performance optimization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.
