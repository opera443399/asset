#!/bin/bash
# 
# execute shell for jenkins
# 2017/4/6

# setup
d_root='/opt/asset'
d_target="${d_root}/src_$(date +%Y%m%d_%H%M%S)"
d_link="${d_root}/latest"
sudo mkdir -p ${d_target}

# deploy
sudo rsync -av ../asset/ --exclude=".git/" ${d_target}/
sudo rm -fv ${d_link}
sudo ln -sv ${d_target} ${d_link}
sudo /bin/bash ${d_link}/ctl.sh c
sudo /bin/bash ${d_link}/ctl.sh t
sudo /bin/bash ${d_link}/ctl.sh r

# cleanup
echo "[-] List dir:"
sudo ls -l ${d_root}
echo "[-] File was last accessed n*24 hours ago:"
sudo find ${d_root} -maxdepth 1 -atime +7 -print |sort
sudo find ${d_root} -maxdepth 1 -atime +7 -exec rm -fr {} \;
echo "[-] List dir again:"
sudo ls -l ${d_root}