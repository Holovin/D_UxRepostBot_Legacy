class Data:
    def __init__(self, filename):
        self.filename = filename

    def get(self):
        file = open(self.filename, 'r')
        data = file.readline().strip()
        file.close()
        return data

    def set(self, data):
        file = open(self.filename, 'w')
        file.write(data)
        file.close()
