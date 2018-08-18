from statistics import mean
import matplotlib.pyplot as plt
from collections import deque
import os
import csv
import numpy as np

ENV_NAME = "CartPole-v1"
SCORES_CSV_PATH = "./scores/scores.csv"
SCORES_PNG_PATH = "./scores/scores.png"
AVERAGE_SCORE_TO_SOLVE = 195
CONSECUTIVE_RUNS_TO_SOLVE = 100


class ScoreLogger:

    scores = deque()

    def __init__(self):
        if os.path.exists(SCORES_PNG_PATH):
            os.remove(SCORES_PNG_PATH)
        if os.path.exists(SCORES_CSV_PATH):
            os.remove(SCORES_CSV_PATH)

    def add_score(self, score, run):
        self._save_csv(score)
        self._save_png()
        self.scores.append(score)
        if len(self.scores) > CONSECUTIVE_RUNS_TO_SOLVE:
            self.scores.popleft()
        mean_score = mean(self.scores)
        print "SCORES: (min: " + str(min(self.scores)) + ", avg: " + str(mean_score) + ", max: " + str(max(self.scores)) + ")\n"
        if mean_score >= AVERAGE_SCORE_TO_SOLVE and len(self.scores) > CONSECUTIVE_RUNS_TO_SOLVE:
            print "SOLVED in " + str(run) + " runs!"
            exit()

    def _save_png(self):
        x = []
        y = []
        with open(SCORES_CSV_PATH, 'r') as scores:
            reader = csv.reader(scores)
            data = list(reader)
            for i in range(0, len(data)):
                x.append(int(i))
                y.append(int(data[i][0]))

        plt.subplots()
        plt.plot(x, y)

        last_100_mean = [np.mean(self.scores)] * len(x)
        plt.plot(x[-100:], last_100_mean, linestyle="--")

        if len(x) > 1:
            trend_x = x[1:]
            z = np.polyfit(np.array(trend_x), np.array(y[1:]), 1)
            p = np.poly1d(z)
            plt.plot(trend_x, p(trend_x), "r--")

        plt.title(ENV_NAME)
        plt.xlabel("runs")
        plt.ylabel("scores")
        plt.savefig(SCORES_PNG_PATH, bbox_inches="tight")
        plt.close()

    def _save_csv(self, score):
        if not os.path.exists(SCORES_CSV_PATH):
            with open(SCORES_CSV_PATH, "w"):
                pass
        scores_file = open(SCORES_CSV_PATH, "a")
        with scores_file:
            writer = csv.writer(scores_file)
            writer.writerow([score])
