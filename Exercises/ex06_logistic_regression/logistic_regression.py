# -*- coding: utf-8 -*-

__author__ = "Petter Hetland"
__email__ = "pehe@nmbu.no"


import numpy as np
from numpy import exp
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.exceptions import NotFittedError
from sklearn.utils import check_random_state, check_X_y


def sigmoid(z):
    r"""Perform a logistic transform on the input.

    This function applies the sigmoidal function element-wise to all
    elements of `z`. The sigmoidal function is on the following form:

    .. math::

        \frac{1}{1 + exp(-\mathbf{z})}.

    Parameters
    ----------
    z : np.ndarray
        Logit to transform.

    Returns
    -------
    sigmoidal_transformed_z : np.ndarray
        Transformed input.
    """
    sigmoidal_transformed_z = 1 / (1 + np.exp(-z))
    return sigmoidal_transformed_z


def predict_proba(coef, X):
    r"""Predict the class probabilities for each data point in :math:`X`.

    Estimate which class each data point in X corresponds to. This is done
    according to the following formula.

    .. math::

        \hat{y}_i = \sigma(\mathbf{x}_i^T \mathbf{w}),

    where :math:`x_i` is the i-th row in :math:`X` and :math:`\sigma` is
    the sigmoidal function. Alternatively, in matrix-vector form:

    .. math::

        \hat{\mathbf{y}} = \sigma(X \mathbf{w}).

    Parameters
    ----------
    coef : np.ndarray(shape=(r,))
        The weight vector, :math:`w`
    X : np.ndarray(shape=(n, r))
        The data matrix (aka design or measurement matrix)

    Returns
    -------
    p : np.ndarray(shape(n,))
        The predicted class probabilities.
    """
    p = sigmoid((X @ coef))

    return p


def logistic_gradient(coef, X, y):
    r"""Returns the gradient of a logistic regression model.

    The gradient is given by

    .. math::

        \nabla_w L(\mathbf{w}; X, \mathbf{y}) = \sum_i \mathbf{x}_i (y_i - \hat
        {y}_i),

    or, elementwise,

    .. math::

        \left[\nabla_w L(\mathbf{w}; X, \mathbf{y})\right]_j = \frac{\partial
        L}{\partial w_j}
                                     = \sum_i X_{ij} (y_i - \hat{y}_i),

    where :math:`\hat{y}_i` is the predicted value for data point
    :math:`i` and is given by :math:`\sigma(x_i^Tw)`, where
    :math:`\sigma(z)` is the sigmoidal function.

    Parameters
    ----------
    coef : np.ndarray(shape=(r,))
        The weight vector, :math:`w`
    X : np.ndarray(shape=(n, r))
        The data matrix (aka design or measurement matrix)
    y : np.ndarray(shape=(n,))
        The true class labels for each data point.

    Returns
    -------
    gradient : np.ndarray(shape=(r,))
        The gradient of the cross entropy loss related to the linear
        logistic regression model.
    """
    y_hat = sigmoid(X @ coef)
    residual = y_hat - y

    gradient = X.T @ residual
    return gradient


