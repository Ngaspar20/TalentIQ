Dim shell, dir
Set shell = CreateObject("WScript.Shell")
dir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))
shell.Run """" & dir & "python\pythonw.exe"" """ & dir & "app\launcher.py""", 0, False
