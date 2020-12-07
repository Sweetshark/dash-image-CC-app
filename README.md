# Dash Image Convert&Compress App
This is a demo of the Dash interactive Python framework developed by [Plotly](https://plot.ly/).

Dash abstracts away all of the technologies and protocols required to build an interactive web-based application and is a simple and effective way to bind a user interface around your Python code. To learn more check out our [dash](https://plot.ly/dash).

![screenshot](https://github.com/Sweetshark/dash-image-CC-app/blob/main/images/screenshot.png)

# Introduction
## Main Functions:
1. Convert
- Upload one or more images, choose the format you want and click the download for each image. You will get the images of specific format you want. Here you have 4 options for the export image format.
2. Compress
-  Upload one or more images, choose the degree of compression you want and click download. There are 3 options to choose. *Slightly, Moderately, High* represents different degrees. The more you compress, the smaller the storage of the image will take up and the blurry the image will be. The influence of the first two options have on images will barely visible to naked eye.

## Main Algorithm and tools
1. SVD 
- It is a algorithm widely used in dimensionality reduction. In image processing, svd could be conducted on np.array images of RGBA(shape of (x,y,z)). After the svd, the image array could be shown by matplotlib or Image or other packages like cv2.
2. Base63, encoder, decoder
- Consider the images upload is encoded with base64, I used b64 to decode and convert to bytes then opened with Image(a method in pillow(PIL)).After compression processing(if any), it will be shown on plotly canvas. Then store the image of base64 encoded format in download button.

## Instructions
1. Upload images you want to process, it will be shown on canvas with the filename and upload time;
2. Choose the conversion or compression options. You can choose both;
3. Wait for updating, you will see the change of figures on canvas;
4. Click download to get the images in your requirement, the image will be saved with the same name it had before.

## Others
- I also add a modebar in plotly canvas, which means you can also zoom in, zoon out, dawrn lines and so on.
