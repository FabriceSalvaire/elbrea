/**************************************************************************************************/

#include <iostream>

/**************************************************************************************************/

#include "Image.hpp"
#include "MemoryAlignment.hpp"
#include "Operations.hpp"
#include "SimdOperations.hpp"

/**************************************************************************************************/

template<class Operation, class SseOperation>
void
unary_operation_sse(const Image& image_src, Image& image_dst) throw (ImageException)
{
  Image::check_is_same_format(image_src, image_dst);

  Operation operation;
  SseOperation sse_operation;

  size_t row_src = image_src.data_pointer_as_integer();
  size_t row_dst = image_dst.data_pointer_as_integer();

  size_t width = image_src.width_in_byte();
  // size_t width = image_src.step();

  for (size_t row = 0 ; row < image_src.height(); row++,
	 row_src += image_src.step(),
	 row_dst += image_dst.step()
       )
    {
      // std::cout << "Row " << row << std::endl;

      size_t offset = 0;
      size_t offset_increment = 2 * SSE_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  // std::cout << "  SSE " << offset << std::endl;
	  // Loads 128-bit value. Address p don't need to be 16-byte aligned.
	  size_t offset2 = offset + 8;
	  __m128i r1 = _mm_loadu_si128((const __m128i*)(row_src + offset));
	  __m128i r2 = _mm_loadu_si128((const __m128i*)(row_src + offset2));
	  r1 = sse_operation(r1);
	  r2 = sse_operation(r2);
	  // Stores 128-bit value. Address p not need be 16-byte aligned.
	  _mm_storeu_si128((__m128i*)(row_dst + offset), r1);
	  _mm_storeu_si128((__m128i*)(row_dst + offset2), r2);
	}

      offset_increment = MMX_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  // std::cout << "  MMX " << offset << std::endl;
	  // Load the lower 64 bits.
	  __m128i r1 = _mm_loadl_epi64((const __m128i*)(row_src + offset));
	  r1 = sse_operation(r1);
	  // Stores the lower 64 bits.
	  _mm_storel_epi64((__m128i*)(row_dst + offset), r1);
	}

      offset_increment = Image::PIXEL_SIZE;
      for (; offset < width; offset += offset_increment )
	{
	  // std::cout << "  " << offset << std::endl;
	  uint16_t r1 = *((uint16_t*)(row_src + offset));
	  r1 = operation(r1);
	  *((uint16_t*)(row_dst + offset)) = r1;
	}
    }
}

/**************************************************************************************************/

template<class Operation, class SseOperation>
void
unary_value_operation_sse(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  Image::check_is_same_format(image_src, image_dst);

  Operation operation;
  SseOperation sse_operation;

  size_t row_src = image_src.data_pointer_as_integer();
  size_t row_dst = image_dst.data_pointer_as_integer();

  size_t width = image_src.width_in_byte();
  // size_t width = image_src.step();

  for (size_t row = 0 ; row < image_src.height(); row++,
	 row_src += image_src.step(),
	 row_dst += image_dst.step()
       )
    {
      // std::cout << "Row " << row << std::endl;

      size_t offset = 0;
      size_t offset_increment = 2 * SSE_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  // std::cout << "  SSE " << offset << std::endl;
	  // Loads 128-bit value. Address p don't need to be 16-byte aligned.
	  size_t offset2 = offset + 8;
	  __m128i r1 = _mm_loadu_si128((const __m128i*)(row_src + offset));
	  __m128i r2 = _mm_loadu_si128((const __m128i*)(row_src + offset2));
	  r1 = sse_operation(r1, value);
	  r2 = sse_operation(r2, value);
	  // Stores 128-bit value. Address p not need be 16-byte aligned.
	  _mm_storeu_si128((__m128i*)(row_dst + offset), r1);
	  _mm_storeu_si128((__m128i*)(row_dst + offset2), r2);
	}

      offset_increment = MMX_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  // std::cout << "  MMX " << offset << std::endl;
	  // Load the lower 64 bits.
	  __m128i r1 = _mm_loadl_epi64((const __m128i*)(row_src + offset));
	  r1 = sse_operation(r1, value);
	  // Stores the lower 64 bits.
	  _mm_storel_epi64((__m128i*)(row_dst + offset), r1);
	}

      offset_increment = Image::PIXEL_SIZE;
      for (; offset < width; offset += offset_increment )
	{
	  // std::cout << "  " << offset << std::endl;
	  uint16_t r1 = *((uint16_t*)(row_src + offset));
	  r1 = operation(r1, value);
	  *((uint16_t*)(row_dst + offset)) = r1;
	}
    }
}

