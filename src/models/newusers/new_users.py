import matplotlib.pyplot as plt
import seaborn as sns


class NewUsers:

    def __init__(self):
        self.average = None
        self.max = None
        self.min = None

    def fit(self, df):
        self.average = df['DNU'].mean()
        self.max = df['DNU'].max()
        self.min = df['DNU'].min()

    def predict(self, date_):
        prediction = {
            'yhat': self.average,
            'ymax': self.max,
            'ymin': self.min
        }
        return prediction

    @staticmethod
    def visualize(df):
        plt.style.use('seaborn')
        plt.plot_date(df['DATE'], df['DNU'], linestyle='solid', marker=None)
        plt.xlabel('Date'), plt.ylabel('DNU')
        return plt
