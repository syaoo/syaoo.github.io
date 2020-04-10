update_time=date
echo --- add file and commit ---
echo 'update'${update_time}
git add . && git commit -m 'update'${update_time}
echo --- push origin master:master ---
git push origin master:master
echo --- Done! ---
read -n1 -p "Press any key to continue..."