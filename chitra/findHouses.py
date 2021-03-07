import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import CustomPipeline as cp
from geopy.distance import geodesic 
imputedHousingData=pd.read_csv("./data/predictedSalePrice.csv")
mappingData = pd.read_csv('./location_mapping/full_latlon.csv')

def convert_latitude(coordinate):
    return float(str(coordinate).replace("(","").replace(")","").split(",")[0])
def convert_longitude(coordinate):
    if (len(str(coordinate).replace("(","").replace(")","").split(",")))==2:
        return float(str(coordinate).replace("(","").replace(")","").split(",")[1])
    else:
        return 0
def get_distance(pointa,pointb):
    return geodesic(pointa,pointb).miles
    
imputedHousingData_map = pd.merge(imputedHousingData, mappingData, on='PID')
imputedHousingData_map["latitude"]=imputedHousingData_map['coord'].apply(convert_latitude)
imputedHousingData_map["longitude"]=imputedHousingData_map['coord'].apply(convert_longitude)
cheapest_200_homes=imputedHousingData_map.sort_values("SalePrice").head(200)
uni_coord=pd.DataFrame({'name':['Iowa State University'],'latitude':[42.023949], 'longitude':[-93.647595]})
university_coordinates = (uni_coord.loc[0,'latitude'],uni_coord.loc[0,'longitude'])
cheapest_200_homes.loc[:,'distUni']=cheapest_200_homes.apply(lambda x: get_distance((x.latitude, x.longitude),university_coordinates), axis=1)
homesforUniHousing=cheapest_200_homes[
    ((cheapest_200_homes['distUni']<=1) & 
     ((cheapest_200_homes['BedroomAbvGr']/cheapest_200_homes['FullBath']<=2) | 
      (((cheapest_200_homes['BsmtFinType1']>=5) | 
        (cheapest_200_homes['BsmtFinType2']>=5) & 
        (cheapest_200_homes["BsmtFullBath"]>=1)))) &
    (cheapest_200_homes['OverallCond'] <= 3) & (cheapest_200_homes['OverallQual']<=3))
]
print(homesforUniHousing)