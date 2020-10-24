from retention import RetentionCurve
import pandas as pd

_PROCESSED_DATA_PATH = '../../data/processed/'
_REPORTS_FIGURES_PATH = '../../reports/figures/'

# Get pre-processed data
df = pd.read_csv(_PROCESSED_DATA_PATH + 'usage_data.csv')

# Data for fitting retention curve
weighted_triangle_df = df.tail(180)
weighted_triangle_df = weighted_triangle_df.reset_index(drop=True)
weighted_triangle_df = weighted_triangle_df.dropna(axis=1, how='all')

cols = ['DATE', 'Revenue', 'DAU']
weighted_triangle_df = weighted_triangle_df.drop(cols, axis=1)

# Fit retention curve
rc = RetentionCurve()
rc.fit(df=weighted_triangle_df)

# Visualize retention curve
plt = rc.visualize(df=weighted_triangle_df)
plt.savefig(_REPORTS_FIGURES_PATH + 'retention.png')

# Fit time series to last 180 days of DNU numbers
