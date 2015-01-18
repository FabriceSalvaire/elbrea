#ifndef __OPERATIONS_H__
#define __OPERATIONS_H__

/**************************************************************************************************/

#include "Image.hpp"

/**************************************************************************************************/

struct saturated_addition_uint16
{
  uint16_t operator()(uint16_t a, uint16_t b) const
  {
    uint32_t r = a + b;
    if (r > Image::PIXEL_SUP)
      return Image::PIXEL_SUP;
    else
      return static_cast<Image::PixelType>(r);
  }
};

struct saturated_subtraction_uint16
{
  uint16_t operator()(uint16_t a, uint16_t b) const
  {
    int32_t r = a - b;
    if (r < Image::PIXEL_INF)
      return Image::PIXEL_INF;
    else
      return static_cast<Image::PixelType>(r);
  }
};

struct shift_left_uint16
{
  uint16_t operator()(uint16_t a, Image::PixelType count) const
  {
    return a << count;
  }
};

struct shift_right_uint16
{
  uint16_t operator()(uint16_t a, Image::PixelType count) const
  {
    return a >> count;
  }
};

struct equal_uint16
{
  uint16_t operator()(uint16_t a, Image::PixelType value) const
  {
    return (a) ? Image::PIXEL_SUP : Image::PIXEL_INF;
  }
};

struct not_equal_uint16
{
  uint16_t operator()(uint16_t a, Image::PixelType value) const
  {
    return a ? Image::PIXEL_INF : Image::PIXEL_SUP;
  }
};

struct and_uint16
{
  uint16_t operator()(uint16_t a, uint16_t b) const
  {
    return a & b;
  }
};

struct or_uint16
{
  uint16_t operator()(uint16_t a, uint16_t b) const
  {
    return a | b;
  }
};

struct zero_up_to_uint16
{
  uint16_t operator()(uint16_t a, Image::PixelType value) const
  {
    return (a > value) ? a: Image::PIXEL_INF;
  }
};

/**************************************************************************************************/

#endif /* __OPERATIONS_H__ */

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
