#ifndef __IMAGE_H__
#define __IMAGE_H__

/**************************************************************************************************/

#include <stdint.h>
#include <stdlib.h>
#include <exception>
#include <string>

using namespace std;

/**************************************************************************************************/

#include "ImageException.hpp"

/**************************************************************************************************/

class ImageSize
{
public: // Ctors
  ImageSize():
    m_width(0), m_height(0)
  {}

  ImageSize(size_t width, size_t height):
    m_width(width), m_height(height)
  {}

  ImageSize(const ImageSize &image_size):
    m_width(image_size.width()), m_height(image_size.height())
  {}

public: // Accessors
  inline size_t width() const { return m_width; }
  inline size_t height() const { return m_height; }
  inline size_t size() const { return m_width * m_height; }

private: // Members
  size_t m_width;
  size_t m_height;
};

bool operator==(const ImageSize &image_size1, const ImageSize &image_size2);
bool operator!=(const ImageSize &image_size1, const ImageSize &image_size2);

/**************************************************************************************************/

class Image
{
public: // Standard typedef
  // typedef Image Self;
  typedef uint16_t PixelType;
  typedef PixelType* PixelPointerType;
  typedef const PixelType* PixelConstPointerType;

public:
  static const size_t PIXEL_SIZE = sizeof(PixelType); // [byte]
  static const size_t PRECISION = PIXEL_SIZE * 8; // [bit]
  static const PixelType PIXEL_INF = 0;
  static const PixelType PIXEL_SUP = 0xFFFF;

public:
  Image();
  Image(size_t height, size_t width, size_t alignement = 0) throw(ImageException);
  Image(ImageSize image_size, size_t alignement = 0) throw(ImageException);
  Image(const Image& image, size_t alignement = 0) throw(ImageException);
  Image(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns) throw(ImageException); // Numpy Interface use attach
  virtual ~Image();

  Image* clone() const;

  // Image Dimension Accessor
  ImageSize image_size() const { return m_image_size; }
  size_t height() const { return m_image_size.height(); }
  size_t width() const { return m_image_size.width(); }

  // void height(int height) { m_image_size.height = height; }
  // void width(int width) { m_image_size.width = width; } // step ?

  size_t pixel_size() const { return PIXEL_SIZE; };  // Size in byte of a pixel
  size_t number_of_pixels_to_bytes(size_t i) const { return i * PIXEL_SIZE; };

  size_t width_in_byte() const { return number_of_pixels_to_bytes(width()); };
  size_t step() const { return m_step; }
  size_t data_size() const { return step() * height(); }

  bool is_allocated() const { return m_allocated; }

  void allocate(size_t height, size_t width, size_t alignement = 0) throw(ImageException);
  void allocate(ImageSize image_size, size_t alignement = 0) throw(ImageException);
  void attach(PixelPointerType data, ImageSize image_size, size_t step = 0);
  void attach(PixelPointerType data, size_t height, size_t width, size_t step = 0);
  void free_memory();

  PixelPointerType data_pointer() { return m_data_pointer; }
  PixelConstPointerType data_pointer() const { return m_data_pointer; }

  size_t data_pointer_as_integer() const { return (size_t)data_pointer(); }
  bool is_data_aligned() const { return m_aligned; };
  bool use_padding() const { return step() > static_cast<size_t>(width()); }

  bool is_same_size(const Image& image) const;
  bool is_same_format(const Image& image) const;
  static void check_is_same_format(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);
  static void check_is_same_format(const Image& image_src1, Image& image_dst) throw (ImageException);

  PixelType get(size_t r, size_t c) const;
  void set(size_t r, size_t c, PixelType value);

  void zero();

  void copy_to(Image &image) const throw (ImageException);
  void copy_from(const Image &image) throw (ImageException);

  void set_constant(PixelType value);
  void set_constant_sse(PixelType value);

  bool equal(const Image& image);

public: // fixme
  size_t data_pointer_offset(size_t r) const;
  size_t data_pointer_offset(size_t r, size_t c) const;
  PixelPointerType pixel_pointer(size_t r, size_t c);
  PixelConstPointerType pixel_pointer(size_t r, size_t c) const;
  PixelPointerType row_pointer(size_t r);
  PixelConstPointerType row_pointer(size_t r) const;

private:
  void init();

private:
  PixelPointerType m_data_pointer; // Image Data Pointer
  size_t m_step; // Distance in bytes between starts of consecutive lines in the source image.
  ImageSize m_image_size; // Dimension of the buffer in pixels

  bool m_aligned;
  bool m_allocated;
};

/**************************************************************************************************/

void equal(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException);
void equal_sse(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException);
void not_equal(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException);
void not_equal_sse(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException);

void saturated_addition(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);
void saturated_addition_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);
void saturated_subtraction(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);
void saturated_subtraction_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);

void shift_left(const Image& image_src, Image& image_dst, Image::PixelType count) throw (ImageException);
void shift_left_sse(const Image& image_src, Image& image_dst, Image::PixelType count) throw (ImageException);
void shift_right(const Image& image_src, Image& image_dst, Image::PixelType count) throw (ImageException);
void shift_right_sse(const Image& image_src, Image& image_dst, Image::PixelType count) throw (ImageException);

void and_(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);
void and_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);
void or_(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);
void or_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException);

void zero_up_to(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException);
void zero_up_to_sse(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException);

/**************************************************************************************************/

#endif /* __IMAGE_H__ */

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
