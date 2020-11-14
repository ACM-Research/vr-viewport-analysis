# How to use this file:
# Simply write a "predicate" function that accepts a UserTrace class and a
# QuestionnaireParser class. Access the user's questionnaire data through their ID
# (see how this is done in some samples below) and compare their questionnaire values
# (see class Questionnaire) against what you're interested in.
# Finally, in the go function, add your predicate function to the list of predicates tested.
from multiprocessing import Pool
from typing import List, Tuple

from QuestionnaireParser import QuestionnaireParser
from overlay import DataParser
from visualizeCorrelation import CorrelationVisualizer


class CorrelationMultitasker:
    thres: int
    data: DataParser
    predicates: Tuple[DataParser.Predicate]
    results: List[Tuple[float, float]]

    def __init__(self, data: DataParser, thres: int, predicates: Tuple[DataParser.Predicate], delay: int):
        self.data = data
        self.thres = thres
        self.predicates = predicates
        self.results = []
        self.delay = delay

        # self.fileheader = "Video ID, "

    def render(self):
        for predicate in self.predicates:
            vis = CorrelationVisualizer(self.data, self.thres, predicate, self.delay)
            if vis.ok:
                self.results.append(vis.render())
            else:
                # Dummy results for no predicate results (see Visualizer constructor)
                self.results.append((0, 0))

    def showresults(self):
        """Note that the list of predicates MUST have predicate_base first so that a baseline
        can be established. Otherwise this will crash with a div by 0."""
        basecorrelation = 0
        print(f"Results for video {self.data.vidid}:\n\n", end='')
        for predicate, result in zip(self.predicates, self.results):
            res = result[1]
            if predicate.__name__ == "predicate_base":
                basecorrelation = res
            ratio, count = self.data.quesparser.getratio(predicate)
            actualres = res / basecorrelation
            print(f"Predicate {predicate.__name__} gives correlation result {res}")
            print(f"Correlation result compared to base is: {actualres * 100:.2f}%")
            print(f"Ratio of participants responding positive to Predicate {predicate.__name__} is: {ratio * 100:.2f}%")
            # This subtraction is commutative through absolute value, since one is bigger than the other.
            print(f"Degree of difference between correlation and ratio is: {abs(ratio - actualres) * 100:.2f}%")
            print(f"Number of Participants for Predicate {predicate.__name__} is: {count}\n")

    def presentation_csv_header(self) -> str:
        return "Video ID, " + ''.join([f"{predicate.__name__}, " for predicate in self.predicates])

    def presentation_csv(self) -> str:
        """Cheaply and quickly throws together one line of CSV for the presentation."""
        basecorrelation = 0
        out = f"Video {self.data.vidid}, "
        for predicate, result in zip(self.predicates, self.results):
            res = result[1]
            if predicate.__name__ == "predicate_base":
                basecorrelation = res
                out += f"{basecorrelation:.2f}, "
            else:
                ratio, count = self.data.quesparser.getratio(predicate)
                actualres = res / basecorrelation
                out += f"{(ratio - actualres) * 100:.2f}%, "
        return out


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


def go(vidid: int) -> Tuple[str, str]:  # , threshold: int, delay: int, predicates_used: List):

    threshold = 250
    delay = 50

    predicates_used = (predicate_base, predicate_male, predicate_female, predicate_experience_with_mobile_vr,
                       predicate_experience_with_room_vr, predicate_experience_with_360video,
                       predicate_older_than_25, predicate_younger_than_25, predicate_inexperienced)

    data = DataParser(vidid, "C:/Users/qwe/Documents/vr-viewport-analysis")
    data.generatedata()
    # PyCharm makes a mistake when type checking predicates_used here
    # noinspection PyTypeChecker
    multitasker = CorrelationMultitasker(data, threshold, predicates_used, delay)
    multitasker.render()
    multitasker.showresults()
    return multitasker.presentation_csv_header(), multitasker.presentation_csv()


def main():
    # This is a tuple of videos for which we have complete data.
    complete_videos = (3, 6, 12, 18, 23, 24, 29, 30)
    # complete_videos = (18, 24)
    # for video in complete_videos:
    #    Thread(target=go, args=(video, threshold, delay, predicates_used)).start()
    csv_lines = []
    with Pool() as p:
        csv_lines = p.map(go, complete_videos)

    with open('output.csv', 'w') as f:
        f.write(csv_lines[0][0])
        f.write('\n')
        f.writelines([f"{line[1]}\n" for line in csv_lines])


if __name__ == "__main__":
    main()
