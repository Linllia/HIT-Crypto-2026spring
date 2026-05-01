chr1 = " ".encode("ascii")
chr2 = "B".encode("ascii")

a = bytes([i ^ j for i, j in zip(chr1, chr2)])
print(a)
