from cx_Freeze import setup, Executable
 
setup(
    name = "main",
    version = "0.1",
    description = "a test",
    executables = [Executable(script = "main.py", base = "win32GUI")]
    )