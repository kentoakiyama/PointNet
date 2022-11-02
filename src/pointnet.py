import tensorflow as tf

from tnet import TNet


class PointNet(tf.keras.Model):
    def __init__(self, num_points: int, num_classes: int, activation: str):
        super(PointNet, self).__init__()

        self.input_tnet = TNet(num_points=num_points, k=3, activation=activation)
        self.feature_tnet = TNet(num_points=num_points, k=64, activation=activation)

        self.nonlinear1 = tf.keras.layers.Dense(64)
        self.nonlinear2 = tf.keras.layers.Dense(64)
        self.nonlinear3 = tf.keras.layers.Dense(64)
        self.nonlinear4 = tf.keras.layers.Dense(128)
        self.nonlinear5 = tf.keras.layers.Dense(1024)
        self.nonlinear6 = tf.keras.layers.Dense(512)
        self.nonlinear7 = tf.keras.layers.Dense(256)
        self.nonlinear8 = tf.keras.layers.Dense(num_classes)

        self.bn1 = tf.keras.layers.BatchNormalization()
        self.bn2 = tf.keras.layers.BatchNormalization()
        self.bn3 = tf.keras.layers.BatchNormalization()
        self.bn4 = tf.keras.layers.BatchNormalization()
        self.bn5 = tf.keras.layers.BatchNormalization()
        self.bn6 = tf.keras.layers.BatchNormalization()
        self.bn7 = tf.keras.layers.BatchNormalization()

        self.activation1 = tf.keras.layers.Activation(activation)
        self.activation2 = tf.keras.layers.Activation(activation)
        self.activation3 = tf.keras.layers.Activation(activation)
        self.activation4 = tf.keras.layers.Activation(activation)
        self.activation5 = tf.keras.layers.Activation(activation)
        self.activation6 = tf.keras.layers.Activation(activation)
        self.activation7 = tf.keras.layers.Activation(activation)
        self.softmax = tf.keras.layers.Activation('softmax')

        self.maxpooling1 = tf.keras.layers.MaxPooling1D(num_points)

        self.flatten = tf.keras.layers.Flatten()

    def call(self, input):
        # input transform
        matrix3 = self.input_tnet(input)
        out = tf.matmul(input, matrix3)

        out = self.activation1(self.bn1(self.nonlinear1(out)))
        out = self.activation2(self.bn2(self.nonlinear2(out)))
        
        # feature transform
        matrix64 = self.feature_tnet(input)
        out = tf.matmul(out, matrix64)

        out = self.activation3(self.bn3(self.nonlinear3(out)))
        out = self.activation4(self.bn4(self.nonlinear4(out)))
        out = self.activation5(self.bn5(self.nonlinear5(out)))

        out = self.flatten(out)

        out = self.activation6(self.bn6(self.nonlinear6(out)))
        out = self.activation7(self.bn7(self.nonlinear7(out)))
        return self.softmax(self.nonlinear8(out))
