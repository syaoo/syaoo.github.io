@echo off
echo --- add file and commit ---
git add . && git commit -m 'update'
echo --- push origin master:master ---
git push origin master:master
echo Done!的
pause
