# A-anime-face-generator-on-art-pi


The generator is based on dcgan. It can randomly outputs different anime faces without any input. 
Due to the limited resources of the embedded system, the scale of the generated faces is designed to be 48*48 and to be gray. 

# How to Use

   "py" folder is to train the generator and the discriminator and export them as .h5 file. Then the .h5 file is inverted into .tflite.

   "model" folder stores the resulted models.          //The effects of the models can be tested dircetly on PC without art-pi.

   "dataset_gray_faces_48_48" folder stores the training set, the scale of while is one channel and 48*48.

   "BSP" folder stores the project files that runs the model on the art-pi. It should be opened by "RT-Thread Studio".

