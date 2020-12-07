import numpy as np
from scipy.linalg import svd
from io import BytesIO
from PIL import Image
import base64
import plotly.express as px
import matplotlib.pyplot as plt


# extract k features
def get_image_features(s, k):
    # do SVD on image，get p,s,q
    p, s, q = svd(s, full_matrices=False)

    s_temp = np.zeros(s.shape[0])
    s_temp[0:k] = s[0:k]
    s = s_temp * np.identity(s.shape[0])

    temp = np.dot(p, s)
    temp = np.dot(temp, q)

    temp[temp >= 255] = 255
    temp[0 >= temp] = 0
    temp = temp.astype(np.uint8)
    # print(temp)
    return temp


def svd_compress(content, degree):
    content = content[content.find(',') + 1:]
    content = base64.b64decode(content)
    imgdata = np.array(Image.open(BytesIO(content)))
    mx = imgdata.shape[1]
    if degree == 'little':
        num = int(round(mx * 0.5))
    if degree == 'medium':
        num = int(round(mx * 0.1))
    if degree == 'high':
        num = int(round(mx * 0.02))

    # get r,g,b matrix
    r = imgdata[:, :, 0]
    g = imgdata[:, :, 1]
    b = imgdata[:, :, 2]

    # plt.figure(figsize=(12,12))

    r_image = get_image_features(r, num)
    g_image = get_image_features(g, num)
    b_image = get_image_features(b, num)

    image = np.stack([r_image, g_image, b_image], axis=2)

    # plt.imshow(image,cmap=plt.cm.gray, interpolation='nearest')
    # plt.show()
    return image
