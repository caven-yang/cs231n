import numpy as np
from random import shuffle
from past.builtins import xrange
import pdb

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  # let's compute the scores for all samples first
  (dim, num_class) = W.shape
  (num_train, dim) = X.shape
  scores = np.matmul(X, W)
  # scores is a (N, C) matrix where scores[i] is the score for the i-th sample
  for i in xrange(num_train):
    score = scores[i]
    pred_denom = np.exp(score)
    pred_denom_sum = np.sum(pred_denom)
    y_train = y[i]
    loss += (-1 * score[y_train] + np.log(pred_denom_sum))

    dW_i_c = np.broadcast_to(X[i], (num_class, dim))
    dW_i_c = np.transpose(dW_i_c)

    pred_mult = np.broadcast_to(pred_denom, W.shape) / pred_denom_sum
    masks = np.zeros(num_class)
    masks[y_train] = -1
    masks = np.broadcast_to(masks, W.shape)
    dW_i = dW_i_c * (masks +  pred_mult)
    dW = dW + dW_i
    # import pdb; pdb.set_trace()
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  
  loss = loss / num_train +  np.sum(W * W) * reg
  dW = dW / num_train + 2 * reg * W
  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scores = np.matmul(X, W)
  (num_train, dim) = X.shape
  (dim, num_class) = W.shape
  scores_exp = np.exp(scores)

  # for each sample, summing the scores_exp
  scores_sum = np.sum(scores_exp, axis = -1)

  loss += np.sum(np.log(scores_sum))
  
  
  scores_sum = np.broadcast_to(np.transpose(scores_sum), (num_class, num_train))
  scores_exp_norm = scores_exp / np.transpose(scores_sum)

  mask = np.zeros(scores_sum.shape)
  mask = np.transpose(mask)
  for i in xrange(num_train):
    mask[i][y[i]] = -1

  score_pred = mask * scores
  loss += np.sum(score_pred)
  
  scores_sum_masked = mask + scores_exp_norm
    
  
  dW = np.matmul(np.transpose(X), scores_sum_masked) 

  loss = loss / num_train + reg * np.sum(W*W)
  dW = dW / num_train + 2 * reg * W
  # import pdb; pdb.set_trace()
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

