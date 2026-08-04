import urllib.parse
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import create_engine
from alembic import context

# Import your application's models and base
from app.db.base import Base
from app.config import settings
from app.models import career_path
from app.models import data_source
from app.models import forecast
from app.models import market_data_points
from app.models import market_signal
from app.models import trend_alert
from app.models import user_profile
from app.models import user


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- DYNAMIC DATABASE URL CONFIGURATION ---
# Read from settings.DATABASE_URL and encode the password if needed.
raw_url = settings.DATABASE_URL
if "://" in raw_url:
    scheme, rest = raw_url.split("://", 1)
    if "@" in rest:
        user_pass, host_db = rest.rsplit("@", 1)
        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
            # Unquote first to prevent double encoding, then quote
            decoded_password = urllib.parse.unquote(password)
            quoted_password = urllib.parse.quote_plus(decoded_password)
            db_url = f"{scheme}://{user}:{quoted_password}@{host_db}"
        else:
            db_url = raw_url
    else:
        db_url = raw_url
else:
    db_url = raw_url

# Force Alembic to use this URL, escaping the '%' symbol for configparser with '%%'
config.set_main_option("sqlalchemy.url", db_url.replace('%', '%%'))
# ------------------------------------------



# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # ...
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    print("Running in offline mode is not supported in this configuration.")
else:
    run_migrations_online()