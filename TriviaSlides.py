import random
from TriviaServices import TriviaServices

# Reference: https://github.com/googleworkspace/python-samples/blob/master/slides/snippets/slides_snippets.py

BULLET_THRESHOLD = 10

# https://developers.google.com/slides/samples/slides#create_a_new_slide_and_modify_placeholders
# predefinedLayouts
TITLE = "TITLE"
TITLE_AND_BODY = "TITLE_AND_BODY"

# type of placeholder
TITLE = "TITLE"
BODY = "BODY"
CENTERED_TITLE = "CENTERED_TITLE"
SUBTITLE = "SUBTITLE"

class TriviaSlides(object):

    #include presentation_if you want to edit a presentation. Otherwise, make sure to create_presentation before you do anything else!
    def __init__(self, presentation_id = None):
        triviaServices = TriviaServices()
        self.service = triviaServices.get_slides_service()
        self.presentation_id = presentation_id 
    
    def create_presentation(self, title):
        slides_service = self.service
        body = {
            'title': title
        }
        # pylint: disable=maybe-no-member
        presentation = slides_service.presentations() \
            .create(body=body).execute()
        self.presentation_id = presentation.get('presentationId') # update if creating a new presentation
        print(f'Created presentation with ID: {self.presentation_id}')
        
        return presentation

    def create_summary_slide(self, round_number_to_round):
        rounds = []
        total_points = 0
        round_numbers = sorted(round_number_to_round.keys(), key = lambda x: int(x))
        for i in round_numbers:
            round = round_number_to_round[i]
            title = round.round_title
            points = round.get_total_points()
            total_points += points
            rounds.append(title + f" ({points} points)" )
        self.create_slide_with_bullets(f"Summary of Rounds ({total_points} points)", rounds)

    # create individual slide methods 
    def create_slide_with_title_and_body(self, title_text, body_text):
        return self.create_slide_with_predefinedLayout(title_text, body_text, TITLE_AND_BODY)

    def create_slide_with_title_and_subtitle(self, title_text, subtitle_text):
        return self.create_slide_with_predefinedLayout(title_text, subtitle_text, TITLE)
    
    # bullets is a list of bullet points
    def create_slide_with_bullets(self, title_text, bullets):
        n = len(bullets)
        should_be_split_in_half = n > BULLET_THRESHOLD

        slides_service = self.service
        pageId, title_title_id, _ = self.get_pageId_titleTitleId_bodyTitleId()
        body_title_ids = [f"{pageId}_title_{i}" for i in range(2)]
        
        if should_be_split_in_half: slide_request = self.request_create_slide_with_two_columns(pageId, title_title_id, body_title_ids)
        else: slide_request = self.request_create_slide_with_title_and_body(pageId, title_title_id, body_title_ids[0])

        title_request = self.request_insert_text(title_title_id, title_text)
        body_request = self.get_request_body_for_bulleted_items(bullets, body_title_ids)

        requests = [slide_request, title_request, body_request]
        body = {
            "requests": requests
        }

        response = self.create_slide_batch_update(body)
        return response

    def create_slide_with_predefinedLayout(self, title, body, predefinedLayout):
        slides_service = self.service
        pageId, title_title_id, body_title_id,  = self.get_pageId_titleTitleId_bodyTitleId()

        slide_request = self.request_create_slide_with_predefinedLayout(pageId, title_title_id, body_title_id, predefinedLayout)
        title_request = self.request_insert_text(title_title_id, title)
        body_request = self.request_insert_text(body_title_id, body) 
        requests = [slide_request, title_request, body_request]

        body = {
            "requests": requests
        }

        response = self.create_slide_batch_update(body)
        return response

    # create methods 
    def create_slide_batch_update(self, body):
        slides_service = self.service
        # pylint: disable=maybe-no-member
        response = slides_service.presentations() \
            .batchUpdate(presentationId=self.presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        # print('Created slide with ID: {0}'.format(
            # create_slide_response.get('objectId')))
        return response

    # request methods 

    def request_insert_text(self, title_id, text):
        return \
        {
            "insertText": {
                "objectId": title_id,
                "text": text,
            }
        }

    def request_create_slide_with_title_and_body(self, pageId, title_title_id, body_title_id):
        return self.request_create_slide_with_predefinedLayout(pageId, title_title_id, body_title_id, TITLE_AND_BODY)

    def request_create_slide_with_title_and_subtitle(self, pageId, title_title_id, subtitle_title_id):
        return self.request_create_slide_with_predefinedLayout(pageId, title_title_id, subtitle_title_id, TITLE)

    def request_create_slide_with_predefinedLayout(self, pageId, title_title_id, body_title_id, predefinedLayout):
        if predefinedLayout == TITLE_AND_BODY:
            primary_type, secondary_type = TITLE, BODY
        elif predefinedLayout == TITLE:
            primary_type, secondary_type = CENTERED_TITLE, SUBTITLE
        
        return \
        {
            "createSlide": {
                "objectId": pageId,
                "slideLayoutReference": {
                "predefinedLayout": predefinedLayout
                },
                "placeholderIdMappings": [
                    {
                        "layoutPlaceholder": {
                        "type": primary_type,
                        "index": 0
                        },
                        "objectId": title_title_id,
                    },

                    {
                        "layoutPlaceholder": {
                        "type": secondary_type,
                        "index": 0
                        },
                        "objectId": body_title_id,
                    }
                ]
            }
        }

    # body_title_ids is a list with 2 elements 
    def request_create_slide_with_two_columns(self, pageId, title_title_id, body_title_ids):
        return \
        {
            "createSlide": {
                "objectId": pageId,
                "slideLayoutReference": {
                "predefinedLayout": "TITLE_AND_TWO_COLUMNS"
                },
                "placeholderIdMappings": [
                    {
                        "layoutPlaceholder": {
                        "type": "TITLE",
                        "index": 0
                        },
                        "objectId": title_title_id,
                    },

                    {
                        "layoutPlaceholder": {
                        "type": "BODY",
                        "index": 0
                        },
                        "objectId": body_title_ids[0],
                    }, 

                    {
                        "layoutPlaceholder": {
                        "type": "BODY",
                        "index": 1
                        },
                        "objectId": body_title_ids[1],
                    }
                ]
            }
        }

    def request_insert_text_with_bullets(self, title_id):
        return \
        {
            "createParagraphBullets": {
                "objectId": title_id,
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                "textRange": {
                    "type": "ALL"
                }
            }
        }

    # get helper methods
    def get_list_str(self, text, start):
        index = start
        text_str = ""
        for txt in text:
            text_str += f"{index}. {txt}\n"
            index += 1
        return text_str[:-1]

    def get_request_body_for_bulleted_items(self, bullets, body_title_ids):
        n = len(bullets)
        half = n//2
        if n > BULLET_THRESHOLD: new_bullets = [bullets[:half], bullets[half:]] 
        else: new_bullets = [bullets]

        requests = []
        # length of body_title_ids should be at most 2 (corresponding to at most 2 columns)
        for i, (bullet_list, column_id) in enumerate(zip(new_bullets, body_title_ids)):
            start = 1 if i == 0 else half + 1
            body =  self.get_list_str(bullet_list, start)
            body_request = self.request_insert_text(column_id, body)
            body_bullet_request = self.request_insert_text_with_bullets(column_id)
            requests.append(body_request)
            requests.append(body_bullet_request)
        return requests

    def get_pageId_titleTitleId_bodyTitleId(self):
        pageId = str(random.randint(10**7, 10**8))
        title_title_id = pageId + "_title"
        body_title_id = pageId + "_body"
        return pageId, title_title_id, body_title_id