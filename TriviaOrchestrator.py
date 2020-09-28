from TriviaServices import TriviaServices
from TriviaSheets import TriviaSheets
from TriviaSlides import TriviaSlides
from TriviaRound import TriviaRound, TriviaRoundType
from tqdm import tqdm

class TriviaOrchestrator(object):
    def __init__(self, slides_presentation_id = None):
        self.slides_presentation_id = slides_presentation_id
        self.triviaSheets = TriviaSheets()
        self.triviaSlides = TriviaSlides(slides_presentation_id)

    def create_presentation_from_sheet(self, spreadsheet_id, spreadsheet_tab):
        title, author, round_number_to_round = self.get_title_author_roundNumberToRound(spreadsheet_id, spreadsheet_tab)
        
        self.triviaSlides.create_presentation(title)
        self.triviaSlides.create_slide_with_title_and_subtitle(title, author)
        self.triviaSlides.create_summary_slide(round_number_to_round)

        for round in tqdm(round_number_to_round.values(), desc="Creating rounds"):
            round.create_slides()

    def get_title_author_roundNumberToRound(self, spreadsheet_id, spreadsheet_tab):
        rows = self.triviaSheets.get_rows(spreadsheet_id, spreadsheet_tab)
        round_number_to_round = dict()

        current_round = None
        title, author = tuple(rows[0])
        headers = rows[1] # is ignored  

        for row in rows[2:]:
            n = len(row) 
            if n == 2 or n == 3: current_round = self.title_logic(round_number_to_round, row) 
            elif n == 4: self.question_logic(round_number_to_round, row, current_round) 
        
        return title, author, round_number_to_round

    def title_logic(self, round_number_to_round, row):
        round_type_and_number, round_title = row[0], row[1]
        round_number = TriviaRound.get_round_number(round_type_and_number) 
        round_summary = row[2] if len(row) > 2 else None

        round = TriviaRound.create_round(round_type_and_number, round_title, self.triviaSlides, round_summary)
        round_number_to_round[round_number] = round
        return round_number

    def question_logic(self, round_number_to_round, row, round_number):
        question_number, question, answer, points = tuple(row)
        round = round_number_to_round[round_number]
        round.add_question_and_answer(question_number, question, answer, points)



    

    

    