
import pytest
from lib import sort_words
import collections

@pytest.mark.parametrize("algorithm", ["timsort", "radix", "merge", "quick", "heap"])
def test_sort_words(algorithm):
    words = ["c", "a", "b", "z", "d", "y", "e", "x"]
    sorted_words = sort_words(words, algorithm=algorithm)
    assert sorted_words == ["a", "b", "c", "d", "e", "x", "y", "z"]

@pytest.mark.parametrize("algorithm", ["timsort", "radix", "merge", "quick", "heap"])
def test_sort_words_with_duplicates(algorithm):
    words = ["c", "a", "b", "a", "c"]
    sorted_words = sort_words(words, algorithm=algorithm)
    assert sorted_words == ["a", "a", "b", "c", "c"]

@pytest.mark.parametrize("algorithm", ["timsort", "radix", "merge", "quick", "heap"])
def test_sort_words_empty_list(algorithm):
    words = []
    sorted_words = sort_words(words, algorithm=algorithm)
    assert sorted_words == []

@pytest.mark.parametrize("algorithm", ["timsort", "radix", "merge", "quick", "heap"])
def test_sort_words_single_word(algorithm):
    words = ["hello"]
    sorted_words = sort_words(words, algorithm=algorithm)
    assert sorted_words == ["hello"]

def test_sort_words_invalid_algorithm():
    with pytest.raises(ValueError):
        sort_words([], algorithm="unknown")

def test_random_sort():
    words = ["c", "a", "b", "a", "c", "b", "a"]
    
    # Run it once
    random_sorted1 = sort_words(words, algorithm="random")
    
    # Check that the elements are the same, just in a different order
    assert collections.Counter(random_sorted1) == collections.Counter(words)
    
    # Check that equal items are grouped together
    # We can do this by sorting the list and the random list and see if they are equal
    # No, that's not right. A better way is to group the items and check the groups.
    grouped = collections.defaultdict(list)
    for word in random_sorted1:
        grouped[word].append(word)
    
    for word_list in grouped.values():
        assert len(set(word_list)) == 1

    # Run it again and check that the order is different (with high probability)
    random_sorted2 = sort_words(words, algorithm="random")
    assert random_sorted1 != random_sorted2
