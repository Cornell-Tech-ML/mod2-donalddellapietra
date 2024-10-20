# from typing import Callable, Iterable, List, Tuple

# from hypothesis import given
# from hypothesis.strategies import DataObject, data, lists, permutations

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
    print((1,) * (len(a.shape) - len(b.shape)) + b.shape)

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
    print(a.sum(0))

    t = minitorch.tensor([[2, 3], [4, 6], [5, 7]])
    print(t.all(0))


def test_neg_backward():
    # a = minitorch.tensor([1.0, -5.0, 3.0], requires_grad=True)
    # a.sum().backward()
    # print(a.grad)

    a = minitorch.tensor([1.0, -2.0, 3.0], requires_grad=True)

    # Perform the negation operation

    b = -a

    b.sum().backward()
    print(a.grad)


def test_view() -> None:
    a = minitorch.tensor([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    # print(a.shape)
    # a = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    print(a.log())
    print(a.shape)
    print(a.view((2, 3)))


def test_mean() -> None:
    b = minitorch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
    mean_value = b.mean(dim=None)
    print(mean_value)
    # Perform backward pass to compute gradients
    mean_value.backward()
    print(b.grad)
    mean_value = b.mean(dim=1)
    print(mean_value)
    mean_value = b.mean(dim=0)
    print(mean_value)

    # a = mean_value.sum().backward()


def test_permute():
    # Create a 3D tensor
    # a = minitorch.tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    # print("Original tensor:")
    # print(a)
    # print("Shape:", a.shape)

    # # Permute the dimensions
    # b = a.permute((2, 0, 1))
    # print("\nPermuted tensor (2, 0, 1):")
    # print(b)
    # print("Shape:", b.shape)

    # # Test with a different permutation
    # c = a.permute((1, 2, 0))
    # print("\nPermuted tensor (1, 2, 0):")
    # print(c)
    # print("Shape:", c.shape)

    def reverse_permutation(perm):
        n = len(perm)
        reversed_perm = [0] * n
        for i in range(n):
            reversed_perm[perm[i]] = i
        return reversed_perm

    # Test permute with gradient
    # Create a tensor with shape 3, 2, 4
    d = minitorch.tensor(
        [
            [[1, 2, 3, 4], [5, 6, 7, 8]],
            [[9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24]],
        ],
        requires_grad=True,
    )
    print("Original tensor shape:", d.shape)
    # print(d)
    # d = minitorch.tensor([[[1., 2.], [3., 4.]], [[5., 6.], [7., 8.]]], requires_grad=True)
    # print("shape1")
    # print(d.shape)
    e = d.permute(2, 0, 1)
    print("shape")
    print(e.shape)
    print(reverse_permutation((2, 0, 1)))
    # 0  2  1
    # print(d.permute(0, 2, 1))

    e.sum().backward()
    print("\nGradient after permute and sum:")
    print(d.grad)


def test_nir():
    d = minitorch.tensor(
        [
            [[1, 2, 3, 4], [5, 6, 7, 8]],
            [[9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24]],
        ],
        requires_grad=True,
    )
    print(d.shape)
    print(d.view((3 * 2 * 4)))
    print(d.sum(1).shape)
    print(d.shape)


import torch


def test_matmul():
    # array_1 = [[[1], [2]],
    #     [[3], [4]],
    #     [[5], [6]],
    #     [[7], [8]]
    # ]
    # array_2 = [
    #     [[1, 2, 3],
    #     [4, 5, 6]]
    # ]

    array_1 = [[[1], [2]], [[3], [4]], [[5], [6]], [[7], [8]]]
    array_2 = [[[1, 2, 3], [4, 5, 6]]]

    # Create a tensor of shape 4 x 2 x 1
    tensor_1 = torch.tensor(array_1)
    tensor_1 = tensor_1.view(4, 2)

    # Create a tensor of shape 1 x 2 x 3
    tensor_2 = torch.tensor(array_2)
    tensor_2 = tensor_2.view(2, 3)

    print(tensor_1.shape)
    print(tensor_2.shape)

    print(tensor_1 @ tensor_2)

    tensor1 = minitorch.tensor(array_1)
    tensor2 = minitorch.tensor(array_2)

    c = (tensor1 * tensor2).sum(1)
    # print(c)

    tensor1 = minitorch.tensor([[1, 2], [3, 4], [5, 6], [7, 8]])

    # Create a 2x3 tensor
    tensor2 = minitorch.tensor([[1, 2, 3], [4, 5, 6]])

    print(tensor1.shape)
    print(tensor2.shape)

    a = tensor1.view((tensor1.shape[0], tensor1.shape[1], 1))
    b = tensor2.view((1, tensor2.shape[0], tensor2.shape[1]))

    c = (a * b).sum(1).view((4, 3))

    print(c)


def test_expand():
    tensor2 = minitorch.tensor([[1, 2, 3], [4, 5, 6]])
    print(tensor2.shape)
    print(tensor2.expand((2, 3, 6)))


if __name__ == "__main__":
    test_expand()
    pass

    # test_matmul()
    # test_permute()
    # test_mean()
    # test_manual()
    # test_sum()
    # test_neg_backward()
    # test_add_backward()
