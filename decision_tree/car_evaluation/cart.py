import csv
import random

import pandas as pd
from dataclasses import dataclass
from decision_tree.lib.utils import gini_gain, entropy_gain
from decision_tree.lib.classification_detree import DecisionTree, MedianLeaf, Leaf


@dataclass()
class CarRecord:
    buying: str
    maint: str
    doors: int
    persons: int
    lug_boot: str
    safety: str
    klass: str = None

    def clean_data(self):
        if self.doors == "5more":
            self.doors = 5
        else:
            self.doors = int(self.doors)

        if self.persons == "more":
            self.persons = 6
        else:
            self.persons = int(self.persons)
        return self

    def to_list(self):
        return [self.buying, self.maint, self.doors, self.persons, self.lug_boot, self.safety, self.klass]



if __name__ == '__main__':
    print("S T A R T E D")
    headers = ["buying", "maint", "doors", "persons", "lug_boot", "safety"]

    known_label = []
    predicted_label = []
    with open("./data/car.data", "r+") as src:
        rows = []
        dataset = list(csv.reader(src, delimiter=","))
        for i in dataset:
            known_label.append(str(i[6]))
            rows.append(CarRecord(i[0], i[1], i[2], i[3], i[4], i[5], i[6]).clean_data().to_list())

        # make a classifier instance with information gain = gini | entropy
        dtree = DecisionTree(information_gain=entropy_gain,
                             max_depth=6,
                             leaf_style=Leaf)

        tree = dtree.build_tree(rows)
        dtree.print_tree(tree, headers=headers)

        # for i in dataset:
        row = random.choice(dataset)
        r = CarRecord(row[0], row[1], row[2], row[3], row[4], row[5]).clean_data().to_list()
        label, perc = dtree.classify(r, tree)
        predicted_label.append(label)

    df_prediction = pd.Series(predicted_label, name="Predicted")
    df_actual = pd.Series(known_label, name="Actual")
    df_confusion = pd.crosstab(df_prediction, df_actual)

    print("-" * 35)
    print(df_confusion)
    print("-"*35)

    print("D O N E")