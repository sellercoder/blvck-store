from orator.migrations import Migration
import json
dt = dict(users=[])
jsn = json.dumps(dt)

class CreateCouponsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('coupons') as table:
            table.increments('id')
            table.text('uid').unique()
            table.decimal('amount')
            table.json('activators').default(jsn)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('coupons')
