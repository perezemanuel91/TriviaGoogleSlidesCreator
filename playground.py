from TriviaOrchestrator import TriviaOrchestrator
import argparse 

if __name__ == '__main__':
    sample_spreadsheet_id = "12nghSvz4o_SzHWEF-XykQ4sAzZ1ofR8vR6RArQhV_M0"
    sample_spreadsheet_tab = "Sheet1" 
    parser = argparse.ArgumentParser(description='Create your trivia Google slides presentation')
    parser.add_argument("spreadsheet_id", nargs='?',  default = sample_spreadsheet_id)
    parser.add_argument("spreadsheet_tab", nargs='?', default = sample_spreadsheet_tab )
    
    args = parser.parse_args()
    spreadsheet_id = args.spreadsheet_id
    spreadsheet_tab = args.spreadsheet_tab

    triviaOrchestrator = TriviaOrchestrator()
    triviaOrchestrator.create_presentation_from_sheet(spreadsheet_id, spreadsheet_tab)
    

    print("Done!")    