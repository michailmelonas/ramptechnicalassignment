import matplotlib.pyplot as plt
import seaborn as sns


class NewUsers:

    def __init__(self):
        self.average = None

    def fit(self, df):
        self.average = df['DNU'].mean()

    def predict(self, date_):
        prediction = {
            'DNU': self.average
        }
        return prediction

    @staticmethod
    def visualize(df):
        plt.style.use('seaborn')
        plt.plot_date(df['DATE'], df['DNU'], linestyle='solid', marker=None)
        plt.xlabel('Date'), plt.ylabel('DNU')
        return plt
