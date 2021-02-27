from orator.migrations import Migration


class CreateItemsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('items') as table:
            table.increments('id')
            table.integer('position_id').unsigned()
            table.foreign('position_id').references('id').on('positions').on_delete('cascade')
            table.text('body')
            table.boolean('reusable').default(False)
            table.boolean('is_file').default(False)
            table.boolean('buy').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('items')
