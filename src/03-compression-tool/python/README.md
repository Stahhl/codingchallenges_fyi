https://codingchallenges.fyi/challenges/challenge-huffman

# Usage
Compress
```
python3 main.py ./test.txt ./compressed --mode compress 
```
Decompress
```
python3 main.py ./compressed ./decompressed.txt --mode decompress
```
Run pytests tests
```
python3 -m pytest
```
# Thoughts
Managed to get the file size down from 3.4MB to 1.9MB. Which seems low but the challenge doesnt really mention desired file size. Might research a bit...