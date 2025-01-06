import numpy as np
import pandas as pd
import tifffile as ti
# import matplotlib.pyplot as plt
# from scipy import ndimage as ndi
from tqdm import tqdm
# from skimage.segmentation import watershed
# from skimage.feature import peak_local_max
# import multiprocessing
# from joblib import Parallel, delayed, Memory

def map_nuc(final_mask,labels,mask,l):
    feats = mask[labels==l]
    feats = list(feats[feats!=0])


    if len(feats)>0:

        feat = max(set(feats), key=feats.count)

        final_mask[labels==l] = feat

    return final_mask

filename = '/orange/pinaki.sarder/nlucarelli/intestine/23_09_CODEX_HuBMAP_alldata_Dryad_merged.csv'
file_path = '/orange/pinaki.sarder/nlucarelli/intestine/'

data = pd.read_csv(filename)
column_names = list(data.columns)

tissue_segments = list(data["unique_region"].drop_duplicates())

classes = list(data["Cell Type"].drop_duplicates())
no_classes = len(classes)
class_idx = list(range(1,no_classes+1))

donors = list(data["donor"].drop_duplicates())

skip_donors = ['B001','B006','B008']
skip_arrays = ['B009Bt']

for donor in tqdm(donors,desc='donors'):

    if donor in skip_donors:
        continue

    arrays = list(data["array"][data["donor"]==donor].drop_duplicates())

    for array in tqdm(arrays,desc='arrays'):


        if array in skip_arrays:
            continue


        regions = list(data["region"][data["array"]==array].drop_duplicates())

        for region in tqdm(regions,desc='Regions'):


            xlocs = list(data["x"][(data["array"]==array) & (data["region"]==region)])
            ylocs = list(data["y"][(data["array"]==array) & (data["region"]==region)])
            class_nms = list(data["Cell Type"][(data["array"]==array)&(data["region"]==region)])

            class_ids = []

            for nm in class_nms:
                result = [item1 for item1, condition in zip(class_idx, classes) if condition == nm]
                class_ids.append(result[0])



            slide_name = file_path + donor + '/' + array + '/reg00' + str(int(region)) + '_X01_Y01_Z01.tif'

            slide = ti.imread(slide_name)[0,0,:,:]


            x,y = slide.shape

            mask = np.zeros((x,y))
            mask = mask.astype(np.uint8)


            for loc in range(len(xlocs)):
                x_cent = int(xlocs[loc])
                y_cent = int(ylocs[loc])
                class_temp = class_ids[loc]

                try:
                    mask[y_cent-3:y_cent+3,x_cent-3:x_cent+3] = class_temp
                except:
                    mask[y_cent,x_cent] = class_temp

            ti.imwrite(file_path + donor + '/' + array + '/reg00' + str(int(region)) + '_classes.tif',mask,photometric='minisblack')

            del slide
            # binary = slide > 5400

            # distance = ndi.distance_transform_edt(binary)
            # footprint_size = (25, 25)  # Adjust this size based on your needs
            # coords = peak_local_max(distance, footprint=np.ones(footprint_size), labels=binary)
            # mask2 = np.zeros(distance.shape, dtype=bool)
            # mask2[tuple(coords.T)] = True
            # markers, _ = ndi.label(mask2)
            # compactness = 0.1  # Adjust this value based on your needs
            # labels = watershed(-distance, markers, mask=binary, compactness=compactness)

            # final_mask = np.zeros((x,y))
            # num_processes=multiprocessing.cpu_count()

            # final_mask = Parallel(n_jobs=num_processes,prefer="threads",require="sharedmem")(delayed(map_nuc)(final_mask,labels,mask,l) for l in tqdm(range(1,np.max(labels)+1),desc='Nucs'))
            # final_mask = final_mask[0]
            # final_mask = final_mask.astype(np.uint8)

            # ti.imwrite(file_path + donor + '/' + array + '/reg00' + str(int(region)) + 'overlay.tif',final_mask,photometric='minisblack')
            # del final_mask, slide, binary,mask