/**************************************************************************************************/

template<class Operation, class SseOperation>
void
unary_sse_value_operation_sse(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  Image::check_is_same_format(image_src, image_dst);

  Operation operation;
  SseOperation sse_operation;

  __m128i value_sse1 = _mm_set1_epi16(static_cast<int16_t>(value));
  __m128i value_sse2 = _mm_set1_epi16(static_cast<int16_t>(value));

  size_t row_src = image_src.data_pointer_as_integer();
  size_t row_dst = image_dst.data_pointer_as_integer();

  size_t width = image_src.width_in_byte();
  // size_t width = image_src.step();

  for (size_t row = 0 ; row < image_src.height(); row++,
	 row_src += image_src.step(),
	 row_dst += image_dst.step()
       )
    {
      std::cout << "Row " << row << std::endl;

      size_t offset = 0;
      size_t offset_increment = 2 * SSE_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  std::cout << "  SSE " << offset << std::endl;
	  // Loads 128-bit value. Address p don't need to be 16-byte aligned.
	  size_t offset2 = offset + 8;
	  __m128i r1 = _mm_loadu_si128((const __m128i*)(row_src + offset));
	  __m128i r2 = _mm_loadu_si128((const __m128i*)(row_src + offset2));
	  r1 = sse_operation(r1, value_sse1);
	  r2 = sse_operation(r2, value_sse2);
	  // Stores 128-bit value. Address p not need be 16-byte aligned.
	  _mm_storeu_si128((__m128i*)(row_dst + offset), r1);
	  _mm_storeu_si128((__m128i*)(row_dst + offset2), r2);
	}

      offset_increment = MMX_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  std::cout << "  MMX " << offset << std::endl;
	  // Load the lower 64 bits.
	  __m128i r1 = _mm_loadl_epi64((const __m128i*)(row_src + offset));
	  r1 = sse_operation(r1, value_sse1);
	  // Stores the lower 64 bits.
	  _mm_storel_epi64((__m128i*)(row_dst + offset), r1);
	}

      offset_increment = Image::PIXEL_SIZE;
      for (; offset < width; offset += offset_increment )
	{
	  std::cout << "  " << offset << std::endl;
	  uint16_t r1 = *((uint16_t*)(row_src + offset));
	  r1 = operation(r1, value);
	  *((uint16_t*)(row_dst + offset)) = r1;
	}
    }
}

/**************************************************************************************************/

template<class Operation, class SseOperation>
void
binary_operation_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  Image::check_is_same_format(image_src1, image_src2, image_dst);

  Operation operation;
  SseOperation sse_operation;

  size_t row_src1 = image_src1.data_pointer_as_integer();
  size_t row_src2 = image_src2.data_pointer_as_integer();
  size_t row_dst = image_dst.data_pointer_as_integer();

  size_t width = image_src1.width_in_byte();
  // size_t width = image_src1.step();

  for (size_t row = 0 ; row < image_src1.height(); row++,
	 row_src1 += image_src1.step(),
	 row_src2 += image_src2.step(),
	 row_dst += image_dst.step()
       )
    {
      std::cout << "Row " << row << std::endl;

      size_t offset = 0;
      size_t offset_increment = 2 * SSE_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  std::cout << "  SSE " << offset << std::endl;
	  // Loads 128-bit value. Address p don't need to be 16-byte aligned.
	  size_t offset2 = offset + 8;
	  __m128i r11 = _mm_loadu_si128((const __m128i*)(row_src1 + offset));
	  __m128i r12 = _mm_loadu_si128((const __m128i*)(row_src2 + offset));
	  __m128i r21 = _mm_loadu_si128((const __m128i*)(row_src1 + offset2));
	  __m128i r22 = _mm_loadu_si128((const __m128i*)(row_src2 + offset2));
	  r11 = sse_operation(r11, r12);
	  r21 = sse_operation(r21, r22);
	  // Stores 128-bit value. Address p not need be 16-byte aligned.
	  _mm_storeu_si128((__m128i*)(row_dst + offset), r11);
	  _mm_storeu_si128((__m128i*)(row_dst + offset2), r21);
	}

      offset_increment = MMX_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  std::cout << "  MMX " << offset << std::endl;
	  // Load the lower 64 bits.
	  __m128i r1 = _mm_loadl_epi64((const __m128i*)(row_src1 + offset));
	  __m128i r2 = _mm_loadl_epi64((const __m128i*)(row_src2 + offset));
	  r1 = sse_operation(r1, r2);
	  // Stores the lower 64 bits.
	  _mm_storel_epi64((__m128i*)(row_dst + offset), r1);
	}

      offset_increment = Image::PIXEL_SIZE;
      for (; offset < width; offset += offset_increment )
	{
	  std::cout << "  " << offset << std::endl;
	  uint16_t r1 = *((uint16_t*)(row_src1 + offset));
	  uint16_t r2 = *((uint16_t*)(row_src2 + offset));
	  r1 = operation(r1, r2);
	  *((uint16_t*)(row_dst + offset)) = r1;
	}
    }
}

