from dateutil.relativedelta import relativedelta
import pandas as pd


class ActiveUsers:

    def __init__(self,  new_users, retention_curve):
        self.new_users = new_users
        self.retention_curve = retention_curve

    @staticmethod
    def compute_dau(forecast, weights):
        forecast['weight'] = weights
        dau = forecast['DNU'] * forecast['weight']
        dau = dau.sum()
        return dau

    def get_estimated_dnu(self, start_date, n_periods):
        forecast = []

        for i in range(1, n_periods + 1):
            date_ = ActiveUsers.get_new_date(start_date, i)
            prediction = self.new_users.predict(date_)
            prediction = {**{'DATE': date_}, **prediction}
            forecast.append(prediction)

        forecast = pd.DataFrame(forecast)
        return forecast

    @staticmethod
    def get_new_date(start_date, days):
        date_ = start_date + relativedelta(days=days)
        return date_

    def predict(self, df, n_periods):
        predictions = []
        start_date, n_rows = df['DATE'].iloc[-1], len(df.index)


        for i in range(1, n_periods + 1):
            forecast = self.get_estimated_dnu(start_date, n_periods=i)
            forecast = pd.concat([df, forecast], ignore_index=True)

            weights = []
            for j in range(0, n_rows + i):
                days = n_rows + i - 1 - j
                weight = self.retention_curve.predict(days)
                weights.append(weight)

            dau = ActiveUsers.compute_dau(forecast, weights)
            date_ = ActiveUsers.get_new_date(start_date, i)
            predictions.append({'DATE': date_, 'DAU': dau})

        predictions = pd.DataFrame(predictions)
        return predictions
