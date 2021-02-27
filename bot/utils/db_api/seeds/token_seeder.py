from orator.seeds import Seeder


class TokenSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('tokens').insert([
            {'token': '73df375618da54c71f2ab6ed75182bf3', 'phone': '+7247991989'}
            ])









