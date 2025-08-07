from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates the initial admin user with username "admin" and password "admin"'
    
    def handle(self, *args, **options):
        try:
            # Check if admin user already exists
            if User.objects.filter(username='admin').exists():
                self.stdout.write(
                    self.style.WARNING('Admin user already exists. Skipping creation.')
                )
                return
            
            # Create admin user
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@bigmomo.com',
                password='admin',
                first_name='Admin',
                last_name='User',
                role='admin',
                status='active',
                is_staff=True,
                is_superuser=True,
                is_password_changed=False
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin user:\n'
                    f'Username: admin\n'
                    f'Password: admin\n'
                    f'Email: {admin_user.email}\n'
                    f'Role: {admin_user.get_role_display()}\n'
                    f'Status: {admin_user.get_status_display()}'
                )
            )
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )
