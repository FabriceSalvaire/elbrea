    ##############################################

    def process_images_via(self, input_image):

        height, width = input_image.shape[:2]
        height_mb = int(math.ceil(height/2.)*2)
        width_mb = int(math.ceil(width/64.)*64)

        image_tmp = np.zeros((height_mb, width_mb), dtype=np.uint8)

        front_image_float = np.array(input_image, dtype=np.float32)
        front_image_float /= 255.
        front_image_hsl = cv2.cvtColor(front_image_float, cv2.COLOR_RGB2HLS)

        hue_image = np.zeros((height_mb, width_mb), dtype=np.float32)
        saturation_image = np.zeros((height_mb, width_mb), dtype=np.float32)
        lightness_image = np.zeros((height_mb, width_mb), dtype=np.float32)
        hue_image[:height,:width] = front_image_hsl[:,:,0]
        lightness_image[:height,:width] = front_image_hsl[:,:,1]
        saturation_image[:height,:width] = front_image_hsl[:,:,2]

        track_inf = 30.
        track_sup = 170.
        high_ligth = .45
        mask = ((hue_image >= track_inf) &
                (hue_image <= track_sup) &
                (lightness_image < high_ligth))
        mask = mask == False

        mask = np.array(mask, dtype=np.uint8)
        mask *= 255
        # radius = 2
        # CvTools.morphology_erode(output_image, output_image, CvTools.ball_structuring_element(radius, radius))
        CvTools.alternate_sequential_filter(mask, mask,
                                            2,
                                            lambda radius: CvTools.ball_structuring_element(radius, radius),
                                            # lambda radius: CvTools.circular_structuring_element(radius),
                                            open_first=False)

        image8_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        output_image_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        binary_image_mb = MambaTools.imageMb(width_mb, height_mb, 1)
        marker_mb = MambaTools.imageMb(width_mb, height_mb, 1)
        distance_image32_mb = MambaTools.imageMb(width_mb, height_mb, 32)
        distance_image8_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        watershed_image32_mb = MambaTools.imageMb(width_mb, height_mb, 32)
        watershed_image8_mb = MambaTools.imageMb(width_mb, height_mb, 8)

        MambaTools.cv2mamba(mask, image8_mb)

        # Segmentation grains with the distance function. Firstly, we compute the distance function
        # (note the edge programming)
        copyBitPlane(image8_mb, 0, binary_image_mb)
        computeDistance(binary_image_mb, distance_image32_mb, edge=FILLED)
        
        # We verify (with computeRange) that the distance image is lower than 256
        range = computeRange(distance_image32_mb)
        print range
        copyBytePlane(distance_image32_mb, 0, distance_image8_mb)

        # The distance function is inverted and its valued watershed is computed
        negate(distance_image8_mb, distance_image8_mb)

        # Computing a marker image
        mc.minima(distance_image8_mb, marker_mb)
        mc.dilate(marker_mb, marker_mb, 2)
        
        # Then, we compute the watershed of the inverted distance function controlled by this marker
        # set (note the number of connected components given by the labelling operator; they should
        # correspond to the number of grains)
        number_of_labels = label(marker_mb, watershed_image32_mb)
        print number_of_labels
        watershedSegment(distance_image8_mb, watershed_image32_mb) # (grayscale, marker -> output)
        # The three first byte planes contain the actual segmentation (each region has a specific
        # label according to the original marker). The last plane represents the actual watershed
        # line (pixels set to 255).

        # We build the labelled catchment basins
        copyBytePlane(watershed_image32_mb, 3, watershed_image8_mb) # copy watershed lines
        negate(watershed_image8_mb, watershed_image8_mb) # black watershed lines
        copyBytePlane(watershed_image32_mb, 0, output_image_mb) # copy labels
        logic(output_image_mb, watershed_image8_mb, output_image_mb, 'inf') # min(labels, black watershed lines)
        
        # Then, we obtain the final (and better) result. Each grain is labelled
        convert(image8_mb, watershed_image8_mb)
        # min(labels, black watershed lines, input mask)
        logic(output_image_mb, watershed_image8_mb, output_image_mb, "inf")

        output_image_mb.setPalette(patchwork)
        output_image_mb.save('tmp.png')
        image_tmp = cv2.imread('tmp.png')

        # MambaTools.mamba2cv(output_image_mb, image_tmp)

        output_image = np.zeros((height, width, 3), dtype=np.uint8)
        # output_image[:height,:width,0] = mask[:height,:width] * 255
        # output_image[:height,:width,1] = mask[:height,:width] * 255
        # output_image[:height,:width,2] = mask[:height,:width] * 255
        # output_image[:height,:width,0] = image_tmp[:height,:width] * 255
        # output_image[:height,:width,1] = image_tmp[:height,:width] * 255
        # output_image[:height,:width,2] = image_tmp[:height,:width] * 255
        output_image[:height,:width] = image_tmp[:height,:width]

        return output_image

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
