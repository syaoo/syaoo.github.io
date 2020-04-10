echo --- add file and commit ---
git add . && git commit -m 'update'
echo --- push origin master:master ---
git push origin master:master
echo Done!的
read -n1 -p "Press any key to continue..."