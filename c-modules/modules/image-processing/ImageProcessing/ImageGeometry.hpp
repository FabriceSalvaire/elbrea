#ifndef __IMAGEGEOMETRY_H__
#define __IMAGEGEOMETRY_H__

/* *********************************************************************************************** */

#include <stdint.h>

/**************************************************************************************************/

#include "../../math/Geometry.hpp"

/* *********************************************************************************************** */

// Fixme: SWIG ?
// typedef int64_t OffsetType;
// typedef uint64_t PositionType;
typedef long int OffsetType;
typedef unsigned long int PositionType;

class Point2D;

/* *********************************************************************************************** */

// class Offset2D : public Vector2D<OffsetType>
class Offset2D : public Vector2D_traits<OffsetType>
{
public: // Ctors
  Offset2D();
  Offset2D(OffsetType r, OffsetType c);
  Offset2D(const Point2D & point);

  // Fixme: why ?
  Offset2D operator-(const Offset2D & other) const;
  Offset2D& operator= (const Offset2D& other);

public: // Accessors
  inline OffsetType r() const { return y(); }
  inline OffsetType c() const { return x(); }
};

/* *********************************************************************************************** */

// Vocabular: point, location

class Point2D : public Vector2D_traits<PositionType>
{
public: // Ctors
  Point2D();
  Point2D(PositionType r, PositionType c);

public: // Accessors
  inline PositionType r() const { return y(); }
  inline PositionType c() const { return x(); }

public: // Methods
  Point2D operator+(const Offset2D & other) const;
  Point2D operator-(const Offset2D & other) const;

  Point2D & operator+=(const Offset2D & other);
  Point2D & operator-=(const Offset2D & other);
};

/**************************************************************************************************/

#endif /* __IMAGEGEOMETRY_H__ */

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
