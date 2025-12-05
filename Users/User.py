class User:

    def __init__(self, first_name, last_name, username=None):
        self.fname = first_name
        self.lname = last_name
        self.score = 0
        if username is not None:
            self.username = username
        else:
            self.username = self.fname[0] + self.lname[1:]

    # Should these be @classmethod?
    def login(self):
        pass

    def logout(self):
        pass

    def save_to_leaderboard(self):
        pass