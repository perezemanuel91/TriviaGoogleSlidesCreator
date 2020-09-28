import enum
from TriviaSlides import TriviaSlides

SPACE = " "
ANSWER = "ANSWER"
FILLER_SLIDE_TEXT =  "AND THE ANSWER IS..."

class TriviaRoundType(enum.Enum):
    Regular = 1
    Bullet = 2
    Hybrid = 3 # not used
    Pictures = 4 # not used

class TriviaRound(object):
    def __init__(self, round_type_and_number, round_title, slides_service, round_summary):
        round_type = TriviaRound.get_round_type(round_type_and_number)
        round_number = TriviaRound.get_round_number(round_type_and_number)

        self.round_type = round_type
        self.round_title = round_title
        self.round_number = round_number
        self.triviaSlides = slides_service
        self.round_summary = round_summary

        self.total_points = 0
        self.questions = dict()
        self.points = dict()
        self.answers = dict()

    def __str__(self):
        newline = "\n"
        round = f"Round {self.round_number}: {self.round_title} [{self.round_type}]" + newline
        question_numbers = self.get_question_numbers()
        for i in range(question_numbers):
            round += str([i, (self.questions[i], self.answers[i], self.points[i])]) + newline
        return round
    
    # main methods
    def add_question_and_answer(self, question_number, question, answer, points):
        self.questions[question_number] = question
        self.answers[question_number] = answer
        self.points[question_number] = points
        self.total_points += int(points)

    def create_slides(self):
        self.create_round_slide()
        question_numbers = self.get_question_numbers()  
         
        for i in question_numbers:
            title_text = self.get_title_for_question(i)
            question, answer = self.questions[i], self.answers[i]

            self.triviaSlides.create_slide_with_title_and_body(title_text, question)
            self.triviaSlides.create_slide_with_title_and_body(title_text, FILLER_SLIDE_TEXT)
            self.triviaSlides.create_slide_with_title_and_body(title_text + ANSWER, answer) 

    def create_round_slide(self):
        title_text = self.get_title_for_round()
        body_text = self.round_summary 
        self.triviaSlides.create_slide_with_title_and_body(title_text, body_text)

    # get methods 
    def get_title_for_round(self):
        return f"Round {self.round_number}: {self.round_title} ({self.total_points} points) " 

    def get_title_for_question(self, question_number):
        question_number, points = question_number, self.points[question_number]
        return f"R{self.round_number}: {self.round_title}, Q{question_number} ({points} points) " 

    def get_question_numbers(self):
        return sorted(self.questions.keys(), key = lambda x: int(x))     
    
    def get_total_points(self):
        return self.total_points
    
    # static methods
    @staticmethod
    def get_round_type(round_type_and_number):
        if "R" in round_type_and_number: return TriviaRoundType.Regular
        if "H" in round_type_and_number: return TriviaRoundType.Hybrid
        if "P" in round_type_and_number: return TriviaRoundType.Pictures
        if "B" in round_type_and_number: return TriviaRoundType.Bullet 

    @staticmethod
    def get_round_number(round_type_and_number):
        return int(round_type_and_number[1:])

    @staticmethod 
    def create_round(round_type_and_number, round_title, slides_service, round_summary):
        round_type = TriviaRound.get_round_type(round_type_and_number)

        if round_type == TriviaRoundType.Bullet:
            return BulletRound(round_type_and_number, round_title, slides_service, round_summary)
        else:
            return TriviaRound(round_type_and_number, round_title, slides_service, round_summary)

class BulletRound(TriviaRound):
    def __init__(self, round_type_and_number, round_title, slides_service, round_summary):
        super(BulletRound, self).__init__(round_type_and_number, round_title, slides_service, round_summary)

    def create_slides(self):
        self.create_round_slide()
    
        question_numbers = self.get_question_numbers()
        title_text = self.get_title_for_round()
        questions = [self.questions[i] for i in question_numbers]
        answers = [self.answers[i] for i in question_numbers]

        self.triviaSlides.create_slide_with_bullets(title_text, questions)
        self.triviaSlides.create_slide_with_title_and_body(title_text, FILLER_SLIDE_TEXT)
        self.triviaSlides.create_slide_with_bullets(title_text + ANSWER, answers)  

