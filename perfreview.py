import csv


class Question:
    def __init__(self, row):
        self.question_text = None
        self.response_type = None
        self.response_text = None
        self.responder_name = None
        self.reviewee_name = None
        self.parse_row(row)

    def parse_row(self, row):
        self.question_text = row["Question"]
        self.response_type = row["Response Type"]
        self.response_text = row["Response Text"]
        self.responder_name = row["Responder Name"]
        self.reviewee_name = row["Reviewee Name"]


class Review:
    def __init__(self, responder, reviewee, response_type):
        self.responder_name = responder
        self.reviewee_name = reviewee
        self.response_type = response_type
        self.accomp = None
        self.growth = None

    def add_question(self, question):
        if question.responder_name == self.responder_name and question.reviewee_name == self.reviewee_name:
            if question.question_text == 'Accomplishments & Strengths ':
                self.accomp = question.response_text
            elif question.question_text == 'Areas of Growth & Improvement ':
                self.growth = question.response_text
            else:
                pass


    # def find(self, attributename):
    #     found = None
    #     for question in self.review_questionlist:
    #         if question.question_text == attributename:
    #             found =


class PerformanceReview:
    def __init__(self, reviewee):
        self.reviewee_name = reviewee
        self.peer_reviewlist = list()
        self.manager_review = None
        self.self_review = None
        self.direct_reviewlist =list()

    def add_review(self, review):
        if review.reviewee_name == self.reviewee_name:
            if review.response_type == "self":
                self.self_review = review
            elif review.response_type == "manager":
                self.manager_review = review
            elif review.response_type == "report":
                self.direct_reviewlist.append(review)
            else:
                self.peer_reviewlist.append(review)

    def to_dict(self):
        whatever = dict()
        whatever["Employee Name"] = self.reviewee_name
        whatever["Manager Name"] = self.manager_review.responder_name
        whatever["Accomplishments and Strengths Response - From Manager"] = self.manager_review.accomp
        whatever["Areas of Growth and Improvement Response - From Manager"] = self.manager_review.growth
        whatever["Accomplishments and Strengths Response - From Self"] = self.self_review.accomp
        whatever["Areas of Growth and Improvement Response - From Self"] = self.self_review.growth
        peer_count = 1
        for peer_review in self.peer_reviewlist:
            whatever[f"Peer Reviewer Name {peer_count}"] = peer_review.responder_name
            whatever[f"Accomplishments and Strengths Response - From Peer Reviewer {peer_count}"] = peer_review.accomp
            whatever[f"Areas of Growth and Improvement Response - From Peer Reviewer {peer_count}"] = peer_review.growth
            peer_count += 1
        direct_count = 1
        for direct_review in self.direct_reviewlist:
            whatever[f"Direct Reviewer Name {direct_count}"] = direct_review.responder_name
            whatever[f"Accomplishments and Strengths Response - From Direct Reviewer {direct_count}"] = direct_review.accomp
            whatever[f"Areas of Growth and Improvement Response - From Direct Reviewer {direct_count}"] = direct_review.growth
            direct_count += 1
        return whatever


if __name__ == "__main__":
    # read the data from the csv file
    with open("perfreview.csv", newline="") as csvfile:
        perfreader = csv.DictReader(csvfile, delimiter=",")
        questionlist = list()
        # iterate through the list and do something
        for row in perfreader:
            questionlist.append(Question(row))

        reviews = dict()
        for question in questionlist:
            if question.reviewee_name not in reviews.keys():
                reviews[question.reviewee_name] = {question.responder_name: Review(question.responder_name, question.reviewee_name, question.response_type)}
            else:
                if question.responder_name not in reviews[question.reviewee_name].keys():
                    reviews[question.reviewee_name][question.responder_name] = Review(question.responder_name, question.reviewee_name, question.response_type)
            reviews[question.reviewee_name][question.responder_name].add_question(question)

        performance_reviews = list()
        for reviewee in reviews.keys():
            pr = PerformanceReview(reviewee)
            for review in reviews[reviewee].values():
                pr.add_review(review)
            performance_reviews.append(pr)

        csvoutput = list()
        for output in performance_reviews:
            csvoutput.append(output.to_dict())
        j = 5

    fieldnames = list()
    for review in csvoutput:
        for key in review.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    # output to new .txt file
    with open("formattedperf.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        for review in csvoutput:
            writer.writerow(review)
