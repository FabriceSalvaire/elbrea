/* *********************************************************************************************** */

#include <climits>
#include <cmath>
#include <cstdlib>
#include <iostream>

#include "Math.hpp"
#include "GeometrySimd.hpp"

/* *********************************************************************************************** */

// // template<> const char * Vector2D_traits<uint64_t>::class_name = "Vector2D<uint64_t>";
// // 
// // Vector2D<uint64_t>::Vector2D()
// // {
// //   m_v.p = {0, 0};
// // }
// // 
// // Vector2D<uint64_t>::Vector2D(uint64_t x, uint64_t y)
// // {
// //   m_v.p = {x, y};
// // }
// // 
// // Vector2D<uint64_t>::Vector2D(const Vector2D<uint64_t> & other)
// // {
// //   m_v.p = other.m_v.p;
// // }
// // 
// // Vector2D<uint64_t>
// // Vector2D<uint64_t>::operator-(const Vector2D<uint64_t> & other) const
// // {
// //   _m128
// // 
// //   uint64_t x = m_x - other.m_x;
// //   uint64_t y = m_y - other.m_y;
// // 
// //   return Vector2D<uint64_t>(x, y);
// // }
// // 
// // Vector2D<uint64_t>
// // Vector2D<uint64_t>::operator+(const Vector2D<uint64_t> & other) const
// // {
// //   uint64_t x = m_x + other.m_x;
// //   uint64_t y = m_y + other.m_y;
// // 
// //   return Vector2D<uint64_t>(x, y);
// // }
// // 
// // Vector2D<uint64_t>
// // Vector2D<uint64_t>::operator*(uint64_t scale) const
// // {
// //   uint64_t x = m_x * scale;
// //   uint64_t y = m_y * scale;
// // 
// //   return Vector2D<uint64_t>(x, y);
// // }
// // 
// // Vector2D<uint64_t> &
// // Vector2D<uint64_t>::operator-=(const Vector2D<uint64_t> & other)
// // {
// //   m_x -= other.m_x;
// //   m_y -= other.m_y;
// // 
// //   return *this;
// // }
// // 
// // Vector2D<uint64_t> &
// // Vector2D<uint64_t>::operator+=(const Vector2D<uint64_t> & other)
// // {
// //   m_x += other.m_x;
// //   m_y += other.m_y;
// // 
// //   return *this;
// // }
// // 
// // Vector2D<uint64_t> &
// // Vector2D<uint64_t>::operator-=(const Vector2D<int64_t> & other)
// // {
// //   m_x -= other.x();
// //   m_y -= other.y();
// // 
// //   return *this;
// // }
// // 
// // Vector2D<uint64_t> &
// // Vector2D<uint64_t>::operator+=(const Vector2D<int64_t> & other)
// // {
// //   m_x += other.x();
// //   m_y += other.y();
// // 
// //   return *this;
// // }
// // 
// // Vector2D<uint64_t> &
// // Vector2D<uint64_t>::operator*=(uint64_t scale)
// // {
// //   m_x *= scale;
// //   m_y *= scale;
// // 
// //   return *this;
// // }

/* *********************************************************************************************** */

template<> const char * Vector2D_traits<int64_t>::class_name = "Vector2D<int64_t>";

Vector2D<int64_t>::Vector2D()
{
  // warning: non-static data member initializers only available with -std=c++11 or -std=gnu++11 [enabled by default]
  m_v.p = (pvector_t){0, 0};
}

Vector2D<int64_t>::Vector2D(int64_t x, int64_t y)
{
  m_v.p = (pvector_t){x, y};
}

Vector2D<int64_t>::Vector2D(const pvector_t v)
{
  m_v.p = v;
}

Vector2D<int64_t>::Vector2D(const vector_t v)
{
  m_v.p = v.p;
}

Vector2D<int64_t>::Vector2D(const Vector2D<int64_t> & other)
{
  m_v.p = other.m_v.p;
}

Vector2D<int64_t>
Vector2D<int64_t>::operator-(const Vector2D<int64_t> & other) const
{
  pvector_t v1;
  v1 = m_v.p - other.m_v.p;

  return Vector2D<int64_t>(v1);
}

Vector2D<int64_t>
Vector2D<int64_t>::operator+(const Vector2D<int64_t> & other) const
{
  pvector_t v1;
  v1 = m_v.p + other.m_v.p;

  return Vector2D<int64_t>(v1);
}

Vector2D<int64_t>
Vector2D<int64_t>::operator*(int64_t scale) const
{
  /*
  pvector_t v1;
  pvector_t v_scale = {scale, scale};
  v1 = m_v.p * v_scale;

  return Vector2D<int64_t>(v1);
  */

  return Vector2D<int64_t>(x() * scale, y() * scale);
}

