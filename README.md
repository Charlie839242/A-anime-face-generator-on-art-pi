# A-anime-face-generator-on-art-pi
The generator is based on dcgan. It can randomly outputs different anime faces without any input. 
Due to the limited resources of the embedded system, the scale of the generated faces is designed to be 48*48 and to be gray. 

The generated face at 0 epoch:![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/0.png)
The generated face at 1250 epoch:
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/1250.png)
The generated face at 2500 epoch:
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/2500.png)
The generated face at 3750 epoch:
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/3750.png)
The generated face at 5000 epoch:
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/5000.png)
The generated face at 6250 epoch:
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/6250.png)

It could be seen that the model performs bettter at around 5000 epoch.

Here are some examples of generated faces:
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/1.png)
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/2.png)
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/3.png)
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/4.png)
![image](https://github.com/Charlie839242/A-anime-face-generator-on-art-pi/blob/main/images/5.png)


# How to Use

   "py" folder is to train the generator and the discriminator and export them as .h5 file. Then the .h5 file is inverted into .tflite.

   "model" folder stores the resulted models.          //The effects of the models can be tested dircetly on PC without art-pi.

   "dataset_gray_faces_48_48" folder stores the training set, the scale of while is one channel and 48*48.

   "BSP" folder stores the project files that runs the model on the art-pi. It should be opened by "RT-Thread Studio".

