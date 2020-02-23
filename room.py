from threading import Timer

class Room:
    def __init__(self, questions):
        self.started = False
        self.endtimer = None
        self.users = []
        self.user_score = dict()
        self.answers = [dict()]
        self.questions = questions
        self.current_question = 0

    def next_question(self):
        if not self.is_ended():
            self.current_question += 1
            self.answers.append(dict())

    def get_current_question(self):
        return self.questions[self.current_question]

    def is_correct_answer(self):
        for u in self.users:
            self.user_score[u.id] = 0
        i = 0
        for answ in self.answers:
            for a in answ:
                if int(answ.get(a))-1 == self.questions[i].answer:
                    self.user_score[a] += 1;
            i += 1 

    def start_timer(self):
        self.endtimer = Timer(30, self.next_question)
        self.endtimer.start()

    def cancel_timer(self):
        if self.endtimer:
            self.endtimer.cancel()
            self.endtimer = None

    def is_user_player(self, user):
        for u in self.users:
            if u.id == user.id:
                return True
        return False

    def add_user(self, user):
        self.users.append(user)

    def add_user_answer(self, user, answer):
        if self.is_user_player(user):
            currentAnswers = self.answers[self.current_question]
            currentAnswers[user.id] = answer

    def is_all_answer(self):
        print(len(self.users))
        print('{}\n'.format(len(self.answers[self.current_question])))
        if len(self.users) == len(self.answers[self.current_question]):
            self.next_question()
            return True
        return False

    def start_game(self):
        self.started = True
        self.start_timer()

    def is_ended(self):
        return self.current_question >= len(self.questions)

    