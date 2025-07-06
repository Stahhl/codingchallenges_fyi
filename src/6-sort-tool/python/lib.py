# lib.py
from __future__ import annotations
import heapq
import os
import hashlib
import hmac

def _merge_sort(arr: list[str]) -> list[str]:
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        _merge_sort(L)
        _merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def _quicksort(arr: list[str]) -> list[str]:
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return _quicksort(left) + middle + _quicksort(right)


def _heapsort(arr: list[str]) -> list[str]:
    h = []
    for value in arr:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for _ in range(len(h))]

def _radix_sort(arr: list[str]) -> list[str]:
    if not arr:
        return []
    max_len = len(max(arr, key=len))

    # Pad strings to have the same length
    padded_arr = [s.ljust(max_len) for s in arr]

    for i in range(max_len - 1, -1, -1):
        buckets = [[] for _ in range(256)] # Assuming ASCII
        for s in padded_arr:
            buckets[ord(s[i])].append(s)
        padded_arr = [s for bucket in buckets for s in bucket]

    # Remove padding
    return [s.rstrip() for s in padded_arr]

def _random_sort(arr: list[str]) -> list[str]:
    """
    Sorts a list of strings in a random order, keeping equal keys together.
    This is achieved by sorting based on a randomized hash of each string.
    """
    # Get a random key for the HMAC function. os.urandom is preferred for cryptographic randomness.
    random_key = os.urandom(16)

    def get_hash(item: str) -> bytes:
        """Computes the HMAC-SHA256 hash of the item."""
        return hmac.new(random_key, item.encode('utf-8'), hashlib.sha256).digest()

    # Sort the array based on the hash of each element.
    # Elements with the same value will have the same hash, so they stay grouped.
    return sorted(arr, key=get_hash)


def sort_words(words: list[str], algorithm: str = 'timsort') -> list[str]:
  """
  Sorts a list of words lexicographically using a specified algorithm.

  Args:
    words: A list of strings.
    algorithm: The sorting algorithm to use. One of 'timsort' (default), 
               'radix', 'merge', 'quick', 'heap', or 'random'.

  Returns:
    A new list of strings, sorted lexicographically.
  """
  # Make a copy to avoid modifying the original list for in-place sorts
  words_copy = words.copy()
  if algorithm == 'timsort':
      # sorted() uses Timsort
      return sorted(words_copy)
  elif algorithm == 'radix':
      return _radix_sort(words_copy)
  elif algorithm == 'merge':
      return _merge_sort(words_copy)
  elif algorithm == 'quick':
      return _quicksort(words_copy)
  elif algorithm == 'heap':
      return _heapsort(words_copy)
  elif algorithm == 'random':
      return _random_sort(words_copy)
  else:
      raise ValueError(f"Unknown sorting algorithm: {algorithm}")
