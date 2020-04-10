update_time=$(date  "+%xT%X")
git pull origin master:master
echo --- add file and commit ---
echo 'update at:'${update_time}
git add . && git commit -m 'update at:'${update_time}
echo --- push origin master:master ---
git push origin master:master
echo --- Done! ---
read -n1 -p "Press any key to continue..."