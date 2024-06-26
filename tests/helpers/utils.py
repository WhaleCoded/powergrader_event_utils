from typing import Any, List, Tuple

import itertools

VALID_UUIDS = [
    "123",
    None,
    "this is a really long super annoying string which is still a valid uuid for our particular use case",
]
INVALID_UUIDS = [
    -1,
    25.0,
    ["a", "b", "c"],
    {"a": "b"},
]

VALID_STRS = [
    None,
    "0",
    "this is a really long super annoying string which is still a valid uuid for our particular use case",
    "\n",
]
INVALID_STRS = [1, -1.0, [1, 2, 3], {"a": "b"}]

VALID_TIMESTAMPS = [1, 1234567890, 9876543210]
INVALID_TIMESTAMPS = [-1, -1.0, [1, 2, 3], b"123", {"a": "b"}, "10"]

VALID_INTS = [None, 1, 1234567890, 4294967295]
INVALID_INTS = [-1, -1.0, [1, 2, 3], b"123", {"a": "b"}, "10"]


def generate_all_permutations(*lists) -> List[Tuple[Any]]:
    return list(itertools.product(*lists))


def generate_singularly_invalid_permutations(
    valid_lists, invalid_lists
) -> List[Tuple[Any]]:
    assert len(valid_lists) == len(
        invalid_lists
    ), "Valid and invalid lists must be the same length"
    permutations = []
    for invalid_index in range(len(valid_lists)):
        lists_with_single_invalid = [
            valid_lists[idx] if idx != invalid_index else invalid_lists[idx]
            for idx in range(len(valid_lists))
        ]
        permutations.extend(list(itertools.product(*lists_with_single_invalid)))
    return permutations


class MockProducer:
    was_called: bool

    def __init__(self, *args, **kwargs):
        self.was_called = False

    def produce(self, topic_name, key, value, headers):
        self.was_called = True
        assert isinstance(topic_name, str)
        assert isinstance(key, (str, bytes, type(None)))
        assert isinstance(value, bytes)
        # Ensure that the headers are a dictionary of strings to (str, bytes, None)
        assert isinstance(headers, dict)
        for header_key, header_value in headers.items():
            assert isinstance(header_key, str)
            assert isinstance(header_value, (str, bytes, type(None)))
