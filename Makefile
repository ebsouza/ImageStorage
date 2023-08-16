run_migration:
	rm migrations/versions/*.py
	alembic revision --autogenerate -m "Creating models"
	alembic upgrade heads

run_migration_test:
	rm migrations/versions/*.py
	export APP_SETTINGS=testing && alembic revision --autogenerate -m "Creating models"
	alembic upgrade heads

