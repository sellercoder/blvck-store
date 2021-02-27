from orator.migrations import Migration


class AddUsernameToUsers(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('users') as table:
            table.text('username').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('users') as table:
            pass
