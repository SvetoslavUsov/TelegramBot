@staticmethod
def proverka_bylevo(self):
    with open("bylevo.txt", "r") as f:
        a = f.read()
        if a == "True":
            return True
        else:
            return False