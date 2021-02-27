from orator.migrations import Migration


class CreateTokensTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('tokens') as table:
            table.increments('id')
            table.text('token')
            table.text('phone')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('tokens')
