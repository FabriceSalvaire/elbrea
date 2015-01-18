/* *********************************************************************************************** */

#ifndef __Math_H__
#define __Math_H__

/* *********************************************************************************************** */

#include <stdint.h>
#include <stdlib.h>

#include <cmath>

/* *********************************************************************************************** */

const double FRAC_PI_180 = M_PI / 180.;
const double FRAC_180_PI = 180. * M_1_PI;

const float FRAC_PI_180_F = static_cast<float>(FRAC_PI_180);
const float FRAC_180_PI_F = static_cast<float>(FRAC_180_PI);

inline float
rad2deg(float rad)
{
  return FRAC_180_PI_F*rad;
}

inline float
deg2rad(float deg)
{
  return FRAC_PI_180_F*deg;
}

/* *********************************************************************************************** */

inline int64_t
copy_sign(int64_t x)
{
  /*
   * +1 = 00...01
   * -1 = 11...11
   *
   * sb...b >> number of bits -1: copy the sign bit in all bits
   * 
   */

  const size_t byte_size = 8;
  return +1 | (x >> (byte_size*sizeof(int64_t) - 1));
}

/*
inline int64_t
copy_sign(int64_t x)
{
  return (x > 0) ? 1 : -1;
}

// GCC_builtin copysign
inline double
copy_sign(double x)
{
  return (x > .0) ? 1. : -1.;
}
*/

/* *********************************************************************************************** */

#endif /* __Math_H__ */

/* *********************************************************************************************** */
