from orator.migrations import Migration


class CreatePaymentsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('payments') as table:
            table.increments('id')
            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users').on_delete('cascade')
            table.text('comment')
            table.decimal('amount')
            table.text('provider').default('qiwi')
            table.boolean('success').default(False)           
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('payments')
