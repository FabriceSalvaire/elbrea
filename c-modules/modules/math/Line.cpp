/* *********************************************************************************************** */

#include <climits>
#include <cmath>
#include <cstdlib>
#include <iostream>

/* *********************************************************************************************** */

#include "Math.hpp"
#include "Line.hpp"

/* *********************************************************************************************** */
  
Line2D::Line2D(const Vector2D<double> & point, const Vector2D<double> & vector)
  : m_point(point), m_vector(vector)
{}

void
Line2D::print_object() const
{
  std::cout << "Line2D" << std::endl;
  m_point.print_object();
  m_vector.print_object();
  std::cout << "magnitude " << m_vector.magnitude() << std::endl;
}

Vector2D<double>
Line2D::point_at_s(double s) const
{
  Vector2D<double> p(m_vector);

  p *= s;
  p += m_point;

  return p;
}

Vector2D<double>
Line2D::point_at_distance(double d) const
{
  Vector2D<double> p(m_vector);

  p *= d / m_vector.magnitude();
  p += m_point;

  return p;
}

double
Line2D::get_y_from_x(double x) const
{
  return m_vector.slope() * (x - m_point.x()) + m_point.y();
}

double
Line2D::get_x_from_y(double y) const
{
  return m_vector.slope_inverse() * (y - m_point.y()) + m_point.x();
}

Line2D
Line2D::shifted_parallel_line(double shift) const
{
  Vector2D<double> n = m_vector.rotate_counter_clockwise_90();
  n.normalise();
  n *= shift;

  Vector2D<double> p(m_point);
  p += n;

  return Line2D(p, m_vector);
}

Line2D
Line2D::orthogonal_line_at_abscissa(double s) const
{
  Vector2D<double> p = point_at_s(s);
  Vector2D<double> v = m_vector.rotate_counter_clockwise_90();
    
  return Line2D(p, v);
}

bool
Line2D::is_parallel(const Line2D & other) const
{
  return m_vector.is_parallel(other.m_vector);
}

bool
Line2D::is_orthogonal(const Line2D & other) const
{
  return m_vector.is_orthogonal(other.m_vector);
}

bool
Line2D::intersection_abscissae(const Line2D & other, double & s1, double & s2) const
{
  if (is_parallel(other) == true)
    return false;

  double n = 1. / m_vector.cross(other.m_vector);

  Vector2D<double> delta(other.m_point);
  delta -= m_point;
  
  s1 = delta.cross(other.m_vector) * n;
  s2 = delta.cross(m_vector) * n;

  return true;
}

Vector2D<double>
Line2D::intersection(const Line2D & other) const
{
  double s1, s2;

  if (intersection_abscissae(other, s1, s2))
    return point_at_s(s1);
  else
    return Vector2D<double>(NAN, NAN);
}

void
Line2D::distance_to_line(const Vector2D<double> & at_point, double & s1, double & s2) const
{
  Vector2D<double> delta(at_point);
  delta -= m_point;

  double side = copysign(1., m_vector.cross(delta));
  
  double t = m_vector.dot(delta) / m_vector.magnitude_square();
  Vector2D<double> pt = point_at_s(t);

  Vector2D<double> p1(pt);
  p1 -= at_point;
  s1 = side * p1.magnitude();

  s2 = t * m_vector.magnitude();
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
