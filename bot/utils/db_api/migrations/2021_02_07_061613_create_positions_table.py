from orator.migrations import Migration


class CreatePositionsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('positions') as table:
            table.increments('id')
            table.integer('category_id').unsigned()
            table.foreign('category_id').references('id').on('categories').on_delete('cascade')
            table.text('name')
            table.text('description').default("Описание позиции")
            table.float('price').default(99)
            table.boolean('reusable').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('positions')
