Dim shell, dir
Set shell = CreateObject("WScript.Shell")
dir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))
shell.Run "pythonw """ & dir & "launcher.py""", 0, False
