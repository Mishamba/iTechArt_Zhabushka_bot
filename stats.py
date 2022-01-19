import pickle

class User:
    def __init__(self, name):
        self.name = name
        self.frogCount = 0

class Stats:
    def __init__(self, file_path):
        self.record = 0
        self.overall = 0
        self.users = dict()
        self.file_path = file_path
    def getUserById(self, id):
        if str(id) in self.users:
            return self.users[str(id)]
        else:
            return None
    def load(self):
        with open(self.file_path, 'rb') as f:
            loadedObj = pickle.load(f)
            self.record = loadedObj.record
            self.users = loadedObj.users
            self.overall = loadedObj.overall
            print(self.record)
    def save(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self, f)