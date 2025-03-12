# database/migrate.py
from alembic import command
from alembic.config import Config
import os


def run_migrations():
    # Get the project's root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Create Alembic configuration, assuming your alembic.ini is at the project's root
    alembic_cfg = Config(os.path.join(project_root, 'alembic.ini'))
    alembic_cfg.set_main_option('script_location', os.path.join(project_root, 'database', 'migrations'))

    # Run migrations
    command.upgrade(alembic_cfg, 'head')


if __name__ == '__main__':
    run_migrations()
