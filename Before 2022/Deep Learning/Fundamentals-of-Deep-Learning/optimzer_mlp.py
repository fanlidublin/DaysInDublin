import input_data
mnist = input_data.read_data_sets("data/", one_hot=True)

import tensorflow as tf
import argparse

# Architecture
n_hidden_1 = 256
n_hidden_2 = 256

# Parameters
training_epochs = 500
batch_size = 100
display_step = 100

def layer(input, weight_shape, bias_shape):
    weight_init = tf.random_normal_initializer(stddev=(2.0/weight_shape[0])**0.5)
    bias_init = tf.constant_initializer(value=0)
    W = tf.get_variable("W", weight_shape, initializer=weight_init)
    b = tf.get_variable("b", bias_shape, initializer=bias_init)
    return tf.nn.relu(tf.matmul(input, W) + b)

def inference(x):
    with tf.variable_scope("hidden_1"):
        hidden_1 = layer(x, [784, n_hidden_1], [n_hidden_1])
     
    with tf.variable_scope("hidden_2"):
        hidden_2 = layer(hidden_1, [n_hidden_1, n_hidden_2], [n_hidden_2])
     
    with tf.variable_scope("output"):
        output = layer(hidden_2, [n_hidden_2, 10], [10])

    return output

def loss(output, y):
    xentropy = tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=y)    
    loss = tf.reduce_mean(xentropy)
    return loss

def training(cost, global_step, optimizer):
    tf.summary.scalar("cost", cost)
    train_op = None
    print optimizer
    if optimizer == "sgd":
        learning_rate = 0.01
        optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        train_op = optimizer.minimize(cost, global_step=global_step)
    if optimizer == "momentum":
        learning_rate = 0.01
        momentum = 0.9
        optimizer = tf.train.MomentumOptimizer(learning_rate, momentum)
        train_op = optimizer.minimize(cost, global_step=global_step)
    return train_op


def evaluate(output, y):
    correct_prediction = tf.equal(tf.argmax(output, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar("validation error", (1.0 - accuracy))
    return accuracy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test various optimization strategies')
    parser.add_argument('optimizer', nargs=1, type=str)
    args = parser.parse_args()

    with tf.Graph().as_default():
        with tf.variable_scope("mlp_model"):
            x = tf.placeholder("float", [None, 784]) # mnist data image of shape 28*28=784
            y = tf.placeholder("float", [None, 10]) # 0-9 digits recognition => 10 classes

            output = inference(x)
            cost = loss(output, y)
            global_step = tf.Variable(0, name='global_step', trainable=False)
            train_op = training(cost, global_step, args.optimizer[0])
            eval_op = evaluate(output, y)
            summary_op = tf.summary.merge_all()
            saver = tf.train.Saver()

            sess = tf.Session()
            summary_writer = tf.summary.FileWriter("mlp_logs_%s/" % args.optimizer[0], graph=sess.graph)
            
            init_op = tf.global_variables_initializer()
            sess.run(init_op)

            # saver.restore(sess, "mlp_logs/model-checkpoint-66000")

            # Training cycle
            for epoch in range(training_epochs):
                avg_cost = 0.
                total_batch = int(mnist.train.num_examples/batch_size)
                # Loop over all batches
                for i in range(total_batch):
                    minibatch_x, minibatch_y = mnist.train.next_batch(batch_size)
                    # Fit training using batch data
                    sess.run(train_op, feed_dict={x: minibatch_x, y: minibatch_y})
                    # Compute average loss
                    avg_cost += sess.run(cost, feed_dict={x: minibatch_x, y: minibatch_y})/total_batch
                # Display logs per epoch step
                if epoch % display_step == 0:
                    print "Epoch:", '%04d' % (epoch+1), "cost =", "{:.9f}".format(avg_cost)
                    accuracy = sess.run(eval_op, feed_dict={x: mnist.validation.images, y: mnist.validation.labels})
                    print "Validation Error:", (1 - accuracy)
                    summary_str = sess.run(summary_op, feed_dict={x: minibatch_x, y: minibatch_y})
                    summary_writer.add_summary(summary_str, sess.run(global_step))

                    saver.save(sess, "mlp_logs_%s/model-checkpoint" % args.optimizer[0], global_step=global_step)

            print "Optimization Finished!"
            accuracy = sess.run(eval_op, feed_dict={x: mnist.test.images, y: mnist.test.labels})
            print "Test Accuracy:", accuracy