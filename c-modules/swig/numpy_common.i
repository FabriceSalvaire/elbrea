// -*- C++ -*-

/* *********************************************************************************************** */

%{
#include <stdint.h>
%}

%include "std_typedef.i"

/* *********************************************************************************************** */
/*
 * Numpy interface
 *
 */

%{
#define SWIG_FILE_WITH_INIT
%}

%include "numpy.i"

%init %{
import_array();
%}

/****** 1D ******/

// fixme: uint8_t
%apply (unsigned char *INPLACE_ARRAY1, int DIM1) {(uint8_t *buffer, size_t size)};
%apply (unsigned char *INPLACE_ARRAY1, int DIM1) {(uint8_t *buffer1, size_t size1)};
%apply (unsigned char *INPLACE_ARRAY1, int DIM1) {(uint8_t *buffer2, size_t size2)};
%apply (unsigned char *INPLACE_ARRAY1, int DIM1) {(uint8_t *buffer3, size_t size3)};
%apply (unsigned char *INPLACE_ARRAY1, int DIM1) {(uint8_t *buffer4, size_t size4)};
%apply (unsigned char *INPLACE_ARRAY1, int DIM1) {(uint8_t *src_buffer, size_t src_size)};
%apply (unsigned char *INPLACE_ARRAY1, int DIM1) {(uint8_t *dst_buffer, size_t dst_size)};

// fixme: uint16_t
%apply (unsigned short *INPLACE_ARRAY1, int DIM1) {(uint16_t *buffer, size_t size)};
%apply (unsigned short *INPLACE_ARRAY1, int DIM1) {(uint16_t *buffer1, size_t size1)};
%apply (unsigned short *INPLACE_ARRAY1, int DIM1) {(uint16_t *buffer2, size_t size2)};
%apply (unsigned short *INPLACE_ARRAY1, int DIM1) {(uint16_t *buffer3, size_t size3)};
%apply (unsigned short *INPLACE_ARRAY1, int DIM1) {(uint16_t *buffer4, size_t size4)};
%apply (unsigned short *INPLACE_ARRAY1, int DIM1) {(uint16_t *src_buffer, size_t src_size)};
%apply (unsigned short *INPLACE_ARRAY1, int DIM1) {(uint16_t *dst_buffer, size_t dst_size)};

// fixme: uint64_t
%apply (unsigned long int *INPLACE_ARRAY1, int DIM1) {(uint64_t *dst_buffer, size_t dst_size)};

// float
%apply (float *INPLACE_ARRAY1, int DIM1) {(float *buffer, size_t size)};
%apply (float *INPLACE_ARRAY1, int DIM1) {(float *src_buffer, size_t src_size)};
%apply (float *INPLACE_ARRAY1, int DIM1) {(float *dst_buffer, size_t dst_size)};

/****** 2D ******/

// fixme: uint8_t
%apply (unsigned char *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint8_t *buffer,
							     size_t number_of_rows, size_t number_of_columns)};

%apply (unsigned char *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint8_t *src_buffer,
							     size_t src_number_of_rows, size_t src_number_of_columns)};

%apply (unsigned char *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint8_t *dst_buffer,
							     size_t dst_number_of_rows, size_t dst_number_of_columns)};


%apply (unsigned char *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint8_t *red_buffer,
							     size_t red_number_of_rows, size_t red_number_of_columns)};
%apply (unsigned char *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint8_t *green_buffer,
							     size_t green_number_of_rows, size_t green_number_of_columns)};
%apply (unsigned char *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint8_t *blue_buffer,
							     size_t blue_number_of_rows, size_t blue_number_of_columns)};

%apply (unsigned char *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint8_t *buffer1,
							     size_t number_of_rows1, size_t number_of_columns1)};

%apply (unsigned char *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint8_t *buffer2,
							     size_t number_of_rows2, size_t number_of_columns2)};

%apply (unsigned char *IN_ARRAY2, int DIM1, int DIM2) {(uint8_t *buffer3,
							size_t number_of_rows3, size_t number_of_columns3)};

%apply (unsigned char *IN_ARRAY2, int DIM1, int DIM2) {(uint8_t *buffer4,
							size_t number_of_rows4, size_t number_of_columns4)};

// fixme: uint16_t
%apply (unsigned short *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint16_t *buffer,
							      size_t number_of_rows, size_t number_of_columns)};

%apply (unsigned short *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint16_t *src_buffer,
							      size_t src_number_of_rows, size_t src_number_of_columns)};

%apply (unsigned short *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint16_t *dst_buffer,
							      size_t dst_number_of_rows, size_t dst_number_of_columns)};

%apply (unsigned short *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint16_t *red_buffer,
							      size_t red_number_of_rows, size_t red_number_of_columns)};
%apply (unsigned short *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint16_t *green_buffer,
							      size_t green_number_of_rows, size_t green_number_of_columns)};
%apply (unsigned short *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint16_t *blue_buffer,
							      size_t blue_number_of_rows, size_t blue_number_of_columns)};


%apply (unsigned short *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint16_t *buffer1,
							      size_t number_of_rows1, size_t number_of_columns1)};

%apply (unsigned short *INPLACE_ARRAY2, int DIM1, int DIM2) {(uint16_t *buffer2,
							      size_t number_of_rows2, size_t number_of_columns2)};

%apply (unsigned short *IN_ARRAY2, int DIM1, int DIM2) {(uint16_t *buffer3,
							 size_t number_of_rows3, size_t number_of_columns3)};

%apply (unsigned short *IN_ARRAY2, int DIM1, int DIM2) {(uint16_t *buffer4,
							 size_t number_of_rows4, size_t number_of_columns4)};

/****** 3D ******/

// fixme: uint8_t
%apply (unsigned char *INPLACE_ARRAY3, int DIM1, int DIM2, int DIM3) {(uint8_t *buffer,
								       size_t number_of_rows,
								       size_t number_of_columns,
								       size_t number_of_channels)};

// fixme: uint16_t
%apply (unsigned short *INPLACE_ARRAY3, int DIM1, int DIM2, int DIM3) {(uint16_t *buffer,
									size_t number_of_rows,
									size_t number_of_columns,
									size_t number_of_channels)};

/* *********************************************************************************************** */

/*
 * End
 *
 ************************************************************************************************* */
