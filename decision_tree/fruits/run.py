import csv


#########################################################################
def top_questions(rows):
    questions = []
    avai_values = set_values(rows)
    for feature in avai_values:
        col_idx, col_values = feature
        for col_val in col_values:
            question = Question(col_idx, col_val)
            true_rows, false_rows = partition(rows, question)

            if not true_rows or not false_rows:
                continue

            gain = gini_info_gain(true_rows, false_rows)
            questions.append([question, gain])
    return questions


def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def set_values(rows):
    u_values = []
    row = rows[0]
    for col in range(len(row) - 1):
        values = set([row[col] for row in rows])
        u_values.append(values)
    return list(zip(range(len(rows)), u_values))
            

def gini_info_gain(parent_branch, left_branch, right_branch):
    prob_left = len(left_branch) / (len(left_branch) + len(right_branch))
    prob_right = len(right_branch) / (len(left_branch) + len(right_branch))

    gini_left = gini(left_branch)
    gini_right = gini(right_branch)

    # Information Gain = Entropy(parent) - ( (Probability(left) * Entropy(Left)) + Probability(right) * Entropy(Right) )
    gain = gini(parent_branch) - ( (prob_left*gini_left) + prob_right*gini_right )

    return round(gain, 3)


def gini(rows):
    counts = label_count(rows)
    impurity = 1
    for label in counts:
        prob_of_label = counts[label] / len(rows)
        impurity -= prob_of_label**2
    return round(impurity, 3)


def label_count(rows):
    count = {}
    for row in rows:
        label = row[-1]
        if label not in count:
            count[label] = 0
        count[label] += 1
    return count


class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, row):
        try:
            self.value = float(self.value)
            return float(row[self.column]) >= self.value
        except ValueError:
            return row[self.column].lower() == self.value.lower()    
        return False

    def __repr__(self):
        try:
            self.value = float(self.value)
            return "%s >= %s " % (self.column, self.value)
        except ValueError:
            return "%s == %s " % (self.column, self.value)



if __name__ == "__main__":
    with open("decision_tree/fruits/data/fruits.csv", "r") as src:
        dataset = csv.reader(src, delimiter=",")
        dataset = list(dataset)[1:]
        print(top_questions(dataset))
        # Need to find good questions base on good impurity
                
        # Partition rows

        # Calculate impurity