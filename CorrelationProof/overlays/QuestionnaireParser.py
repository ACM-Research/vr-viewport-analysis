from tkinter import filedialog, messagebox
from typing import Dict
import pandas as pd
from pandas import DataFrame


class Questionnaire:
    studyid: str
    gender: str
    age: int
    # These values are based on "experience levels" from 0 (no exp.) up
    mobilevr: int
    roomvr: int
    vrvideo: int

    def __init__(self, studyid: str, gender: str, age: int, mobilevr: int, roomvr: int,
                 vrvideo: int):
        self.studyid = studyid
        self.gender = gender
        self.age = age
        self.mobilevr = self.explevel(mobilevr)
        self.roomvr = self.explevel(roomvr)
        self.vrvideo = self.explevel(vrvideo)

    @staticmethod
    def explevel(count: int) -> int:
        level = 1 if count >= 1 else 0
        level = 2 if count >= 5 else level
        level = 3 if count >= 10 else level
        level = 4 if count >= 20 else level
        level = 5 if count >= 50 else level
        return level


class QuestionnaireParser:
    participants: Dict[str, Questionnaire]
    sheet: DataFrame

    def __init__(self, filepath: str = None):
        self.participants = {}
        self.loadsheet(filepath)
        self.parse()

    def loadsheet(self, filepath=None):
        if filepath is None:
            file = filedialog.askopenfile(mode='rb', title='Choose a file')
            if file is None:
                messagebox.showerror("File error!", "Error: No file selected.")
                exit(-1)
            filepath = file.name
            # We, uh, don't actually need this file handle. Just its path.
            file.close()
        self.sheet = pd.read_csv(filepath)

    @staticmethod
    def stripthings(value: str) -> int:
        # Strip string of "occasion[s]"
        value = value[: value.find(" ")]
        # Pick first number if two are given
        if '-' in value:
            value = value[: value.find('-')]
        # Strip MORE stuff
        if '+' in value:
            value = value[: value.find('+')]
        return int(value)

    def parse(self):
        # print(self.sheet.head(0))
        for row in self.sheet.iterrows():
            row = row[1].values  # Ditch the extras
            studyid = row[0]
            gender = row[1]
            age = row[2]
            # And it stays 0 if they've never done it
            mobilevr = 0
            if "Yes" in row[3]:
                mobilevr = self.stripthings(row[4])
            # Ditto for the following
            roomvr = 0
            if "Yes" in row[5]:
                roomvr = self.stripthings(row[6])
            vrvideo = 0
            if "Yes" in row[7]:
                vrvideo = self.stripthings(row[8])

            self.participants[studyid] = Questionnaire(
                studyid, gender, age, mobilevr, roomvr, vrvideo
            )


if __name__ == "__main__":
    q = QuestionnaireParser\
        (r"C:\Users\qwe\Documents\vr-viewport-analysis\Experiment Data\Questionnaires\BackgroundQuestionnaire.csv")
    print(q.participants["BGQZ3M"].mobilevr)
