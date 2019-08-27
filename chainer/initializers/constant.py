import numpy

import chainer
from chainer import backend
from chainer import initializer
from chainer import types  # NOQA


class Identity(initializer.Initializer):

    """Initializes array with the identity matrix.

    It initializes the given array with the constant
    multiple of the identity matrix.
    Note that arrays to be passed must be 2D squared matrices.

    Attributes:
        scale (scalar): A constant to be multiplied to identity matrices.

    """

    def __init__(self, scale=1.0, dtype=None):
        self.scale = scale
        super(Identity, self).__init__(dtype)

    def __call__(self, array):
        if self.dtype is not None:
            assert array.dtype == self.dtype
        shape = array.shape
        if len(shape) != 2 or shape[0] != shape[1]:
            raise ValueError('Identity matrix initialization can only be used '
                             'for 2D squared matrices.')

        device = backend.get_device_from_array(array)
        array[...] = device.xp.identity(shape[0]) * self.scale


class _Constant(initializer.Initializer):

    fill_value = None  # type: types.ScalarValue

    def __init__(self, dtype=None):
        if not (isinstance(self.fill_value, chainer.get_array_types())
                or numpy.isscalar(self.fill_value)):
            raise ValueError(
                'fill_value must be either scalar, numpy.ndarray, '
                'cupy.ndarray or chainerx.ndarray.')
        super(_Constant, self).__init__(dtype)

    def __call__(self, array):
        if self.dtype is not None:
            assert array.dtype == self.dtype

        # Calling copy to ensures that the fill_value array
        # is moved to the device where array resides
        if isinstance(self.fill_value, chainer.get_array_types()):
            backend.copyto(array, self.fill_value)
        else:
            device = backend.get_device_from_array(array)
            array[...] = device.xp.asarray(self.fill_value)


class Constant(_Constant):

    """Initializes array with constant value.

    Attributes:
        ~Constant.fill_value (scalar or :ref:`ndarray`):
            A constant to be assigned to the initialized array.
            Broadcast is allowed on this assignment.
        dtype: Data type specifier.

    """

    def __init__(self, fill_value, dtype=None):
        self.fill_value = fill_value
        super(Constant, self).__init__(dtype)


class Zero(_Constant):
    """Initializes array to all-zero.

    Attributes:
        ~Zero.dtype: Data type specifier.
    """

    fill_value = 0.0


class One(_Constant):
    """Initializes array to all-one.

    Attributes:
        ~One.dtype: Data type specifier.
    """

    fill_value = 1.0


class NaN(_Constant):
    """Initializes array to all-NaN.

    Attributes:
        ~NaN.dtype: Data type specifier.
    """

    fill_value = numpy.nan
