apt-get -y update
apt-get -y upgrade
apt-get -y install python-qt4 python-pyside python-scipy

git clone https://github.com/pyqtgraph/pyqtgraph.git pyqtgraph
cd pyqtgraph
python setup.py install
cd ..

git clone https://github.com/petroladkin/jsonrpclib.git jsonrpclib
cd jsonrpclib
python setup.py install
cd ..

CWD=$(pwd)
python $CWD/scr/setup.py