from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import sympy as sym


class RetentionCurve:
    _ROUND = 3

    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def fit(self, df):
        x, y = RetentionCurve.get_input_arrays(df)
        popt, _ = curve_fit(RetentionCurve.retention_func, x, y)
        self.a, self.b = popt[0], popt[1]

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
        y = RetentionCurve.retention_func(x, self.a, self.b)
        return y

    @staticmethod
    def retention_func(x, a, b):
        return a * x ** (-1 * b)

    def visualize(self, df):
        x, y = RetentionCurve.get_input_arrays(df)
        plt.plot(x, y, 'ro', label='Weighted retention points')

        x = np.linspace(min(x), max(x), 100)
        a, b = round(self.a, RetentionCurve._ROUND), round(self.b, RetentionCurve._ROUND)
        plt.plot(x, RetentionCurve.retention_func(x, a, b), label='Fitted power function')
        
        xs = sym.Symbol('x')
        tex = sym.latex(RetentionCurve.retention_func(xs, a, b)).replace('$', '')
        plt.title(r'Power function: $f(x)= %s$' %(tex),fontsize=15)
        plt.legend(loc='upper right')

        return plt
