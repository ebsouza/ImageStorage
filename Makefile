run_migration:
# Set environment variable to make clear when migration is test or production
	-alembic revision --autogenerate -m "Creating models"
	alembic upgrade heads