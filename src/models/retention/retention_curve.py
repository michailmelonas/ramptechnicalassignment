from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class RetentionCurve:

    def __init__(self):
        self.a = None
        self.b = None

    def fit(self, df):
        x, y = RetentionCurve.get_input_arrays(df)
        parameters, _ = curve_fit(RetentionCurve.retention_func, x, y)
        self.a, self.b = parameters[0], parameters[1]

    @classmethod
    def get_input_arrays(cls, df):
        weighted_retentions = cls.get_weighted_retentions(df)
        x, y = np.array([]), np.array([])

        for k, v in weighted_retentions.items():
            k = float(k[1:])
            x, y = np.append(x, k), np.append(y, v)

        return x, y

    @staticmethod
    def get_weighted_retentions(df):
        weighted_retentions = {}

        cols = list(df.columns)
        n_cols = len(cols)

        for i in range(1, n_cols):
            df_ = df[[cols[0], cols[i]]]
            df_ = df_.dropna()

            weighted_ave = (df_[cols[0]] * df_[cols[i]]).sum() / df_[cols[0]].sum()
            weighted_retentions[cols[i]] = weighted_ave

        return weighted_retentions

    def predict(self, x):
        if x == 0:
            return float(1)

        return RetentionCurve.retention_func(x, self.a, self.b)

    @staticmethod
    def retention_func(x, a, b):
        return a * x ** (-1 * b)

    def visualize(self, df):
        x, y = RetentionCurve.get_input_arrays(df)
        plt.style.use('seaborn')
        plt.plot(x, y, 'ro', label='Weighted retention points')

        x = np.linspace(min(x), max(x), 100)
        plt.plot(x, RetentionCurve.retention_func(x, self.a, self.b), label='Fitted power function')

        plt.legend(loc='upper right')
        plt.xlabel('Days'), plt.ylabel('Retention rate')

        return plt
