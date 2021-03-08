import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import CustomPipeline as cp
import pickle
from geopy.distance import geodesic 


def convert_string_to_coor(s):
    s = s.strip('()')
    points = s.split(',')
    coor = (float(points[0]), float(points[1]))
    return coor

def get_distance(pointa,pointb):
    return geodesic(pointa,pointb).miles



def getUniHouses(path):
    loaded_model = pickle.load(open('../LinearModel.sav', 'rb'))

    data = cp.clean(path)

    latlongDF = pd.read_csv('data/latlong.csv')

    significant_features = ['GrLivArea', 'OverallQual', 'YearBuilt', 'Neighborhood_Crawfor', 'Neighborhood_Somerst', 
                            'Neighborhood_NridgHt', 'LotArea', 'Neighborhood_StoneBr', 'BsmtExposure', 
                            'YearRemodAdd', 'ExterQual', 'Functional', 'Exterior1st', 'FireplaceQu', 
                            'ScreenPorch', 'Fireplaces','GarageCond', 'EnclosedPorch', 'PavedDrive','GarageArea', 
                            'BsmtFullBath', 'Condition1_Norm', 'MSSubClass_20', 'TotRmsAbvGrd', 'BsmtQual', 
                            'BsmtFinType1', 'BldgType_1Fam', 'Neighborhood_ClearCr', 'Neighborhood_BrkSide', 
                            'HalfBath', 'BsmtFinSF2', 'NewHome', 'LandContour_HLS', '3SsnPorch', 'Condition1_PosN', 
                            'WoodDeckSF', 'Neighborhood_Timber', 'GarageFinish', 'PoolQC', 'MSZoning_RL', 
                            'Neighborhood_IDOTRR', 'RoofMatl', 'RoofStyle', 'Alley', 'GasHeating',  
                            'LotConfig_CulDSac', 'Neighborhood_Sawyer', 'MasVnrArea', 'ModernElectrical', 
                            'LotFrontage', 'ExterCond', 'Neighborhood_CollgCr', 'GarageType']

    X_test = data[significant_features]

    predicted_y = loaded_model.predict(X_test)

    data['PredictedSalePrice'] = np.exp(predicted_y)

    data = data.merge(latlongDF, on='PID')

    data.dropna(inplace=True)

    data['point'] = data['point'].apply(convert_string_to_coor)

    university_coordinates = (42.023949,-93.647595)
    data['distance'] = data.apply(lambda x: get_distance(x.point,university_coordinates), axis=1)
    data.sort_values('PredictedSalePrice', ascending=True, inplace = True)
    data.head(int(0.1*len(data)))
    homesforUniHousing=data[
        ((data['distance']<=1) & 
         ((data['BedroomAbvGr']/data['FullBath']<=2) | 
          (((data['BsmtFinType1']>=5) | 
            (data['BsmtFinType2']>=5) & 
            (data["BsmtFullBath"]>=1)))) &
        (data['OverallCond'] <= 3) & (data['OverallQual']<=3))
    ]

    homesforUniHousing.to_csv('uni_houses.csv')