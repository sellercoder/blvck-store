from orator.migrations import Migration


class CreatePurchasesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('purchases') as table:
            table.increments('id')
            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users').on_delete('cascade')
            table.json('item')
            table.boolean('is_file').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('purchases')
