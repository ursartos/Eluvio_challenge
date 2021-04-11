# Eluvio_challenge

Problem description:
Given a large number of binary files, write a program that finds the
longest strand of bytes that is identical between two or more files

Use the test set attached (files sample.*)

The program should display:
- the length of the strand
- the file names where the largest strand appears
- the offset where the strand appears in each file

Solution in Python:
Used Dynamic Programming and a complete graph holding all possible file pairs to determine all files with the longest byte strand.
For n files and k number of bytes in the largest file,
Time Complexity is O(n^2k^2)
Space Complexity is O(nk)
