python -m venv env 
./env/Scripts/activate
pip install -r requirement.txt
echo "cd $pwd" | Out-File -FilePath ./resave.ps1
echo ".\env\Scripts\Activate.ps1" | Out-File -FilePath ./resave.ps1 -Append
echo "python .\resave.py" | Out-File -FilePath ./resave.ps1 -Append
echo "Use the resave.ps1 as a shortcut"
