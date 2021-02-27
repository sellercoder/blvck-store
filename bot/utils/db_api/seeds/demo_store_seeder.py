from orator.seeds import Seeder


class DemoStoreSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('categories').delete()
        self.db.table('categories').insert([
            {'id': 100, 'name': '🤖 Боты и парсеры', 'description': 'Крутые боты для телеги и различные парсеры сайтов.'},
            {'id': 200, 'name': '🐠 Cайты ', 'description': 'Качественные аналоги известных сайтов для сбора логинов и паролей.'},
            {'id': 300, 'name': '📒 Курсы и схемы', 'description': 'Полезные курсы по различным областям и схемы заработка в сети.'}
            ])
        self.db.table('positions').delete()
        self.db.table('positions').insert([
            {'id': 1000,'category_id': 100,'name': 'Бот автопродаж','description': 'Продажи в телеге - легко!','price': 3999 },
            {'id': 2000,'category_id': 100,'name': 'Парсер авито','description': 'Удобный авито парсер','price': 999 },
            {'id': 3000,'category_id': 200,'name': 'Клон Hydra','description': 'Крутой клон трехглавой','price': 5999 },
            {'id': 4000,'category_id': 200,'name': 'TikTok Фиш','description': 'Страница логина в тт. Собирает логи и отправляет в телеграм','price': 199 },
            {'id': 5000,'category_id': 300,'name': 'Успешный успех','description': 'Как заработать кучу денег и купить тачку или ифоцыгане и места их обитания','price': 1000000 }
        ])

        self.db.table('items').delete()










