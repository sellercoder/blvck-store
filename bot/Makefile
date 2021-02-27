db_migrate:
	orator migrate -c data/config.py -p utils/db_api/migrations -f

db_rollback:
	orator migrate:rollback -c data/config.py -p utils/db_api/migrations -f

db_rm_users:
	orator db:seed -c data/config.py -p utils/db_api/seeds -f -q --seeder=cleaner_seeder

db_rm_transactions:
	orator db:seed -c data/config.py -p utils/db_api/seeds -f -q --seeder=clean_transactions_seeder

demo_store:
	orator db:seed -c data/config.py -p utils/db_api/seeds -f -q --seeder=demo_store_seeder
