# A-anime-face-generator-on-art-pi


The generator and  is based on dcgan

"py" file is to train the generator and the discriminator and export them as .h5 file. Then the .h5 file is inverted into .tflite.

"model" file stores the resulted models.
# The effects of the models can be tested dircetly on PC without art-pi.

"dataset_gray_faces_48_48" file stores the training set, teh scale of while is one channel and 48*48.

"BSP" stores the project files that runs the model on the art-pi. It should be opened by "RT-Thread Studio".

