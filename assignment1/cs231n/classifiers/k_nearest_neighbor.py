import numpy as np
from past.builtins import xrange
import time

class KNearestNeighbor(object):
  """ a kNN classifier with L2 distance """

  def __init__(self):
    pass

  def train(self, X, y):
    """
    Train the classifier. For k-nearest neighbors this is just 
    memorizing the training data.

    Inputs:
    - X: A numpy array of shape (num_train, D) containing the training data
      consisting of num_train samples each of dimension D.
    - y: A numpy array of shape (N,) containing the training labels, where
         y[i] is the label for X[i].
    """
    self.X_train = X
    self.y_train = y
    
  def predict(self, X, k=1, num_loops=0):
    """
    Predict labels for test data using this classifier.

    Inputs:
    - X: A numpy array of shape (num_test, D) containing test data consisting
         of num_test samples each of dimension D.
    - k: The number of nearest neighbors that vote for the predicted labels.
    - num_loops: Determines which implementation to use to compute distances
      between training points and testing points.

    Returns:
    - y: A numpy array of shape (num_test,) containing predicted labels for the
      test data, where y[i] is the predicted label for the test point X[i].  
    """
    if num_loops == 0:
      dists = self.compute_distances_no_loops(X)
    elif num_loops == 1:
      dists = self.compute_distances_one_loop(X)
    elif num_loops == 2:
      dists = self.compute_distances_two_loops(X)
    else:
      raise ValueError('Invalid value %d for num_loops' % num_loops)

    return self.predict_labels(dists, k=k)

  def compute_distances_two_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a nested loop over both the training data and the 
    test data.

    Inputs:
    - X: A numpy array of shape (num_test, D) containing test data.

    Returns:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      is the Euclidean distance between the ith test point and the jth training
      point.
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train))

    start = time.time()
    interval = 90
    # print("kick off")
    for i in xrange(num_test):
      for j in xrange(num_train):
        # given that both the training and test sample is a vector of D.
        # tic = time.time()
        dists[i][j] = np.linalg.norm(X[i] - self.X_train[j])
        # print("1 iteration took {}s".format(time.time() - tic))
        # break
        
    # print("{}s used".format(int(time.time() - start)))
        #####################################################################
        #                       END OF YOUR CODE                            #
        #####################################################################

    return dists

  def compute_distances_one_loop(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a single loop over the test data.

    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train))
    # start = self.report_time(meta="start")
    start = time.time()
    for i in xrange(num_test):
      #######################################################################
      # TODO:                                                               #
      # Compute the l2 distance between the ith test point and all training #
      # points, and store the result in dists[i, :].                        #
      #######################################################################
      # X[i] is test sample
      # self.X_train is a vector of training samples

      # A Very Naive Way
      # tic = time.time()
      X_test = np.broadcast_to(X[i], self.X_train.shape)
      # import pdb; pdb.set_trace()

      dists[i] = np.linalg.norm(X_test - self.X_train, axis=-1)

      # print("axial norm took {}s".format(time.time() - tic)); tic = time.time()
      
      #######################################################################
      #                         END OF YOUR CODE                            #
      #######################################################################
    print("{}s elapsed".format(int(time.time() - start)))
    return dists

  def compute_distances_no_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using no explicit loops.

    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    start = time.time()
    # print("kick off")
    dists = np.zeros((num_test, num_train)) 
    #########################################################################
    # TODO:                                                                 #
    # Compute the l2 distance between all test points and all training      #
    # points without using any explicit loops, and store the result in      #
    # dists.                                                                #
    #                                                                       #
    # You should implement this function using only basic array operations; #
    # in particular you should not use functions from scipy.                #
    #                                                                       #
    # HINT: Try to formulate the l2 distance using matrix multiplication    #
    #       and two broadcast sums.                                         #
    #########################################################################
    # N_test * D
    
    test_sq = X * X
    train_sq = self.X_train * self.X_train
    # N_train * D
    # summing along pixels
    # get N_train * 1
    train_sum = np.sum(train_sq, axis = -1)
    train_sum = np.transpose(train_sum)
    train_sum = np.broadcast_to(train_sum, (num_test, num_train))

    # do the same to test_sum
    test_sum = np.sum(test_sq, axis = -1)
    test_sum = np.broadcast_to(test_sum, (num_train, num_test))
    test_sum = np.transpose(test_sum)

    # finally let's get the product
    prod = np.matmul(X, np.transpose(self.X_train))
    sq = test_sum + train_sum - 2 * prod
    dists = np.sqrt(sq)
    # print("{}s used".format((time.time() - start)))
    #########################################################################
    #                         END OF YOUR CODE                              #
    #########################################################################
    return dists

  def predict_labels(self, dists, k=1):
    """
    Given a matrix of distances between test points and training points,
    predict a label for each test point.

    Inputs:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      gives the distance betwen the ith test point and the jth training point.

    Returns:
    - y: A numpy array of shape (num_test,) containing predicted labels for the
      test data, where y[i] is the predicted label for the test point X[i].  
    """
    num_test = dists.shape[0]
    y_pred = np.zeros(num_test)
    for i in xrange(num_test):
      # A list of length k storing the labels of the k nearest neighbors to
      # the ith test point.
      closest_y = []
      #########################################################################
      # TODO:                                                                 #
      # Use the distance matrix to find the k nearest neighbors of the ith    #
      # testing point, and use self.y_train to find the labels of these       #
      # neighbors. Store these labels in closest_y.                           #
      # Hint: Look up the function numpy.argsort.                             #
      #########################################################################
      sorted = np.argsort(dists[i])
      for z in xrange(k):
        closest_y.append(self.y_train[sorted[z]])

      #########################################################################
      # TODO:                                                                 #
      # Now that you have found the labels of the k nearest neighbors, you    #
      # need to find the most common label in the list closest_y of labels.   #
      # Store this label in y_pred[i]. Break ties by choosing the smaller     #
      # label.                                                                #
      #########################################################################
      scores = {}
      for z in xrange(k):
        category = closest_y[z]
        weight = (k - z)
        if scores.get(category) is None:
          scores[category] = weight + (k * 3)
        else:
          scores[category] = scores[category] + weight + (k * 3)

      max_category = None
      for (cat, score) in scores.items():
        if score > scores.get(max_category, 0):
          max_category = cat
      y_pred[i] = max_category
      #########################################################################
      #                           END OF YOUR CODE                            # 
      #########################################################################

    return y_pred