/**************************************************************************************************/

void
Image::set_constant_sse(PixelType value)
{
  size_t row_ptr = data_pointer_as_integer();

  size_t width = width_in_byte();
  // size_t width = step();

  __m128i value_sse1 = _mm_set1_epi16(static_cast<int16_t>(value));
  __m128i value_sse2 = _mm_set1_epi16(static_cast<int16_t>(value));

  for (size_t row = 0 ; row < height(); row++, row_ptr += step())
    {
      size_t offset = 0;
      size_t offset_increment = 2 * SSE_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  size_t offset2 = offset + 8;
	  // Stores 128-bit value. Address p don't need to be 16-byte aligned.
	  _mm_storeu_si128((__m128i*)(row_ptr + offset), value_sse1);
	  _mm_storeu_si128((__m128i*)(row_ptr + offset2), value_sse2);
	}

      // Fixme: move row_ptr + offset in the loop
      offset_increment = MMX_BYTE_SIZE;
      for (; offset <= width - offset_increment; offset += offset_increment)
	{
	  // Stores the lower 64 bits.
	  _mm_storel_epi64((__m128i*)(row_ptr + offset), value_sse1);
	}

      offset_increment = Image::PIXEL_SIZE;
      for (; offset < width; offset += offset_increment )
	{
	  *((uint16_t*)(row_ptr + offset)) = value;
	}
    }
}

/**************************************************************************************************/

void
equal_sse(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  unary_sse_value_operation_sse<equal_uint16, sse_equal_uint16>(image_src, image_dst, value);
}

void
not_equal_sse(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  unary_sse_value_operation_sse<not_equal_uint16, sse_not_equal_uint16>(image_src, image_dst, value);
}

void
saturated_addition_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  binary_operation_sse<saturated_addition_uint16, sse_saturated_addition_uint16>(image_src1, image_src2, image_dst);
}

void
saturated_subtraction_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  binary_operation_sse<saturated_subtraction_uint16, sse_saturated_subtraction_uint16>(image_src1, image_src2, image_dst);
}

void
shift_left_sse(const Image& image_src, Image& image_dst, Image::PixelType count) throw (ImageException)
{
  unary_value_operation_sse<shift_left_uint16, sse_shift_left_uint16>(image_src, image_dst, count);
}

void
shift_right_sse(const Image& image_src, Image& image_dst, Image::PixelType count) throw (ImageException)
{
  unary_value_operation_sse<shift_right_uint16, sse_shift_right_uint16>(image_src, image_dst, count);
}

void
and_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  binary_operation_sse<and_uint16, sse_and>(image_src1, image_src2, image_dst);
}

void
or_sse(const Image& image_src1, const Image& image_src2, Image& image_dst) throw (ImageException)
{
  binary_operation_sse<or_uint16, sse_or>(image_src1, image_src2, image_dst);
}

void
zero_up_to_sse(const Image& image_src, Image& image_dst, Image::PixelType value) throw (ImageException)
{
  unary_value_operation_sse<zero_up_to_uint16, sse_zero_up_to_uint16>(image_src, image_dst, value);
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
