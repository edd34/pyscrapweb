from ctypes import cdll
lib = cdll.LoadLibrary('./libadd.so')

def Add(a: int, b: int) -> int:
    return lib.My_Add(a, b)
