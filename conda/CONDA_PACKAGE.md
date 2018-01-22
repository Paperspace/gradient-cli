Conda Setup
-----------
(from: https://conda.io/docs/user-guide/install/linux.html )

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod a+x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
export PATH=~/miniconda3/bin:$PATH

(from: https://conda.io/docs/user-guide/tutorials/build-pkgs-skeleton.html )

conda install conda-build
conda install anaconda-client


Conda Package Build
-------------------
conda update conda
conda update conda-build

cd python3

conda-build paperspace

conda build purge


Upload Package to Anaconda.org
------------------------------
anaconda login

anaconda upload /home/sanfilip/miniconda3/conda-bld/linux-64/paperspace-X.X.X-py36_0.tar.bz2

anaconda logout

