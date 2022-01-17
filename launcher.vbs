Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c run_coro.bat"
oShell.Run strArgs, 0, false