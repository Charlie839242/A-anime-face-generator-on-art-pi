import tensorflow as tf
# from tensorflow.python.framework import ops
# from tensorflow.python.ops import math_ops
# from tensorflow.python.keras import backend as K

def convert_tflite(tflite_path, model_path):
    from pathlib import Path
    # 恢复 keras 模型，并预测
    model = tf.keras.models.load_model(model_path)
    model.input.set_shape(1+model.input.shape[1:])

    # 动态量化 dynamic range quantization
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]


    tflite_model = converter.convert()
    tflite_path = Path(tflite_path)
    tflite_path.write_bytes(tflite_model)
    print("convert model to tflite done...")

if __name__ == "__main__":
    # 将h5模型转化为tflite模型方法1
    modelparh = r'D:\垃圾堆\2021春智能嵌入式设计\GAN\h52tflite\model\generator_model_100.h5'
    savepath = r'D:\垃圾堆\2021春智能嵌入式设计\GAN\h52tflite\model\generator_model_100.tflite'
    # open(savepath, "wb").write(tflite_model)
    convert_tflite(savepath, modelparh)