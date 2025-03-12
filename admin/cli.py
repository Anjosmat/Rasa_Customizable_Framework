import click
from database.db_config import Session, init_db
from admin.models import AdminUser


@click.group()
def admin_cli():
    """Admin management commands"""
    pass


@admin_cli.command()
@click.option('--username', prompt='Admin username', help='Username for the admin account')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
              help='Password for the admin account')
def create_admin(username, password):
    """Create a new admin user"""
    init_db()
    session = Session()
    try:
        # Check if admin already exists
        existing_admin = session.query(AdminUser).filter_by(username=username).first()
        if existing_admin:
            click.echo(f"Admin user '{username}' already exists!")
            return

        # Create new admin user
        admin = AdminUser(username=username, is_admin=True)
        admin.set_password(password)
        session.add(admin)
        session.commit()
        click.echo(f"Admin user '{username}' created successfully!")
    except Exception as e:
        click.echo(f"Error creating admin user: {str(e)}")
        session.rollback()
    finally:
        session.close()


@admin_cli.command()
def list_admins():
    """List all admin users"""
    init_db()
    session = Session()
    try:
        admins = session.query(AdminUser).all()
        if not admins:
            click.echo("No admin users found.")
            return

        click.echo("Admin users:")
        for admin in admins:
            click.echo(f"- {admin.username} (ID: {admin.id})")
    finally:
        session.close()


if __name__ == '__main__':
    admin_cli()
