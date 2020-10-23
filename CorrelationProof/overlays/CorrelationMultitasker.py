# How to use this file:
# Simply write a "predicate" function that accepts a UserTrace class and a
# QuestionnaireParser class. Access the user's questionnaire data through their ID
# (see how this is done in some samples below) and compare their questionnaire values
# (see class Questionnaire) against what you're interested in.
# Finally, in the main function, add your predicate function to the list of predicates tested.
from typing import List, Tuple

from QuestionnaireParser import QuestionnaireParser
from overlay import DataParser
from visualizeCorrelation import CorrelationVisualizer


class CorrelationMultitasker:
    thres: int
    data: DataParser
    predicates: Tuple[DataParser.Predicate]
    results: List[Tuple[float, float]]

    def __init__(self, data: DataParser, thres: int, predicates: Tuple[DataParser.Predicate]):
        self.data = data
        self.thres = thres
        self.predicates = predicates
        self.results = []

    def render(self):
        # So this WOULD be multithreaded, but...
        # Python doesn't have interpreter-level multithreading due to the GIL :(
        # I was hoping to take advantage of the 16 threads on this computer :(
        for predicate in self.predicates:
            vis = CorrelationVisualizer(self.data, self.thres, predicate)
            self.results.append(vis.render())

    def showresults(self):
        for predicate, result in zip(self.predicates, self.results):
            print(f"Predicate {predicate.__name__} gives results {result[0]}, {result[1]}")


def predicate_base(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return True


def predicate_male(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].gender == "Male"


def predicate_female(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].gender == "Female"


def predicate_experience_with_mobile_vr(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].mobilevr > 2


def predicate_experience_with_room_vr(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].roomvr > 2


def predicate_experience_with_360video(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].vrvideo > 2


def predicate_older_than_25(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].age > 25


def predicate_younger_than_25(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].age < 25


def predicate_inexperienced(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].mobilevr < 2 and q.participants[trace[0]].roomvr < 2 and \
        q.participants[trace[0]].vrvideo < 2


def main():
    data = DataParser(12, "C:/Users/qwe/Documents/vr-viewport-analysis")
    data.generatedata()
    threshold = 250

    predicates_used = (predicate_base, predicate_male, predicate_female, predicate_experience_with_mobile_vr,
                       predicate_experience_with_room_vr, predicate_experience_with_360video,
                       predicate_older_than_25, predicate_younger_than_25, predicate_inexperienced)

    # PyCharm makes a mistake when type checking predicates_used here
    # noinspection PyTypeChecker
    multitasker = CorrelationMultitasker(data, threshold, predicates_used)
    multitasker.render()
    multitasker.showresults()


if __name__ == "__main__":
    main()
