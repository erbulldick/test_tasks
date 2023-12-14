class First:
    def getClassname(self):
        print("First")

    def getLetter(self):
        print("A")


class Second:
    def getClassname(self):
        print("Second")

    def getLetter(self):
        print("B")


if __name__ == '__main__':

    first = First()
    second = Second()

    first.getClassname()
    second.getClassname()

    first.getLetter()
    second.getLetter()
