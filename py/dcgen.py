#tensorflow 2.3.0
from tensorflow.keras.layers import Input,Dense,Reshape,Flatten,Dropout
from tensorflow.keras.layers import BatchNormalization,Activation,ZeroPadding2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import UpSampling2D,Conv2D
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.optimizers import Adam,RMSprop

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import matplotlib.pyplot as plt
import sys
import numpy as np

class DCGAN():
    def __init__(self):
        self.img_rows = 48;
        self.img_cols = 48;
        self.channels = 1;
        self.img_shape=(self.img_rows,self.img_cols,self.channels)
        self.latent_dim =100

        optimizer = Adam(0.0002,0.5)
        optimizerD =RMSprop(lr=0.0008, clipvalue=1.0, decay=6e-8)
        optimizerG = RMSprop(lr=0.0004, clipvalue=1.0, decay=6e-8)
        print("-1")

        #对判别器进行构建和编译
        self.discriminator = self.build_discriminator()
        print("0")
        self.discriminator.compile(loss='binary_crossentropy',optimizer=optimizer,metrics=['accuracy'])
        print("1")
        #对生成器进行构造
        self.generator = self.build_generator()
        print("2")
        # The generator takes noise as input and generates imgs
        z = Input(shape=(self.latent_dim,))
        img = self.generator(z)

        # 总体模型只对生成器进行训练
        self.discriminator.trainable = False

        # 从生成器中生成的图 经过判别器获得一个valid
        valid = self.discriminator(img)
        self.combined = Model(z,valid)
        self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

    def build_generator(self):
        #输入100*5*5
        model = Sequential()
        model.add(Dense(6*6*128,activation='relu',input_dim=self.latent_dim))  #输入维度为100，输出128*7*7
        model.add(Reshape((6,6,128)))
        model.add(UpSampling2D())  #进行上采样，变成12*12*128
        model.add(Conv2D(64,kernel_size=3,padding='same'))  #12*12*64
        model.add(BatchNormalization(momentum=0.8))#该层在每个batch上将前一层的激活值重新规范化，即使得其输出数据的均值接近0，其标准差接近1优点（1）加速收敛 （2）控制过拟合，可以少用或不用Dropout和正则 （3）降低网络对初始化权重不敏感 （4）允许使用较大的学习率
        model.add(Activation("relu"))#
        model.add(UpSampling2D())   ###24*24*64
        model.add(Conv2D(32, kernel_size=3, padding="same"))        #24*24*32
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))
        model.add(UpSampling2D())   ###48*48*32
        model.add(Conv2D(self.channels, kernel_size=3, padding="same"))    ###96*96*1
        model.add(Activation("tanh"))


        model.summary()  #打印网络参数

        noise = Input(shape=(self.latent_dim,))
        img = model(noise)
        return  Model(noise,img)  #定义一个 一个输入noise一个输出img的模型

    def build_discriminator(self):
        dropout = 0.25
        depth = 32
        model = Sequential()

        model.add(Conv2D(64, kernel_size=3, strides=2, input_shape=self.img_shape, padding="same"))  # 48*48*64
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))  # 24*24*128
        model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
        model.add(BatchNormalization(momentum=0.8))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(256, kernel_size=3, strides=2, padding="same"))  # 12*12*256
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))

        model.summary()

        img = Input(shape=self.img_shape)
        validity = model(img)

        return Model(img,validity)

    def train(self,epochs,batch_size=128,save_interval = 250):

        # Adversarial ground truths
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        for epoch in range(epochs):

            # ---------------------
            #  Train Discriminator
            # ---------------------

            # Select a random half of images
            # idx = np.random.randint(0, X_train.shape[0], batch_size)
            # imgs = X_train[idx]
            imgs = self.load_batch_imgs(batch_size,'gray_faces48')

            # Sample noise and generate a batch of new images
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            gen_imgs = self.generator.predict(noise)

            # Train the discriminator (real classified as ones and generated as zeros)
            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

            # ---------------------
            #  Train Generator
            # ---------------------

            # Train the generator (wants discriminator to mistake images as real)
            g_loss = self.combined.train_on_batch(noise, valid)
            g_loss = self.combined.train_on_batch(noise, valid)


            # Plot the progress
            print ("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss))

            # If at save interval => save generated image samples
            if epoch % save_interval == 0:
                self.combined.save('./model/combined_model_%d.h5' % epoch)
                self.discriminator.save('./model/discriminator_model_%d.h5' % epoch )
                self.generator.save('./model/generator_model_%d.h5' % epoch)
                self.save_imgs(epoch)


    def load_batch_imgs(self,batch_size,dirName):
        img_names = os.listdir(os.path.join(dirName))
        img_names = np.array(img_names)
        idx = np.random.randint(0, img_names.shape[0], batch_size)
        img_names = img_names[idx]
        img = []
        # 把图片读取出来放到列表中
        for i in range(len(img_names)):
            images = image.load_img(os.path.join(dirName, img_names[i]), color_mode="grayscale", target_size=(48, 48))
            x = image.img_to_array(images)
            x = np.expand_dims(x, axis=0)
            img.append(x)
            # print('loading no.%s image' % i)

        # 把图片数组联合在一起

        x = np.concatenate([x for x in img])
        x = x / 127.5 - 1.
        return x


    def save_imgs(self, epoch):
        r, c = 5, 5
        noise = np.random.normal(0, 1, (r * c, self.latent_dim))  #高斯分布，均值0，标准差1，size= (5*5, 100)
        gen_imgs = self.generator.predict(noise)

        # Rescale images 0 - 1
        gen_imgs = 0.5 * gen_imgs + 0.5

        fig, axs = plt.subplots(r, c)
        cnt = 0   #生成的25张图 显示出来
        for i in range(r):
            for j in range(c):
                axs[i,j].imshow(gen_imgs[cnt, :,:,:])
                axs[i,j].axis('off')
                cnt += 1
        fig.savefig("images/mnist_%d.png" % epoch)
        plt.close()
    def loadModel(self):
        self.combined = load_model('./model/combined_model_9500.h5')
        self.discriminator = load_model('./model/discriminator_model_9500.h5')
        #self.generator = load_model('./model/generator_model.h5')
if __name__ == '__main__':
    dcgan = DCGAN()
    dcgan.train(epochs=40000, batch_size=64, save_interval=100)

