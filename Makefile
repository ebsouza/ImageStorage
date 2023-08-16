run_migration:
	-alembic revision --autogenerate -m "Creating models"
	alembic upgrade heads

run_migration_test:
	export APP_SETTINGS=testing && alembic revision --autogenerate -m "Creating models"
	alembic upgrade heads

