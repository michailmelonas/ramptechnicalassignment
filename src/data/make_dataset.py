import pandas as pd

_DATA_PATH = '../../data/'


def main():
    df = pd.read_csv(_DATA_PATH + 'raw/demo_test_data (1).csv')
    # TODO: clean/pre-process

    df.to_csv(_DATA_PATH + 'processed/usage_data.csv', index=False)

if __name__ == '__main__':
    main()
