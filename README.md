# rtx2mnc_py
Converts an Dicom RTX struct to minc

## Authors
Rigshospitalet
  - Claes Ladefoged <claes.noehr.ladefoged@regionh.dk>

## Installation:
<pre><code>
cp rtx2mnc.py /usr/local/bin
</code></pre>

## Usage:
<pre><code>
rtx2mnc < VOLUME.mnc > < RTx > < out_label.mnc >
      	
      	< VOLUME.mnc > is the file which the RTx was defined on.
      	< RTx > is the RT struct in DICOM format.
      	< out_label.mnc > is the resulting MINC file with the contours in the RT file set to 1. If more than one struct, out_label will be suffixed by a running number.
</code></pre>

## Requires/Dependencies:
 - MINC tools
 - DCMTK
 - opencv2-python
 - numpy