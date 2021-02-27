from orator.migrations import Migration


class CreatePagesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('pages') as table:
            table.increments('id')
            table.enum('types', ['hello', 'catalog', 'about'])
            table.text('body')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('pages')
