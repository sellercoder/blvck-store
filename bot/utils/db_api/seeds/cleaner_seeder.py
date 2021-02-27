from orator.seeds import Seeder


class CleanerSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('users').delete()


