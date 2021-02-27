from orator.migrations import Migration


class CreateBillsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('bills') as table:
            table.increments('id')
            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users').on_delete('cascade')
            table.text('currency').default('KZT')
            table.decimal('value')
            table.text('phone')
            table.text('status')
            table.text('email')
            table.text('pay_url')
            table.text('comment').deafult('Оплата в магазине')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('bills')
