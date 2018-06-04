# !/bin/sh

sudo apt-get update -y

sudo apt-get install -y python3-pip python3-distutils screen postgresql pgadmin3
sudo pip3 install --upgrade pip
sudo pip3 install -r requirements.txt

sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'admin';"
