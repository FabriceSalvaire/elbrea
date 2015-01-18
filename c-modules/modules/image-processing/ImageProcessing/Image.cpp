/**************************************************************************************************/

// fixme: use friend?

/**************************************************************************************************/

#include "Image.hpp"
#include "MemoryAlignment.hpp"

#include <cstring>
#include <iostream>
// #include "Python.h"

/**************************************************************************************************/

#define USE_POSIX_MALLOC

#ifdef USE_POSIX_MALLOC
#define ALIGNED_MALLOC posix_memalign
#define ALIGNED_FREE free
#else
#define ALIGNED_MALLOC aligned_malloc
#define ALIGNED_FREE aligned_free
#endif

/**************************************************************************************************/

bool
operator==(const ImageSize &image_size1, const ImageSize &image_size2)
{
  return (image_size1.width() == image_size2.width() &&
	  image_size1.height() == image_size2.height());
}

bool
operator!=(const ImageSize &image_size1, const ImageSize &image_size2)
{
  return (image_size1.width() != image_size2.width() ||
	  image_size1.height() != image_size2.height());
}

 /**************************************************************************************************/

const size_t Image::PRECISION;

Image::Image()
{
  init();
}

Image::Image(ImageSize image_size, size_t alignement) throw(ImageException)
{
  init();
  allocate(image_size, alignement);
}

Image::Image(size_t height, size_t width, size_t alignement) throw(ImageException)
{
  init();
  allocate(height, width, alignement);
}

Image::Image(const Image& image, size_t alignement) throw(ImageException)
{
  init();
  allocate(image.image_size(), alignement);
}

Image::Image(PixelPointerType buffer, size_t number_of_rows, size_t number_of_columns) throw(ImageException)
{
  // cerr << "< Image Numpy Interface > Buffer Pointer: " << buffer << endl;
  if (! is_pointer_sse_aligned(buffer))
    throw ImageException("Data are not aligned for SSE.");
  init();
  attach(buffer, number_of_rows, number_of_columns);
}

Image*
Image::clone() const
{
  return new Image(*this, is_data_aligned());
}

void
Image::init()
{
  m_data_pointer = NULL;
  m_image_size = ImageSize();
  m_step = 0;

  m_aligned = false;
  m_allocated = false;
}

Image::~Image()
{
  free_memory();
}

/*
size_t
Image::pixel_size() const
{
  return precision_to_number_of_bytes(PRECISION);
}
*/

void
Image::free_memory()
{
  if (is_allocated())
    {
      ALIGNED_FREE (data_pointer());
    }
  init(); // ?
}

void
Image::allocate(size_t height, size_t width, size_t alignement) throw(ImageException)
{
  ImageSize image_size(width, height);
  allocate(image_size, alignement);
}

void
Image::allocate(ImageSize image_size, size_t alignement) throw(ImageException)
{
  size_t new_step = number_of_pixels_to_bytes(image_size.width());
  if (alignement)
    // Align each line to alignement-byte boundary
    new_step += get_byte_padding(alignement, new_step);;

  if (! (is_allocated() && height() == image_size.height() && step() == new_step))
    {
      free_memory();
     
      size_t size = new_step * image_size.height();
      // Allocates memory aligned to 32-byte boundary.
      // Fixme: 32 -> constant
      // m_data_pointer = (PixelPointerType)aligned_malloc(32, size);
      int rc = ALIGNED_MALLOC ((void **) &m_data_pointer, 32, size);

      m_allocated = m_data_pointer != NULL;
      if (rc || ! m_allocated)
	throw ImageException("Memory allocation failed");
    }
  // else allocated and same size, but reset these variables since they can differ

  m_image_size = image_size;
  m_step = new_step;
  m_aligned = alignement != 0;
}

void
Image::attach(PixelPointerType data, size_t height, size_t width, size_t step)
{
  ImageSize image_size(width, height);
  attach(data, image_size, step);
}

void
Image::attach(PixelPointerType data, ImageSize image_size, size_t step)
{
  free_memory();

  m_data_pointer = data;
  m_image_size = image_size;
  
  if (step == 0)
    step = number_of_pixels_to_bytes(m_image_size.width());
  m_step = step;
}

bool
Image::is_same_size(const Image &image) const
{
  return image_size() == image.image_size();
}

bool
Image::is_same_format(const Image &image) const
{
  return is_same_size(image) && image.step() == step();
}

void
Image::check_is_same_format(const Image& image_src1, Image& image_dst) throw (ImageException)
{
  if (image_src1.is_same_format(image_dst) == false)
    throw ImageException("Image source 1 and destination doesn't have the same format");
}

void
Image::check_is_same_format(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  if (image_src1.is_same_format(image_src2) == false)
    throw ImageException("Image source 1 and 2 doesn't have the same format");
  check_is_same_format(image_src1, image_dst);
}

size_t
Image::data_pointer_offset(size_t r) const
{
  return r * step();
}

size_t
Image::data_pointer_offset(size_t r, size_t c) const
{
  // r_c_to_i = r * width + c
  // unchecked !
  return r * step() + c * pixel_size();
}

Image::PixelPointerType
Image::row_pointer(size_t r)
{
  return (PixelPointerType)((uint8_t*)data_pointer() + data_pointer_offset(r));
}

Image::PixelConstPointerType
Image::row_pointer(size_t r) const
{
  return (PixelConstPointerType)((uint8_t*)data_pointer() + data_pointer_offset(r));
}

Image::PixelPointerType
Image::pixel_pointer(size_t r, size_t c)
{
  return (PixelPointerType)((uint8_t*)data_pointer() + data_pointer_offset(r, c));
}

Image::PixelConstPointerType
Image::pixel_pointer(size_t r, size_t c) const
{
  // Fixme: duplicated code
  return (PixelConstPointerType)((uint8_t*)data_pointer() + data_pointer_offset(r, c));
}

Image::PixelType
Image::get(size_t r, size_t c) const
{
  return *(pixel_pointer(r, c));
}

void
Image::set(size_t r, size_t c, PixelType value)
{
  PixelPointerType pixel = pixel_pointer(r, c);
  *pixel = value;
}

void
Image::zero()
{
  memset(m_data_pointer, 0, data_size());
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
