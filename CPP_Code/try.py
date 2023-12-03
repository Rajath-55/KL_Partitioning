from ctypes import cdll

hello_lib = cdll.LoadLibrary("shared.so")
hello = hello_lib.main

hello(4, "Graph1.txt", 100, 0)
