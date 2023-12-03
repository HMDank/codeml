import numpy as np
import pandas as pd

df_cars = pd.read_csv('data\\cars.csv')

df_ad_locations = pd.read_csv('data\\ad_locations.csv')
df_wards = pd.read_csv('data\\regions.csv')
df_regions = pd.read_csv('data\\regions.csv')
df_subregions = pd.read_csv('data\\subregions.csv')

#NOTE: chưa remove nhiều outliers + có vẻ quá ít data points
df_cars = df_cars.drop_duplicates().dropna()
df_cars = df_cars[(df_cars.brand.isin(['Toyota', 'Ford', 'Kia', 'Huyndai', 'Mitsubishi',
                                      'Mercedes Benz', 'Mazda', 'Honda', 'Chevrolet', 'Vinfast',
                                      'Suzuki', 'BMW', 'Nissan', 'Daewoo', 'Lexus', 'Peugeot']))
                                      & (df_cars.condition == "used")
                                      & (df_cars.mileage_v2 > 0)
                                      & (df_cars.mileage_v2 > 5000)
                                      & (df_cars.price > 200000000)
                                      & (df_cars.gearbox != "unknown")
                                      & (df_cars.manufacture_date > 2017)
                                      & (df_cars.model != 'Dòng khác')
                                      & (df_cars.origin != 'Nước khác')
                                      & (df_cars.type != 'Kiểu dáng khác')
                                      & (df_cars.type != 'Kiểu dáng khác')
                                      & (df_cars.seats > 4)
                                      ]
df_cars = df_cars[['id','brand','model','price']]

df_locations = pd.merge(df_cars, df_ad_locations, on = "id")
df_locations = df_locations.drop(['longitude', 'latitude'], axis = 1)
df_locations.dropna()
df_locations.drop_duplicates()

df_regions = df_regions.rename(columns = {'id' : 'region_id'})
df_regionid = pd.merge(df_locations, df_regions, on = "region_id")
df_regionid = df_regionid.drop(['url'], axis = 1)
df_regionid = df_regionid.drop_duplicates()
df = df_regionid.dropna()

df = df[df['model'].str.contains("Dòng khác") == False]
df = df[df['brand'].str.contains("Hãng khác") == False]
df =df.drop(['ward_id','region_id',	'subregion_id'], axis = 1)

City = ['Tp Hồ Chí Minh', 'Hà Nội', 'Hải Phòng', 'Đà Nẵng', 'Cần Thơ']
Urban = np.setdiff1d(df['name'], City)

avg_price_city = df.groupby(['brand', 'model', 'name'])['price'].mean()
avg_price_city_df = avg_price_city.reset_index()

df_city = avg_price_city_df[avg_price_city_df['name'].isin(City)]
df_urban = avg_price_city_df[~avg_price_city_df['name'].isin(City)]

merged = pd.merge(df_city, df_urban, on = ['brand', 'model'])
merged['price_ratio'] = merged['price_x'] / merged['price_y']
merged.drop_duplicates()

final_df = merged.drop(columns = ['price_x', 'price_y'])
final_df = final_df.rename(columns={'name_x' : 'City', 'name_y' : 'Urban'})

final_df.to_csv('data.csv')