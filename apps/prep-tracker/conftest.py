# server_test.py is a script: it starts a server on import and ends in
# sys.exit(), which pytest reports as an internal error. grade_test.py runs it
# as a subprocess instead.
collect_ignore = ["server_test.py"]
