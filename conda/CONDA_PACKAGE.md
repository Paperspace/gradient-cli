Conda Setup
-----------
(from: https://conda.io/docs/user-guide/install/linux.html )

(for python3)
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod a+x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
export PATH=~/miniconda3/bin:$PATH

-or-

(for python2)
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
chmod a+x Miniconda2-latest-Linux-x86_64.sh
./Miniconda2-latest-Linux-x86_64.sh
export PATH=~/miniconda2/bin:$PATH

(from: https://conda.io/docs/user-guide/tutorials/build-pkgs-skeleton.html )

conda install conda-build
conda install anaconda-client


Conda Package Build
-------------------
cd ~/sdk/paperspace-python/conda

bash
export PATH=~/miniconda3/bin:$PATH
conda update conda
conda update conda-build

(if not exists:)
mkdir python3
-or-
mkdir python2

cd python3
-or-
cd python2

(if exists:)
mv paperspace paperspace.bak
conda skeleton pypi paperspace

cd paperspace

wget https://conda.io/docs/_downloads/build1.sh
wget https://conda.io/docs/_downloads/bld.bat
chmod a+x build1.sh

sed -i -e "s/requests\[security\]/requests/g" meta.yaml
sed -i -e "/^  description: /,/^  doc_url: ''/c\  description: \"Paperspace Python\"\n  doc_url: ''" meta.yaml

cd ..

conda-build paperspace


Upload Package to Anaconda.org
------------------------------
anaconda login

anaconda upload ~/miniconda3/conda-bld/linux-64/paperspace-X.X.X-py36_0.tar.bz2
-or-
anaconda upload ~/miniconda3/conda-bld/linux-64/paperspace-X.X.X-py27_0.tar.bz2

anaconda logout


Cleanup
-------
conda build purge

(if exists:)
rm -Rf paperspace.bak

