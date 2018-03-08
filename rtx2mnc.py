import numpy as np
import dicom
from dicom.filereader import InvalidDicomError
import matplotlib.pyplot as plt
import pyminc.volumes.volumes as pyvolume
import pyminc.volumes.factory as pyminc
import argparse
import cv2
from matplotlib.path import Path

##
# RTX2MNC python script
# VERSIONS:
#  - 1.0.0 :: Basic functionality working for one or more RT-files
##
# TODO:
#  - Add RT-name in minc header
#  - Add check for MINC-file matches RTX dimensions and IDs
##

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='RTX2MNC.')
	parser.add_argument('RTX', help='Path to the DICOM RTX file')
	parser.add_argument('MINC', help='Path to the MINC container file')
	parser.add_argument('RTMINC', help='Path to the OUTPUT MINC RT file')
	parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
	parser.add_argument("--visualize", help="Show plot of slices for debugging", action="store_true")
	args = parser.parse_args()

	try:
		RTSS = dicom.read_file(args.RTX) 
		ROIs = RTSS.ROIContourSequence
		if args.verbose:
			print "Found",len(ROIs),"ROIs"

		volume = pyminc.volumeFromFile(args.MINC)

		for ROI_id,ROI in enumerate(ROIs):
			# Create one MNC output file per ROI
			RTMINC_outname = args.RTMINC if len(ROIs) == 1 else args.RTMINC[:-4] + "_" + str(ROI_id) + ".mnc"
			RTMINC = pyminc.volumeLikeFile(args.MINC,RTMINC_outname)
			contour_sequences = ROI.ContourSequence

			if args.verbose:
				print " --> Found",len(contour_sequences),"contour sequences" 

			for contour in contour_sequences:
				assert contour.ContourGeometricType == "CLOSED_PLANAR"
				
				if args.verbose:
					print "\t",contour.ContourNumber,"contains",contour.NumberOfContourPoints

				world_coordinate_points = np.array(contour.ContourData)
				world_coordinate_points = world_coordinate_points.reshape((contour.NumberOfContourPoints,3))
				current_slice = np.zeros((volume.getSizes()[1],volume.getSizes()[2]))
				voxel_coordinates_inplane = np.zeros((len(world_coordinate_points),2))
				current_slice_i = 0
				for wi,world in enumerate(world_coordinate_points):
					voxel = volume.convertWorldToVoxel([-world[0],-world[1],world[2]])
					current_slice_i = voxel[0]
					voxel_coordinates_inplane[wi,:] = [voxel[2],voxel[1]]
				current_slice_inner = np.zeros((volume.getSizes()[1],volume.getSizes()[2]),dtype=np.float)
				converted_voxel_coordinates_inplane = np.array(np.round(voxel_coordinates_inplane),np.int32)
				cv2.fillPoly(current_slice_inner,pts=[converted_voxel_coordinates_inplane],color=1)
				p = Path(voxel_coordinates_inplane)
				points = np.array(np.nonzero(current_slice_inner)).T
				grid = p.contains_points(points[:,[1,0]])
				for pi,point in enumerate(points):
					if not grid[pi]:
						# REMOVE EDGE POINT BECAUSE CENTER IS NOT INCLUDED
						current_slice_inner[point[0],point[1]] = 0 

						if args.visualize:
							plt.plot(point[1],point[0],'bx')

					elif args.visualize:
						plt.plot(point[1],point[0],'bo')

				if args.visualize:
					plt.imshow(current_slice_inner)
					plt.plot(voxel_coordinates_inplane[:,0],voxel_coordinates_inplane[:,1],'ro')
					plt.show()

				RTMINC.data[np.int(current_slice_i)] += current_slice_inner 


			# Remove even areas - implies a hole.
			RTMINC.data[RTMINC.data % 2 == 0] = 0

			RTMINC.writeFile()
			RTMINC.closeVolume()
		volume.closeVolume()

	except InvalidDicomError:
		print "Could not read DICOM RTX file",args.RTX
		exit(-1)
