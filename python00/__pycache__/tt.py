import marshal
import dis

with open("ft_count_harvest_iterative.cpython-310.pyc", "rb") as f:
    f.read(16)  # skip header (Python-version dependent)
    code = marshal.load(f)

dis.dis(code)
