# How to install

- Find latest distribution https://www.anaconda.com/distribution/ (example used Anaconda3-2019.10-Linux-x86_64.sh)
- cd /tmp
- curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
- bash Anaconda3-2019.10-Linux-x86_64.sh
- source ~/.bashrc
- conda create --name myEnv python=3 
  - (to create python 3 environment)
- conda activate myEnv / conda deactivate
- conda install --file requirements.txt 
- pip install python-resize-image
- pip install glob3

# Download Fonts

- mkdir fonts
- cd fonts
- curl -O https://www.fontmirror.com/app_public/files/t/1/Helvetica_33244fbeea10f093ae87de7a994c3697.ttf
- curl -O https://github.com/huuphongnguyen/cereal-airbnb-font/raw/master/AirbnbCereal-Book.ttf