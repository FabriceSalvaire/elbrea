/* *********************************************************************************************** *
 *
 * Random RGBA 8-bit Colour Generator
 *
 * *********************************************************************************************** */

/* *********************************************************************************************** */

#include <cmath>
#include <cstdlib>

#include "RandomPixelColour.hpp"

/* *********************************************************************************************** */

uint8_t
RGBAColour::get_random_channel_value() const
{
  const int bias = 20;
  const float factor = (255. - (float) bias) / (float) RAND_MAX;

  return bias + (int) rintf(factor * (float) rand());
}

void
RGBAColour::set_random_colour()
{
  red = get_random_channel_value();
  green = get_random_channel_value();
  blue = get_random_channel_value();
  alpha = 0;
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
