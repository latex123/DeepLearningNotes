import tensorflow as tf
from agent.framework import Framework


class Agent(object):
    def __init__(self, train=True):
        if train:
            self.agent = Framework(0.5)
        else:
            self.agent = Framework(1.0)

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=config)
        trainable_variables = tf.get_collection(
            tf.GraphKeys.TRAINABLE_VARIABLES, "value")
        # print(trainable_variables)
        self.saver = tf.train.Saver(trainable_variables)
        self.sess.run(tf.global_variables_initializer())
        self.sess.graph.finalize()

    def get_deterministic_policy(self, inputs):
        return self.agent.get_deterministic_policy(self.sess, inputs)

    def get_stochastic_policy(self, inputs, epsilon=0.9):
        return self.agent.get_stochastic_policy(self.sess, inputs, epsilon)

    def update_cache(self, state, action, reward, next_state, done):
        self.agent.update_cache(state, action, reward, next_state, done)

    def update_eval(self):
        self.agent.update_value_net(self.sess)

    def update_target(self):
        self.agent.update_target_net(self.sess)

    def save_model(self, path="model/ddqn.ckpt"):
        self.saver.save(self.sess, path)

    def restore_model(self, path="model/ddqn.ckpt"):
        self.saver.restore(self.sess, path)

    def close(self):
        self.sess.close()
