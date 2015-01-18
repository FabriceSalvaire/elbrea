/* *********************************************************************************************** *
 *
 * Random RGBA 8-bit Colour Generator
 *
 * *********************************************************************************************** */

/* *********************************************************************************************** */

#ifndef __RandomPixelColour_H__
#define __RandomPixelColour_H__

/* *********************************************************************************************** */

#include <stdint.h>

/* *********************************************************************************************** */

// Fixme: bad API

//! Random RGBA 8-bit Colour Generator
class RGBAColour
{
public:
  RGBAColour()
    : red(0), green(0), blue(0), alpha(0)
  {}

  RGBAColour(uint8_t red, uint8_t green, uint8_t blue, uint8_t alpha)
    : red(red), green(green), blue(blue), alpha(alpha)
  {}

  uint8_t get_random_channel_value() const;
  void set_random_colour();

public:
  uint8_t red;
  uint8_t green;
  uint8_t blue;
  uint8_t alpha;
};

/* *********************************************************************************************** */

#endif /* __RandomPixelColour_H__ */

/* *********************************************************************************************** */
