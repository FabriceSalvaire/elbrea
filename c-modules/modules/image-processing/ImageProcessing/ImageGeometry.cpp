/**************************************************************************************************/

#include <iostream>

#include "ImageGeometry.hpp"

/**************************************************************************************************/

Offset2D::Offset2D()
  : Vector2D_traits<OffsetType>()
{
}

Offset2D::Offset2D(OffsetType r, OffsetType c)
  : Vector2D_traits<OffsetType>(c, r)
{
}

Offset2D::Offset2D(const Point2D & point)
  : Vector2D_traits<OffsetType>(point.x(), point.y())
{}

Offset2D
Offset2D::operator-(const Offset2D & other) const
{
  OffsetType c = m_x - other.m_x;
  OffsetType r = m_y - other.m_y;
  
  return Offset2D(r, c);
}

Offset2D&
Offset2D::operator=(const Offset2D & other)
{
  m_x = other.m_x;
  m_y = other.m_y;

  return *this;
}

/* *********************************************************************************************** */

Point2D::Point2D()
  : Vector2D_traits<PositionType>()
{
}

Point2D::Point2D(PositionType r, PositionType c)
  : Vector2D_traits<PositionType>(c, r)
{
}

Point2D
Point2D::operator+(const Offset2D & other) const
{
  return Point2D(r() + other.r(),
		 c() + other.c());
}

Point2D
Point2D::operator-(const Offset2D & other) const
{
  // Throw exception
  // PositionType vs int
  // Point2D::PositionType _r = (r > other.r) ? r - other.r : 0;
  // Point2D::PositionType _c = (c > other.c) ? c - other.c : 0;
  // 
  // return Point2D(_r, _c);

  return Point2D(r() - other.r(),
		 c() - other.c());
}

Point2D &
Point2D::operator+=(const Offset2D & other)
{
  // Vector2D_traits<PositionType>::operator+=(other);
  m_x += other.x();
  m_y += other.y();

  return *this;
}

Point2D &
Point2D::operator-=(const Offset2D & other)
{
  // Throw exception
  // if (r > other.r)
  //   r -= other.r;
  // else
  //   r = 0;
  // 
  // if (c > other.c)
  //   c -= other.c;
  // else
  //   c = 0;

  // Vector2D_traits<PositionType>::operator-=(other);
  m_x -= other.x();
  m_y -= other.y();

  return *this;
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
