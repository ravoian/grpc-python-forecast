call python -m pip install requests
call python -m pip install bs4
echo 0 | call gen_proto.bat 
start cmd /k run_server.bat
start cmd /k run_client.bat
@pause