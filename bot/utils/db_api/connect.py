from orator import DatabaseManager, Schema, Model
from data.config import DATABASES

db = DatabaseManager(DATABASES)
schema = Schema(db)
Model.set_connection_resolver(db)