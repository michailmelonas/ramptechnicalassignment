from newusers import NewUsers
from retention import RetentionCurve
import pandas as pd

_DAYS = 180
_PROCESSED_DATA_PATH = '../../data/processed/'
_REPORTS_FIGURES_PATH = '../../reports/figures/'


# Get pre-processed data
df = pd.read_csv(_PROCESSED_DATA_PATH + 'usage_data.csv')

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
dnu_time_series_df['DATE'] = pd.to_datetime(dnu_time_series_df['DATE'])

# Visualize DNU time series
nu = NewUsers()
fig = nu.visualize(df=dnu_time_series_df)
fig.savefig(_REPORTS_FIGURES_PATH + 'dnu.png')
fig.close()

# Fit (simple) new user forecast model
nu.fit(df=dnu_time_series_df)