class LogisticRegression(BaseEstimator, ClassifierMixin):
    """A logistic regression classifier that follows the scikit-learn API.

    Note that the ``__init__`` method of scikit-learn estimators should not do
    any logic or input validation. This is all taken care of in the ``fit``
    method. 

    Parameters
    ----------
    max_iter : int (default=1000)
        Maximum number of gradient descent iterations to run.
    tol : float (default=1e-5)
        The gradient descent iterations will converge when the gradient
        norm is less than this.
    learning_rate : float (default=0.01)
        The step-size for the gradient descent updates.
    random_state : np.random.random_state or int or None (default=None)
        A numpy random state object or a seed for a numpy random state object.

    Attributes
    ----------
    coef_ : np.ndarray(shape=(r,))
        The logistic regression weights (initialised in ``self.fit``)
    max_iter : int (default=1000)
        Maximum number of gradient descent iterations to run.
    tol : float (default=1e-5)
        The gradient descent iterations will converge when the gradient
        norm is less than this.
    learning_rate : float (default=0.01)
        The step-size for the gradient descent updates.
    random_state : np.random.random_state or int or None (default=None)
        A numpy random state object or a seed for a numpy random state object.
    """

    def __init__(
        self, max_iter=1000, tol=1e-5, learning_rate=0.01, random_state=None
    ):
        """Initialise a logistic regression instance.

        The ``__init__`` method of scikit-learn estimators should not do any
        logic or input validation. This is all taken care of in the ``fit``
        method. 

        Parameters
        ----------
        max_iter : int (default=1000)
            Maximum number of gradient descent iterations to run.
        tol : float (default=1e-5)
            The gradient descent iterations will converge when the gradient
            norm is less than this.
        learning_rate : float (default=0.01)
            The step-size for the gradient descent updates.
        random_state : np.random.random_state or int or None (default=None)
            A numpy random state object or a seed for a numpy random state
            object.
        """
        self.max_iter = max_iter
        self.tol = tol
        self.learning_rate = learning_rate
        self.random_state = random_state

    def _has_converged(self, coef, X, y):
        r"""Whether the gradient descent algorithm has converged.

        Returns True if the norm of the gradient is smaller than ``self.tol``,
        mathematically, that is

        .. math::

            ||\nabla_w L(\mathbf{w}^{(k)}; X, \mathbf{y})|| < T

        where :math:`\nabla_w L` is the gradient of the loss function,
        :math:`|| \mathbf{v} ||` is the norm of the vector :math:`\mathbf{v}`,
        :math:`\mathbf{w}^{(k)}` is the weights at iteration ``k``, and
        :math:`T` is the convergence tolerance (``self.tol``).

        Parameters
        ----------
        coef : np.ndarray(shape=(r,))
            The weight vector, :math:`\mathbf{w}^{(k)}`
        X : np.ndarray(shape=(n, r))
            The data matrix (aka design or measurement matrix)
        y : np.ndarray(shape=(n,))
            The true class labels for each data point.

        Returns
        -------
        has_converged : bool
            True if the convergence criteria above is met, False otherwise.
        """
        gradient_norm = np.linalg.norm(logistic_gradient(coef, X, y))

        return gradient_norm < self.tol

    def _fit_gradient_descent(self, coef, X, y):
        r"""Fit the logisitc regression model to the data given initial weights

        Gradient descent works by iteratively applying the following update
        rule

        .. math::

            \mathbf{w}^{(k)} \gets \mathbf{w}^{(k-1)} - \eta \nabla L(\mathbf
            {w}^{(k-1)}; X, \mathbf{y}),

        where :math:`\mathbf{w}^{(k)}` is the coefficient vector at iteration 
        ``k``, :math:`\mathbf{w}^{(k-1)}` is the coefficient vector at 
        iteration k-1, :math:`\eta` is the learning rate and 
        :math:`\nabla L(\mathbf{w}^{(k-1)}; X, \mathbf{y})` is the gradient of
        the loss function at iteration k-1.

        The iterative algorithm should be performed for at most
        ``self.max_iter`` iterations, or until the convergence criteria is
        reached.

        Parameters
        ----------
        coef : np.ndarray(shape=(r,))
            The initial guess for the coefficient vector.
            May be modified inplace by the method.
        X : np.ndarray(shape=(n, r))
            The data matrix
        y : np.ndarray(shape=(n,))
            The target vector

        Returns
        -------
        coef : np.ndarray(shape=(n,))
            The logistic regression weights
        """
        coef_ = coef

        for _ in range(self.max_iter):
            coef_ = coef_ - self.learning_rate * logistic_gradient(coef_, X, y)

            if self._has_converged(coef_, X, y):
                print("The model has converged!")
                break

        return coef_

    def fit(self, X, y):
        """Fit a logistic regression model to the data.
        Parameters
        ----------
        X : np.ndarray(shape=(n, r))
            The data matrix
        y : np.ndarray(shape=(n,))
            The observed classes for each data point in X.
        """
        # This function ensures that X and y has acceptable data types
        # and flattens y to have shape (n,) if it has shape (n, 1)
        X, y = check_X_y(X, y, order="C")

        if any((y < 0) | (y > 1)):
            raise ValueError("Only y-values between 0 and 1 are accepted.")

        # A random state is a random number generator, akin to those
        # you made in earlier coursework. It has all functions of
        # np.ranom, but its sequence of random numbers is not affected
        # by calls to np.random.
        random_state = check_random_state(self.random_state)
        coef_guess = random_state.standard_normal(X.shape[1])

        self.coef_ = self._fit_gradient_descent(coef_guess, X, y)
        return self

    def predict_proba(self, X):
        """Estimate the class probabilities.

        This function returns the probability that each datapoint belongs to
        the positive class.

        Parameters
        ----------
        X : np.ndarray
            The data matrix.

        Returns
        -------
        p : np.ndarray
            A vector of probabilities. The i-th entry is the probability for
            the i-th data point belonging to the positive class.
        """
        if not hasattr(self, "coef_"):
            raise NotFittedError("Call fit before prediction")
        return predict_proba(self.coef_, X)

    def predict_log_proba(self, X):
        """Estimate the class log probabilities.

        This function returns the probability that each datapoint belongs to
        the positive class.

        Parameters
        ----------
        X : np.ndarray
            The data matrix.

        Returns
        -------
        lp : np.ndarray
            A vector of log probabilities. The i-th entry is the log
            probability for the i-th data point belonging to the positive
            class.
        """
        return np.log(self.predict_proba(X))

    def predict(self, X):
        """Predict whether each data point in X belongs to the positive class

        Parameters
        ----------
        X : np.ndarray
            Data matrix

        Returns
        -------
        yhat : np.ndarray
            Predicted classes for the input data matrix. len(yhat) == len(X)
        """
        return self.predict_proba(X) >= 0.5


if __name__ == "__main__":
    # Simulate a random dataset
    X = np.random.standard_normal((100, 5))
    coef = np.random.standard_normal(5)
    y = predict_proba(coef, X) > 0.5

    # Fit a logistic regression model to the X and y vector
    # Create a logistic regression object and fit it to the dataset
    lr_model = LogisticRegression()
    lr_model.fit(X, y)

    # Print performance information
    print(f"Accuracy: {lr_model.score(X, y)}")
    print(f"True coefficients: {coef}")
    print(f"Learned coefficients: {lr_model.coef_}")
