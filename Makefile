run_migration_production:
	export APP_SETTINGS=production && alembic -n production revision --autogenerate -m "Creating models"
	export APP_SETTINGS=production && alembic -n production upgrade heads

run_migration_development:
	export APP_SETTINGS=development && alembic -n development revision --autogenerate -m "Creating models"
	export APP_SETTINGS=development && alembic -n development upgrade heads

run_migration_test:
	export APP_SETTINGS=testing && alembic -n test revision --autogenerate -m "Creating models"
	export APP_SETTINGS=testing && alembic -n test upgrade heads

