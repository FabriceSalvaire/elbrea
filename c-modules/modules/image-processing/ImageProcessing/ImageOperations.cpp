/**************************************************************************************************/

#include <cstring>

#include "Image.hpp"
#include "Operations.hpp"

/**************************************************************************************************/

template<class Operation>
void
unary_operation(const Image& image_src, Image& image_dst) throw (ImageException)
{
  Image::check_is_same_format(image_src, image_dst);

  Operation operation;

  for (size_t r = 0; r < image_src.height(); r++)
    {
      Image::PixelConstPointerType row_ptr = image_src.row_pointer(r);
      Image::PixelPointerType row_dst= image_dst.row_pointer(r);
      for (size_t c = 0; c < image_src.width(); c++)
	row_dst[c] = operation(row_ptr[c]);
    }
}

template<class Operation>
void
unary_value_operation(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  Image::check_is_same_format(image_src, image_dst);

  Operation operation;

  for (size_t r = 0; r < image_src.height(); r++)
    {
      Image::PixelConstPointerType row_ptr = image_src.row_pointer(r);
      Image::PixelPointerType row_dst= image_dst.row_pointer(r);
      for (size_t c = 0; c < image_src.width(); c++)
	row_dst[c] = operation(row_ptr[c], value);
    }
}

template<class Operation>
void
binary_operation(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  Image::check_is_same_format(image_src1, image_src2, image_dst);

  Operation operation;

  for (size_t r = 0; r < image_src1.height(); r++)
    {
      Image::PixelConstPointerType row_ptr1 = image_src1.row_pointer(r);
      Image::PixelConstPointerType row_ptr2 = image_src2.row_pointer(r);
      Image::PixelPointerType row_dst= image_dst.row_pointer(r);
      for (size_t c = 0; c < image_src1.width(); c++)
	row_dst[c] = operation(row_ptr1[c], row_ptr2[c]);
    }
}

/**************************************************************************************************/

void
Image::copy_to(Image &image) const throw (ImageException)
{
  if (! is_same_size(image))
    throw ImageException("Images don't have the same size.");

  for (size_t r = 0; r < height(); r++)
    {
      PixelConstPointerType row_ptr_src = row_pointer(r);
      PixelPointerType row_ptr_dst = image.row_pointer(r);
      memcpy(row_ptr_dst, row_ptr_src, width_in_byte());
    }
}

/**************************************************************************************************/

void
Image::copy_from(const Image &image) throw (ImageException)
{
  if (! is_same_size(image))
    throw ImageException("Images don't have the same size.");

  for (size_t r = 0; r < height(); r++)
    {
      PixelConstPointerType row_ptr_src = image.row_pointer(r);
      PixelPointerType row_ptr_dst = row_pointer(r);
      memcpy(row_ptr_dst, row_ptr_src, width_in_byte());
    }
}

/**************************************************************************************************/

void
Image::set_constant(PixelType value)
{
  //? padding => row multiple of PixelType ?
  for (size_t r = 0; r < height(); r++)
    {
      PixelPointerType row_ptr = row_pointer(r);
      for (size_t c = 0; c < width(); c++)
	row_ptr[c] = value;
    }
}

/**************************************************************************************************/

bool
Image::equal(const Image& image)
{
  if (! is_same_format(image))
    return false;
  else
  {
    for (size_t r = 0; r < height(); r++)
      {
	PixelConstPointerType row_ptr1 = row_pointer(r);
	PixelConstPointerType row_ptr2 = image.row_pointer(r);
	for (size_t c = 0; c < width(); c++)
	  if (row_ptr1[c] != row_ptr2[c])
	    return false;
      }
    return true;
  }
}

void
equal(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  unary_value_operation<equal_uint16>(image_src, image_dst, value);
}

void
not_equal(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  unary_value_operation<not_equal_uint16>(image_src, image_dst, value);
}

/**************************************************************************************************/

void
saturated_addition(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  binary_operation<saturated_addition_uint16>(image_src1, image_src2, image_dst);
}

void
saturated_subtraction(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  binary_operation<saturated_subtraction_uint16>(image_src1, image_src2, image_dst);
}

/**************************************************************************************************/

void
shift_left(const Image& image_src, Image& image_dst, Image::PixelType count) throw (ImageException)
{
  unary_value_operation<shift_left_uint16>(image_src, image_dst, count);
}

void
shift_right(const Image& image_src, Image& image_dst, Image::PixelType count) throw (ImageException)
{
  unary_value_operation<shift_right_uint16>(image_src, image_dst, count);
}

/**************************************************************************************************/

void
and_(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  binary_operation<and_uint16>(image_src1, image_src2, image_dst);
}

void
or_(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  binary_operation<or_uint16>(image_src1, image_src2, image_dst);
}

/**************************************************************************************************/

void
zero_up_to(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  unary_value_operation<zero_up_to_uint16>(image_src, image_dst, value);
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
