# rtx2mnc_py
Converts an Dicom RTX struct to minc

Version 1.0.0 :: 2018-03-08 :: Added basic functionality working for one or more RT-files

## Authors
Rigshospitalet
  - Claes Ladefoged <claes.noehr.ladefoged@regionh.dk>

## Installation (under /opt/bin/rtx2mnc_py):
```
git clone https://github.com/claesnl/rtx2mnc_py.git
ln -s $HOME/rtx2mnc_py/rtx2mnc.py /opt/bin/rtx2mnc_py
```

## Usage:
```
rtx2mnc_py < VOLUME.mnc > < RTx > < out_label.mnc > [ --verbose ] [ --visualize ]
      	   < VOLUME.mnc > is the file which the RTx was defined on.
      	   < RTx > is the RT struct in DICOM format.
      	   < out_label.mnc > is the resulting MINC file with the contours in the RT file set to 1. If more than one struct, out_label will be suffixed by a running number.
      	   --verbose turns on additional information
      	   --visualize shows individual slices for debugging
```

## Requires/Dependencies:
- MINC tools
- pyminc
- DCMTK
- pydicom
- opencv2-python
- numpy

## Installation of dependencies:
### MINC tools:
```
git clone --recursive https://github.com/BIC-MNI/minc-toolkit-v2.git minc-toolkit-v2
cd minc-toolkit-v2 && mkdir build && cd build
ccmake .. -DMT_BUILD_SHARED_LIBS:BOOL=ON
make && sudo make install
```

### pyminc:
```
git clone https://github.com/Mouse-Imaging-Centre/pyminc.git
cd pyminc
python setup.py install
```

### DCMTK:
```
git clone https://github.com/commontk/DCMTK.git
cd DCMTK
./configure
make all
sudo make install-all
```

### Python tools:
```
pip install pydicom opencv-python numpy
```