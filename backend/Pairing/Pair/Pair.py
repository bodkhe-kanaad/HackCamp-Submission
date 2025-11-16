
class Pair(tuple):
    # constructor; returns tuple of 2 users; sets streak to 0; assigns a question to the pair
    def __init__(self, user1: User, user2: User, streak: int = 0):
        if not isinstance(user1, User) or not isinstance(user2, User):
            raise TypeError("Both elements must be User instances")
        if not isinstance(question_of_the_day, Task):
            raise TypeError("question_of_the_day must be a Task instance")
        if not isinstance(streak, int):
            raise TypeError("streak must be an integer")

        self.user1 = user1
        self.user2 = user2
        self.question_of_the_day = generateTask();
        self.streak = streak


    @property
    def user1(self):
        return self[0]

    @property
    def user2(self):
        return self[1]

    def __repr__(self):
        return f"Pair({self.user1}, {self.user2})"
    






