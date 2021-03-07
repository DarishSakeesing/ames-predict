import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np

pd.set_option('display.max_columns', 100)

raw_data = pd.read_csv('Darish/data/Ames_Housing_Price_Data.csv', index_col=0)
raw_data['Log_SalePrice'] = np.log(raw_data['SalePrice'])

pdf = matplotlib.backends.backend_pdf.PdfPages("plots.pdf")

continuous_data = raw_data[['Log_SalePrice','SalePrice','LotFrontage', 'LotArea', 'YearBuilt', 'YearRemodAdd','MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal' ]]

fig_list = []
for feature in continuous_data.columns:
    figure = raw_data.loc[:,[feature, 'Log_SalePrice']].plot(kind='scatter', x=feature,y='Log_SalePrice').figure
    figure.set_size_inches([8, 8])
    fig_list.append(figure)

for fig in fig_list:
    pdf.savefig(fig)

pdf.close()

