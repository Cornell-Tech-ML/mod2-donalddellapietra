from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Tuple, Protocol


# ## Task 1.1
# Central Difference calculation


def central_difference(f: Any, *vals: Any, arg: int = 0, epsilon: float = 1e-6) -> Any:
    r"""Computes an approximation to the derivative of `f` with respect to one arg.

    See :doc:`derivative` or https://en.wikipedia.org/wiki/Finite_difference for more details.

    Args:
    ----
        f : arbitrary function from n-scalar args to one value
        *vals : n-float values $x_0 \ldots x_{n-1}$
        arg : the number $i$ of the arg to compute the derivative
        epsilon : a small constant

    Returns:
    -------
        An approximation of $f'_i(x_0, \ldots, x_{n-1})$

    """
    # Create a list to hold the values
    vals_list = list(vals)

    # Calculate f(x + epsilon)
    vals_list[arg] += epsilon
    f_plus = f(*vals_list)

    # Calculate f(x - epsilon)
    vals_list[arg] -= 2 * epsilon
    f_minus = f(*vals_list)

    # Compute the central difference
    return (f_plus - f_minus) / (2 * epsilon)


variable_count = 1


class Variable(Protocol):
    def accumulate_derivative(self, x: Any) -> None: ...  # noqa: D102

    @property
    def unique_id(self) -> int: ...  # noqa: D102

    def is_leaf(self) -> bool: ...  # noqa: D102

    def is_constant(self) -> bool: ...  # noqa: D102

    @property
    def parents(self) -> Iterable["Variable"]: ...  # noqa: D102

    def chain_rule(self, d_output: Any) -> Iterable[Tuple[Variable, Any]]: ...  # noqa: D102


def topological_sort(variable: Variable) -> Iterable[Variable]:
    """Computes the topological order of the computation graph.

    Args:
    ----
        variable: The right-most variable

    Returns:
    -------
        Non-constant Variables in topological order starting from the right.

    """
    visited = set()
    sorted_variables = []

    def dfs(v: Variable) -> None:
        if v.is_constant():
            return
        if v.unique_id in visited:
            return
        visited.add(v.unique_id)
        for parent in v.parents:
            dfs(parent)
        sorted_variables.append(v)

    dfs(variable)
    return reversed(sorted_variables)


def backpropagate(variable: Variable, deriv: Any) -> None:  # noqa: D417
    """Runs backpropagation on the computation graph in order to
    compute derivatives for the leave nodes.

    Args:
    ----
        variable: The right-most variable
        deriv  : Its derivative that we want to propagate backward to the leaves.

    No return. Should write to its results to the derivative values of each leaf through `accumulate_derivative`.

    """
    # Implement backpropagation
    sorted_variables = list(topological_sort(variable))

    # Initialize gradients
    gradients = {variable: deriv}

    # Iterate through variables in topological order
    for var in sorted_variables:
        if var.is_leaf():
            var.accumulate_derivative(gradients[var])
        else:
            # Compute gradients for parent variables
            for parent, grad in var.chain_rule(gradients[var]):
                if parent not in gradients:
                    gradients[parent] = grad
                else:
                    gradients[parent] += grad


@dataclass
class Context:
    """Context class is used by `Function` to store information during the forward pass."""

    no_grad: bool = False
    saved_values: Tuple[Any, ...] = ()

    def save_for_backward(self, *values: Any) -> None:
        """Store the given `values` if they need to be used during backpropagation."""
        if self.no_grad:
            return
        self.saved_values = values

    @property
    def saved_tensors(self) -> Tuple[Any, ...]:
        """Returns the saved tensors"""
        return self.saved_values
