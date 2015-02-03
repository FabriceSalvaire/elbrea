    ##############################################

    def process_images_track(self, input_image):

        height, width = input_image.shape[:2]
        height_mb = int(math.ceil(height/2.)*2)
        width_mb = int(math.ceil(width/64.)*64)

        src_image = np.zeros((height_mb, width_mb), dtype=input_image.dtype)
        src_image[:height,:width] = input_image[:,:,1]

        filtered_image = np.array(src_image)
        # CvTools.alternate_sequential_filter(src_image, filtered_image,
        #                                     1,
        #                                     lambda radius: CvTools.vertical_structuring_element(radius),
        #                                     open_first=True)

        # image = np.array(input_image, dtype=np.uint64)
        # image[:,1:-1] += input_image[:,:-2]
        # image[:,1:-1] += input_image[:,2:]
        # image[:,:] /= 3
        # input_image[...] = image[...]

        marker_image = np.array(src_image)
        tmp_image = np.array(src_image)
        cv2.subtract(filtered_image, 50, marker_image)

        mask_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        marker_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        # height_mb = mask_mb.mbIm.height
        # width_mb = mask_mb.mbIm.width
        MambaTools.cv2mamba(marker_image, marker_mb)
        MambaTools.cv2mamba(filtered_image, mask_mb)
        mc.geodesy.build(marker_mb, mask_mb)
        MambaTools.mamba2cv(marker_mb, filtered_image)

        #CvTools.morphology_open(filtered_image, filtered_image, CvTools.circular_structuring_element(6))
        #CvTools.morphology_open(filtered_image, marker_image, CvTools.horizontal_structuring_element(6))
        CvTools.morphology_open(filtered_image, marker_image, CvTools.vertical_structuring_element(10))

        MambaTools.cv2mamba(marker_image, marker_mb)
        MambaTools.cv2mamba(filtered_image, mask_mb)
        mc.geodesy.build(marker_mb, mask_mb)
        MambaTools.mamba2cv(marker_mb, tmp_image)

        filtered_image -= tmp_image

        CvTools.morphology_open(filtered_image, marker_image, CvTools.horizontal_structuring_element(7))

        MambaTools.cv2mamba(marker_image, marker_mb)
        MambaTools.cv2mamba(filtered_image, mask_mb)
        mc.geodesy.build(marker_mb, mask_mb)
        MambaTools.mamba2cv(marker_mb, filtered_image)

        # CvTools.alternate_sequential_filter(filtered_image, filtered_image,
        #                                     2,
        #                                     lambda radius: CvTools.horizontal_structuring_element(radius),
        #                                     open_first=True)

        # input_image[:,:,:] = 0
        for i in xrange(3):
            input_image[:,:,i] = filtered_image[:height,:width]
            
        return input_image

####################################################################################################
####################################################################################################
####################################################################################################

    def process_images(self):

        height, width = self.front_image.shape[:2]
        height_mb = int(math.ceil(height/2.)*2)
        width_mb = int(math.ceil(width/64.)*64)

        src_image = np.zeros((height_mb, width_mb), dtype=self.front_image.dtype)
        src_image[:height,:width] = self.front_image[:,:,1]

        filtered_image = np.array(src_image)
        # CvTools.alternate_sequential_filter(src_image, filtered_image,
        #                                     1,
        #                                     lambda radius: CvTools.vertical_structuring_element(radius),
        #                                     open_first=True)

        # image = np.array(self.front_image, dtype=np.uint64)
        # image[:,1:-1] += self.front_image[:,:-2]
        # image[:,1:-1] += self.front_image[:,2:]
        # image[:,:] /= 3
        # self.front_image[...] = image[...]

        sub_image = np.array(src_image)
        cv2.subtract(filtered_image, 50, sub_image)

        mask_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        marker_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        # height_mb = mask_mb.mbIm.height
        # width_mb = mask_mb.mbIm.width
        MambaTools.cv2mamba(filtered_image, mask_mb)
        MambaTools.cv2mamba(sub_image, marker_mb)
        mc.geodesy.build(marker_mb, mask_mb)
        MambaTools.mamba2cv(marker_mb, filtered_image)

        # CvTools.alternate_sequential_filter(filtered_image, filtered_image,
        #                                     2,
        #                                     lambda radius: CvTools.horizontal_structuring_element(radius),
        #                                     open_first=True)

        # self.front_image[:,:,:] = 0
        for i in xrange(3):
            self.front_image[:,:,i] = filtered_image[:height,:width]

####################################################################################################
