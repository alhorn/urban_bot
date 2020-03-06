from threading import Timer
import time
import config



def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t

class Room:
    def __init__(self, questions, update_handler):
        self.started = False
        self.users = []
        self.user_score = dict()
        self.answers = [dict()]
        self.questions = questions
        self.current_question = 0
        self.on_update_handler = update_handler
        self.timestamp_end = None
        self.update_time = None
        # camelCase PascalCase kebab-case snake_case

        def on_tick():
            current_time = time.time()
            if self.timestamp_end and self.timestamp_end <= current_time:
                if not self.is_ended():
                    self.next_question()
                    self.on_update_handler(self)
            else:
                if not self.update_time:
                    self.update_time = current_time + 10
                if current_time >= self.update_time and not self.is_ended():
                    self.on_update_handler(self)
                    self.update_time = current_time + 10

        self.one_second_timer = set_interval(on_tick, 1)


    def time_left(self):
        if self.timestamp_end:
            return self.timestamp_end - time.time()
        else:
            return 0

    def next_question(self):
        if not self.is_ended():
            self.current_question += 1
            self.answers.append(dict())
            self.timestamp_end = time.time() + config.QUESTION_TIME
        
    def get_current_question(self):
        return self.questions[self.current_question]

    def is_current_answer_correct(self, user):
        if int(self.questions[self.current_question].answer) == int(self.answers[self.current_question].get(user.id))-1:
            return True
        else: 
            return False

    def is_correct_answer(self):
        for u in self.users:
            self.user_score[u.id] = 0
        i = 0
        for answ in self.answers:
            for a in answ:
                if int(answ.get(a))-1 == self.questions[i].answer:
                    self.user_score[a] += 1
            i += 1
            if i == config.question_number:
                break 

    def start_timer(self):
        self.timestamp_end = time.time() + config.QUESTION_TIME

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
        if len(self.users) == len(self.answers[self.current_question]):
            self.timestamp_end = time.time() + 1

    def start_game(self):
        self.started = True
        self.start_timer()

    def is_ended(self):
        return self.current_question >= len(self.questions)

    