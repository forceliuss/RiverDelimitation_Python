import rasterio
import numpy as np
from rasterio.plot import show
import matplotlib.pyplot as plt

riverImage = rasterio.open('../Data/Rst/riverImage2.tif')

fig, ax = plt.subplots(figsize=(16,12))
show(riverImage)

redBand, greenBand, blueBand = riverImage.read(1), riverImage.read(2), riverImage.read(3)

redBand = np.float32(redBand)
greenBand = np.float32(greenBand)
blueBand = np.float32(blueBand)

fig, ax = plt.subplots(figsize=(16,12))
plt.imshow(redBand)

hatariIndex = np.zeros(blueBand.shape)

hatariIndex[(redBand > greenBand) | ((redBand > 100) & (redBand < 160))] = 1

fig, ax = plt.subplots(figsize=(16,12))
plt.imshow(hatariIndex)
plt.colorbar (shrink=0.6)

hatariIndex = np.zeros(blueBand.shape)
hatariIndex[(redBand > greenBand)] = 1

from rasterio.features import shapes

hatariIndex = hatariIndex.astype('float32')

riverShape = shapes(hatariIndex)

for river in riverShape:
    print(river)
    break

def transformPoint(pair):
    lonlatPair = riverImage.xy(pair[1],pair[0])
    return lonlatPair

for river in riverShape:
    print(river[0]['coordinates'])
    coordList = [transformPoint(pair) for pair in river[0]['coordinates'][0]]
    print(coordList)
    break

import fiona

riverShape = shapes(hatariIndex)

schema = {
    'geometry':'LineString',
    'properties':[('ID','int')]
}

lineShp = fiona.open('../Data/Shp/riverLine_v2.shp', mode='w', driver='ESRI Shapefile',schema=schema,crs='EPSG:4326')
i = 0
for river in riverShape:
    coordList = [transformPoint(pair) for pair in river[0]['coordinates'][0]]
    
    rowDict = {
        'geometry':{'type':'LineString', 'coordinates': coordList},
        'properties':{'ID': i},
    }
    lineShp.write(rowDict)
    i += 1
    
lineShp.close()