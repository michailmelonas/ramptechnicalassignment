from activeusers import ActiveUsers
from newusers import NewUsers
from retention import RetentionCurve
import matplotlib.pyplot as plt
import pandas as pd

_DAYS = 180
_FORECAST_PERIOD = 730
_PROCESSED_DATA_PATH = '../../data/processed/'
_REPORTS_FIGURES_PATH = '../../reports/figures/'


# Get pre-processed data
df = pd.read_csv(_PROCESSED_DATA_PATH + 'usage_data.csv')
df['DATE'] = pd.to_datetime(df['DATE'])

# Data for fitting retention curve
weighted_triangle_df = df.tail(_DAYS)
weighted_triangle_df = weighted_triangle_df.reset_index(drop=True)
weighted_triangle_df = weighted_triangle_df.dropna(axis=1, how='all')

cols = ['DATE', 'Revenue', 'DAU']
weighted_triangle_df = weighted_triangle_df.drop(cols, axis=1)

# Fit retention curve
rc = RetentionCurve()
rc.fit(df=weighted_triangle_df)

# Visualize retention curve
fig = rc.visualize(df=weighted_triangle_df)
fig.savefig(_REPORTS_FIGURES_PATH + 'retention.png')
fig.close()

# Evaluate last _DAYS days of DNU numbers as time series
dnu_time_series_df = df.tail(_DAYS)
dnu_time_series_df = dnu_time_series_df.reset_index(drop=True)

cols = ['DATE', 'DNU']
dnu_time_series_df = dnu_time_series_df[cols]

# Visualize DNU time series
nu = NewUsers()
fig = nu.visualize(df=dnu_time_series_df)
fig.savefig(_REPORTS_FIGURES_PATH + 'dnu.png')
fig.close()

# Fit (simple) new user forecast model
nu.fit(df=dnu_time_series_df)

# Create ActiveUsers object
au = ActiveUsers(new_users=nu, retention_curve=rc)

# Predict future DAU using historic DNU data, together with rc and nu
cols = ['DATE', 'DNU']
historic_dnu_df = df[cols]
predictions = au.predict(df=historic_dnu_df, n_periods=_FORECAST_PERIOD)

# Visualize DAU time series
plt.plot_date(df['DATE'], df['DAU'], linestyle='solid', marker=None)
plt.plot_date(predictions['DATE'], predictions['DAU'], linestyle='solid', marker=None)
plt.savefig(_REPORTS_FIGURES_PATH + 'dau.png')
plt.close()
