from typing import Callable, Iterable, List, Tuple

from hypothesis import given
from hypothesis.strategies import DataObject, data, lists, permutations

# from minitorch import MathTestVariable, Tensor, grad_check, tensor

import minitorch

def test_manual() -> None:
    """Test manual test."""
    # c = minitorch.shape_broadcast((1,), (5, 5))
    # c = minitorch.shape_broadcast((1, 1), (5, 5, 5, 5))

    a = minitorch.tensor([1.0, 2.0, 3.0])
    # print(a.shape)
    b = minitorch.tensor([[4.0, 5.0, 6.0]])
    # print(b.shape)
    # print(len(a.shape))
    # print(len(b.shape))
    print((1,)* (len(a.shape) - len(b.shape)) + b.shape)

    # print(len(a.shape) < len(b.shape))
    # new_shape = (1,) * (len(a.shape) - len(b.shape)) + b.shape
    print(a.shape)
    print(b.shape)
    print(minitorch.shape_broadcast(a.shape, b.shape))

    print("new line in manual test")
    # print(minitorch.shape_broadcast(tuple([1, 2]), tuple([1])))
    # print(new_shape)

    c = a + b
    print(c)
    print(c.shape)
    d = minitorch.tensor(1.0)
    new_shape = minitorch.shape_broadcast(c.shape, d.shape)
    print(new_shape)
    print(c + d)
    # print(c.stride)


def test_sum() -> None:
    a = minitorch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    # print(a)
    print(a.sum(dim=0))
    print(a.sum(dim=1))
    print(a.sum(dim=None))

    t = minitorch.tensor([[2, 3], [4, 6], [5, 7]])
    print(t.all(0))


def test_view() -> None:
    a = minitorch.tensor([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    # print(a.shape)
    # a = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    print(a.shape)
    print(a.view((2, 3)))


if __name__ == "__main__":
    # test_manual()
    # test_sum()
    test_view()