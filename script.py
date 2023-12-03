import subprocess

file_path_1 = './CPP Code/a.out'
file_path_2 = './Python Code/opticalKL.py'
cmd_py = ["python3 ", file_path_2, " Graph2.txt", " 100 0 | grep 'cost in'"]
cmd_cpp = [file_path_1, " Graph2.txt 100 0 | grep 'cost in'"]
# output = subprocess.Popen( cmd_cpp, stdout=subprocess.PIPE ).communicate()[0]
output_py = subprocess.Popen( cmd_py, stdout=subprocess.PIPE ).communicate()[0]
# print(output)
print(output_py)