Vector2D<int64_t> &
Vector2D<int64_t>::operator-=(const Vector2D<int64_t> & other)
{
  m_v.p -= other.m_v.p;

  return *this;
}

Vector2D<int64_t> &
Vector2D<int64_t>::operator+=(const Vector2D<int64_t> & other)
{
  m_v.p += other.m_v.p;

  return *this;
}

Vector2D<int64_t> &
Vector2D<int64_t>::operator*=(int64_t scale)
{
  pvector_t v_scale = {scale, scale};
  m_v.p *= v_scale;

  return *this;
}

// // /* *********************************************************************************************** */
// // 
// // template<> const char * Vector2D_traits<double>::class_name = "Vector2D<double>";
// // 
// // Vector2D<double>::Vector2D()
// //   : m_x(.0), m_y(.0)
// // {}
// // 
// // Vector2D<double>::Vector2D(double angle)
// // {
// //   double rad = deg2rad(angle);
// // 
// //   m_x = cos(rad);
// //   m_y = sin(rad);
// // }
// // 
// // Vector2D<double>::Vector2D(double x, double y)
// //   : m_x(x), m_y(y)
// // {}
// // 
// // Vector2D<double>::Vector2D(const Vector2D<double> & other)
// //   : m_x(other.m_x), m_y(other.m_y)
// // {}
// // 
// // Vector2D<double>
// // Vector2D<double>::operator-(const Vector2D<double> & other) const
// // {
// //   double x = m_x - other.m_x;
// //   double y = m_y - other.m_y;
// // 
// //   return Vector2D<double>(x, y);
// // }
// // 
// // Vector2D<double>
// // Vector2D<double>::operator+(const Vector2D<double> & other) const
// // {
// //   double x = m_x + other.m_x;
// //   double y = m_y + other.m_y;
// // 
// //   return Vector2D<double>(x, y);
// // }
// // 
// // Vector2D<double>
// // Vector2D<double>::operator*(double scale) const
// // {
// //   double x = m_x * scale;
// //   double y = m_y * scale;
// // 
// //   return Vector2D<double>(x, y);
// // }
// // 
// // Vector2D<double> &
// // Vector2D<double>::operator-=(const Vector2D<double> & other)
// // {
// //   m_x -= other.m_x;
// //   m_y -= other.m_y;
// // 
// //   return *this;
// // }
// // 
// // Vector2D<double> &
// // Vector2D<double>::operator+=(const Vector2D<double> & other)
// // {
// //   m_x += other.m_x;
// //   m_y += other.m_y;
// // 
// //   return *this;
// // }
// // 
// // Vector2D<double> &
// // Vector2D<double>::operator*=(double scale)
// // {
// //   m_x *= scale;
// //   m_y *= scale;
// // 
// //   return *this;
// // }
// // 
// // double
// // Vector2D<double>::magnitude_square() const
// // {
// //   double f1 = m_x*m_x;
// //   double f2 = m_y*m_y;
// // 
// //   return f1 + f2;
// // }
// // 
// // double
// // Vector2D<double>::magnitude() const
// // {
// //   return sqrt(magnitude_square());
// // }
// // 
// // void
// // Vector2D<double>::normalise()
// // {
// //   *this *= 1. / magnitude(); // scale, better way?
// // }
// // 
// // double
// // Vector2D<double>::slope() const
// // {
// //   return m_y / m_x;
// // }
// // 
// // double
// // Vector2D<double>::slope_inverse() const
// // {
// //   return m_x / m_y;
// // }
// // 
// // double
// // Vector2D<double>::orientation() const
// // {
// //   return rad2deg(atan(slope()));
// // }
// // 
// // double
// // Vector2D<double>::dot(const Vector2D<double> & other) const
// // {
// //   double f1 = m_x*other.m_x;
// //   double f2 = m_y*other.m_y;
// // 
// //   return f1 + f2;
// // }
// // 
// // double
// // Vector2D<double>::cross(const Vector2D<double> & other) const
// // {
// //   double f1 = m_x*other.m_y;
// //   double f2 = m_y*other.m_x;
// // 
// //   return f1 - f2;
// // }
// // 
// // bool
// // Vector2D<double>::is_parallel(const Vector2D<double> & other) const
// // {
// //   // Fixme
// // 
// //   return (fabs(cross(other)) < 1e-6) ? true : false;
// // }
// // 
// // bool
// // Vector2D<double>::is_orthogonal(const Vector2D<double> & other) const
// // {
// //   return (fabs(dot(other)) < 1e-6) ? true : false;
// // }
// // 
// // double
// // Vector2D<double>::cos_with(const Vector2D<double> & other) const
// // {
// //   double scale = magnitude() * other.magnitude();
// // 
// //   return dot(other) / scale;
// // }
// // 
// // double
// // Vector2D<double>::sin_with(const Vector2D<double> & other) const
// // {
// //   double scale = magnitude() * other.magnitude();
// // 
// //   return cross(other) / scale;
// // }
// // 
// // double
// // Vector2D<double>::orientation_with(const Vector2D<double> & other) const
// // {
// //   return rad2deg(acos(cos_with(other)));
// // }
// // 
// // double
// // Vector2D<double>::deviation_with(const Vector2D<double> & other) const
// // {
// //   return magnitude() * sin_with(other);
// // }
// // 
// // Vector2D<double>
// // Vector2D<double>::rotate_counter_clockwise(double angle) const
// // {
// //   double rad = rad2deg(angle);
// // 
// //   double c = cos(rad);
// //   double s = sin(rad);
// // 
// //   double xp = c*m_x - s*m_y;
// //   double yp = s*m_x + c*m_y;
// // 
// //   return Vector2D<double>(xp, yp);
// // }
// // 
// // Vector2D<double>
// // Vector2D<double>::rotate_counter_clockwise_90() const
// // {
// //   return Vector2D<double>(m_y, -m_x);
// // }
// // 
// // Vector2D<double>
// // Vector2D<double>::rotate_clockwise_90() const
// // {
// //   return Vector2D<double>(-m_y, m_x);
// // }
// // 
// // Vector2D<double>
// // Vector2D<double>::rotate_180() const
// // {
// //   return Vector2D<double>(-m_x, -m_y);
// // }
// // 
// // /* *********************************************************************************************** */
// //   
// // Line2D::Line2D(const Vector2D<double> & point, const Vector2D<double> & vector)
// //   : m_point(point), m_vector(vector)
// // {}
// // 
// // void
// // Line2D::print_object() const
// // {
// //   std::cout << "Line2D" << std::endl;
// //   m_point.print_object();
// //   m_vector.print_object();
// //   std::cout << "magnitude " << m_vector.magnitude() << std::endl;
// // }
// // 
// // Vector2D<double>
// // Line2D::point_at_s(double s) const
// // {
// //   Vector2D<double> p(m_vector);
// // 
// //   p *= s;
// //   p += m_point;
// // 
// //   return p;
// // }
// // 
// // Vector2D<double>
// // Line2D::point_at_distance(double d) const
// // {
// //   Vector2D<double> p(m_vector);
// // 
// //   p *= d / m_vector.magnitude();
// //   p += m_point;
// // 
// //   return p;
// // }
// // 
// // double
// // Line2D::get_y_from_x(double x) const
// // {
// //   return m_vector.slope() * (x - m_point.x()) + m_point.y();
// // }
// // 
// // double
// // Line2D::get_x_from_y(double y) const
// // {
// //   return m_vector.slope_inverse() * (y - m_point.y()) + m_point.x();
// // }
// // 
// // Line2D
// // Line2D::shifted_parallel_line(double shift) const
// // {
// //   Vector2D<double> n = m_vector.rotate_counter_clockwise_90();
// //   n.normalise();
// //   n *= shift;
// // 
// //   Vector2D<double> p(m_point);
// //   p += n;
// // 
// //   return Line2D(p, m_vector);
// // }
// // 
// // Line2D
// // Line2D::orthogonal_line_at_abscissa(double s) const
// // {
// //   Vector2D<double> p = point_at_s(s);
// //   Vector2D<double> v = m_vector.rotate_counter_clockwise_90();
// //     
// //   return Line2D(p, v);
// // }
// // 
// // bool
// // Line2D::is_parallel(const Line2D & other) const
// // {
// //   return m_vector.is_parallel(other.m_vector);
// // }
// // 
// // bool
// // Line2D::is_orthogonal(const Line2D & other) const
// // {
// //   return m_vector.is_orthogonal(other.m_vector);
// // }
// // 
// // bool
// // Line2D::intersection_abscissae(const Line2D & other, double & s1, double & s2) const
// // {
// //   if (is_parallel(other) == true)
// //     return false;
// // 
// //   double n = 1. / m_vector.cross(other.m_vector);
// // 
// //   Vector2D<double> delta(other.m_point);
// //   delta -= m_point;
// //   
// //   s1 = delta.cross(other.m_vector) * n;
// //   s2 = delta.cross(m_vector) * n;
// // 
// //   return true;
// // }
// // 
// // Vector2D<double>
// // Line2D::intersection(const Line2D & other) const
// // {
// //   double s1, s2;
// // 
// //   if (intersection_abscissae(other, s1, s2))
// //     return point_at_s(s1);
// //   else
// //     return Vector2D<double>(NAN, NAN);
// // }
// // 
// // void
// // Line2D::distance_to_line(const Vector2D<double> & at_point, double & s1, double & s2) const
// // {
// //   Vector2D<double> delta(at_point);
// //   delta -= m_point;
// // 
// //   double side = sign_of(m_vector.cross(delta));
// //   
// //   double t = m_vector.dot(delta) / m_vector.magnitude_square();
// //   Vector2D<double> pt = point_at_s(t);
// // 
// //   Vector2D<double> p1(pt);
// //   p1 -= at_point;
// //   s1 = side * p1.magnitude();
// // 
// //   s2 = t * m_vector.magnitude();
// // }
// // 
// // /* *********************************************************************************************** */
// // 
// // template<> const char * InertiaMatrix2D_traits<int>::class_name = "InertiaMatrix2D<int>";
// // 
// // InertiaMatrix2D<int>::InertiaMatrix2D()
// //   : m_xx(.0), m_yy(.0), m_xy(.0)
// // {
// // }
// // 
// // InertiaMatrix2D<int>::InertiaMatrix2D(int xx, int yy, int xy)
// //   : m_xx(xx), m_yy(yy), m_xy(xy)
// // {
// // }
// // 
// // InertiaMatrix2D<int>::InertiaMatrix2D(const InertiaMatrix2D<int> & other)
// //   : m_xx(other.m_xx), m_yy(other.m_yy), m_xy(other.m_xy)
// // {
// // }
// // 
// // InertiaMatrix2D<int> &
// // InertiaMatrix2D<int>::operator+=(const InertiaMatrix2D<int> & other)
// // {
// //   m_xx += other.m_xx;
// //   m_yy += other.m_yy;
// //   m_xy += other.m_xy;
// // 
// //   return *this;
// // }
// // 
// // InertiaMatrix2D<int> &
// // InertiaMatrix2D<int>::operator+=(const Vector2D<int> & vector)
// // {
// //   m_xx += vector.y()*vector.y();
// //   m_yy += vector.x()*vector.x();
// //   m_xy -= vector.x()*vector.y();
// // 
// //   return *this;
// // }
// // 
// // InertiaMatrix2D<int> &
// // InertiaMatrix2D<int>::operator+=(const Vector2D<uint64_t> & vector)
// // {
// //   m_xx += vector.y()*vector.y();
// //   m_yy += vector.x()*vector.x();
// //   m_xy -= vector.x()*vector.y();
// // 
// //   return *this;
// // }
// // 
// // InertiaMatrix2D<int> &
// // InertiaMatrix2D<int>::operator*=(int scale)
// // {
// //   m_xx *= scale;
// //   m_yy *= scale;
// //   m_xy *= scale;
// // 
// //   return *this;
// // }
// // 
// // /* *********************************************************************************************** */
// // 
// // template<> const char * InertiaMatrix2D_traits<double>::class_name = "InertiaMatrix2D<double>";
// // 
// // InertiaMatrix2D<double>::InertiaMatrix2D()
// //   : m_xx(.0), m_yy(.0), m_xy(.0)
// // {
// // }
// // 
// // InertiaMatrix2D<double>::InertiaMatrix2D(double xx, double yy, double xy)
// //   : m_xx(xx), m_yy(yy), m_xy(xy)
// // {
// // }
// // 
// // InertiaMatrix2D<double>::InertiaMatrix2D(const InertiaMatrix2D<double> & other)
// //   : m_xx(other.m_xx), m_yy(other.m_yy), m_xy(other.m_xy)
// // {
// // }
// // 
// // InertiaMatrix2D<double> &
// // InertiaMatrix2D<double>::operator+=(const InertiaMatrix2D<double> & other)
// // {
// //   m_xx += other.m_xx;
// //   m_yy += other.m_yy;
// //   m_xy += other.m_xy;
// // 
// //   return *this;
// // }
// // 
// // InertiaMatrix2D<double> &
// // InertiaMatrix2D<double>::operator+=(const Vector2D<double> & vector)
// // {
// //   m_xx += vector.y()*vector.y();
// //   m_yy += vector.x()*vector.x();
// //   m_xy -= vector.x()*vector.y();
// // 
// //   return *this;
// // }
// // 
// // InertiaMatrix2D<double> &
// // InertiaMatrix2D<double>::operator+=(const Vector2D<uint64_t> & vector)
// // {
// //   m_xx += static_cast<double>(vector.y()*vector.y());
// //   m_yy += static_cast<double>(vector.x()*vector.x());
// //   m_xy -= static_cast<double>(vector.x()*vector.y());
// // 
// //   return *this;
// // }
// // 
// // InertiaMatrix2D<double> &
// // InertiaMatrix2D<double>::operator*=(double scale)
// // {
// //   m_xx *= scale;
// //   m_yy *= scale;
// //   m_xy *= scale;
// // 
// //   return *this;
// // }

/* *********************************************************************************************** */
