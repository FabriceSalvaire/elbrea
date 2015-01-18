/* *********************************************************************************************** */

#include <climits>
#include <cmath>
#include <cstdlib>
#include <iostream>

/* *********************************************************************************************** */

#include "Math.hpp"
#include "Vector.hpp"

/* *********************************************************************************************** */

template<> const char * Vector2D_traits<uint64_t>::class_name = "Vector2D<uint64_t>";

Vector2D<uint64_t> &
Vector2D<uint64_t>::operator-=(const Vector2D<int64_t> & other)
{
  m_x -= other.x();
  m_y -= other.y();

  return *this;
}

Vector2D<uint64_t> &
Vector2D<uint64_t>::operator+=(const Vector2D<int64_t> & other)
{
  m_x += other.x();
  m_y += other.y();

  return *this;
}

/* *********************************************************************************************** */

template<> const char * Vector2D_traits<int64_t>::class_name = "Vector2D<int64_t>";

/* *********************************************************************************************** */

template<> const char * Vector2D_traits<double>::class_name = "Vector2D<double>";

Vector2D<double>::Vector2D(double angle)
  : Vector2D_traits<double>()
{
  double rad = deg2rad(angle);

  m_x = cos(rad);
  m_y = sin(rad);
}

double
Vector2D<double>::magnitude_square() const
{
  double f1 = m_x*m_x;
  double f2 = m_y*m_y;

  return f1 + f2;
}

double
Vector2D<double>::magnitude() const
{
  return sqrt(magnitude_square());
}

void
Vector2D<double>::normalise()
{
  *this *= 1. / magnitude(); // scale, better way?
}

double
Vector2D<double>::slope() const
{
  return m_y / m_x;
}

double
Vector2D<double>::slope_inverse() const
{
  return m_x / m_y;
}

double
Vector2D<double>::orientation() const
{
  return rad2deg(atan(slope()));
}

double
Vector2D<double>::dot(const Vector2D<double> & other) const
{
  double f1 = m_x*other.m_x;
  double f2 = m_y*other.m_y;

  return f1 + f2;
}

double
Vector2D<double>::cross(const Vector2D<double> & other) const
{
  double f1 = m_x*other.m_y;
  double f2 = m_y*other.m_x;

  return f1 - f2;
}

bool
Vector2D<double>::is_parallel(const Vector2D<double> & other) const
{
  // Fixme

  return (fabs(cross(other)) < 1e-6) ? true : false;
}

bool
Vector2D<double>::is_orthogonal(const Vector2D<double> & other) const
{
  return (fabs(dot(other)) < 1e-6) ? true : false;
}

double
Vector2D<double>::cos_with(const Vector2D<double> & other) const
{
  double scale = magnitude() * other.magnitude();

  return dot(other) / scale;
}

double
Vector2D<double>::sin_with(const Vector2D<double> & other) const
{
  double scale = magnitude() * other.magnitude();

  return cross(other) / scale;
}

double
Vector2D<double>::orientation_with(const Vector2D<double> & other) const
{
  return rad2deg(acos(cos_with(other)));
}

double
Vector2D<double>::deviation_with(const Vector2D<double> & other) const
{
  return magnitude() * sin_with(other);
}

Vector2D<double>
Vector2D<double>::rotate_counter_clockwise(double angle) const
{
  double rad = rad2deg(angle);

  double c = cos(rad);
  double s = sin(rad);

  double xp = c*m_x - s*m_y;
  double yp = s*m_x + c*m_y;

  return Vector2D<double>(xp, yp);
}

Vector2D<double>
Vector2D<double>::rotate_counter_clockwise_90() const
{
  return Vector2D<double>(m_y, -m_x);
}

Vector2D<double>
Vector2D<double>::rotate_clockwise_90() const
{
  return Vector2D<double>(-m_y, m_x);
}

Vector2D<double>
Vector2D<double>::rotate_180() const
{
  return Vector2D<double>(-m_x, -m_y);
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
