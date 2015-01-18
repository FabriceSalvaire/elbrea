/* *********************************************************************************************** */

#include <climits>
#include <cmath>
#include <cstdlib>
#include <iostream>

/* *********************************************************************************************** */

#include "Math.hpp"
#include "InertiaMatrix.hpp"

/* *********************************************************************************************** */

template<> const char * InertiaMatrix2D_traits<int>::class_name = "InertiaMatrix2D<int>";

InertiaMatrix2D<int>::InertiaMatrix2D()
  : m_xx(.0), m_yy(.0), m_xy(.0)
{
}

InertiaMatrix2D<int>::InertiaMatrix2D(int xx, int yy, int xy)
  : m_xx(xx), m_yy(yy), m_xy(xy)
{
}

InertiaMatrix2D<int>::InertiaMatrix2D(const InertiaMatrix2D<int> & other)
  : m_xx(other.m_xx), m_yy(other.m_yy), m_xy(other.m_xy)
{
}

InertiaMatrix2D<int> &
InertiaMatrix2D<int>::operator+=(const InertiaMatrix2D<int> & other)
{
  m_xx += other.m_xx;
  m_yy += other.m_yy;
  m_xy += other.m_xy;

  return *this;
}

InertiaMatrix2D<int> &
InertiaMatrix2D<int>::operator+=(const Vector2D<int> & vector)
{
  m_xx += vector.y()*vector.y();
  m_yy += vector.x()*vector.x();
  m_xy -= vector.x()*vector.y();

  return *this;
}

InertiaMatrix2D<int> &
InertiaMatrix2D<int>::operator+=(const Vector2D<unsigned int> & vector)
{
  m_xx += vector.y()*vector.y();
  m_yy += vector.x()*vector.x();
  m_xy -= vector.x()*vector.y();

  return *this;
}

InertiaMatrix2D<int> &
InertiaMatrix2D<int>::operator*=(int scale)
{
  m_xx *= scale;
  m_yy *= scale;
  m_xy *= scale;

  return *this;
}

/* *********************************************************************************************** */

template<> const char * InertiaMatrix2D_traits<double>::class_name = "InertiaMatrix2D<double>";

InertiaMatrix2D<double>::InertiaMatrix2D()
  : m_xx(.0), m_yy(.0), m_xy(.0)
{
}

InertiaMatrix2D<double>::InertiaMatrix2D(double xx, double yy, double xy)
  : m_xx(xx), m_yy(yy), m_xy(xy)
{
}

InertiaMatrix2D<double>::InertiaMatrix2D(const InertiaMatrix2D<double> & other)
  : m_xx(other.m_xx), m_yy(other.m_yy), m_xy(other.m_xy)
{
}

InertiaMatrix2D<double> &
InertiaMatrix2D<double>::operator+=(const InertiaMatrix2D<double> & other)
{
  m_xx += other.m_xx;
  m_yy += other.m_yy;
  m_xy += other.m_xy;

  return *this;
}

InertiaMatrix2D<double> &
InertiaMatrix2D<double>::operator+=(const Vector2D<double> & vector)
{
  m_xx += vector.y()*vector.y();
  m_yy += vector.x()*vector.x();
  m_xy -= vector.x()*vector.y();

  return *this;
}

InertiaMatrix2D<double> &
InertiaMatrix2D<double>::operator+=(const Vector2D<unsigned int> & vector)
{
  m_xx += static_cast<double>(vector.y()*vector.y());
  m_yy += static_cast<double>(vector.x()*vector.x());
  m_xy -= static_cast<double>(vector.x()*vector.y());

  return *this;
}

InertiaMatrix2D<double> &
InertiaMatrix2D<double>::operator*=(double scale)
{
  m_xx *= scale;
  m_yy *= scale;
  m_xy *= scale;

  return *this;
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
