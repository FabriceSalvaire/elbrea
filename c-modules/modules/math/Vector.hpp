/* *********************************************************************************************** */

#ifndef __Vector_H__
#define __Vector_H__

/* *********************************************************************************************** */

#include <stdint.h>
#include <iostream>

using namespace std;

/* *********************************************************************************************** */

template<typename T> class Vector2D;

template<typename T> class Vector2D_traits
{
public: // static
  static const char * class_name; // Fixme: Warning 451: Setting a const char * variable may leak memory.

public: // Ctors
  Vector2D_traits()
    : m_x(), m_y()
  {}

  Vector2D_traits(T x, T y)
    : m_x(x), m_y(y)
  {}

  Vector2D_traits(const Vector2D<T> & other)
    : m_x(other.m_x), m_y(other.m_y)
  {}

public: // Accessors
  inline T x() const { return m_x; }
  inline T y() const { return m_y; }

  inline T x(T x) { m_x = x; return m_x; }
  inline T y(T y) { m_y = y; return m_y; }

public: // Methods
  Vector2D<T> operator-(const Vector2D<T> & other) const
  {
    T x = m_x - other.m_x;
    T y = m_y - other.m_y;
    
    return Vector2D<T>(x, y);
  }

  Vector2D<T> operator+(const Vector2D<T> & other) const
  {
    T x = m_x + other.m_x;
    T y = m_y + other.m_y;
    
    return Vector2D<T>(x, y);
  }

  Vector2D<T> operator*(T scale) const
  {
    T x = m_x * scale;
    T y = m_y * scale;
    
    return Vector2D<T>(x, y);
  }

  Vector2D_traits<T> & operator-=(const Vector2D<T> & other)
  {
    m_x -= other.m_x;
    m_y -= other.m_y;
    
    return *this;
  }

  Vector2D_traits<T> & operator+=(const Vector2D<T> & other)
  {
    m_x += other.m_x;
    m_y += other.m_y;
    
    return *this;
  }

  Vector2D_traits<T> & operator*=(T scale)
  {
    m_x *= scale;
    m_y *= scale;
    
    return *this;
  }

  bool operator==(const Vector2D<T> & other)
  {
    return x() == other.x() && y() == other.y();
  }

  void print_object() const // _object for Python
  {
    std::cout << class_name << " (" << x() << ", " << y() << ")" << std::endl;
  }

protected: // Members
  T m_x;
  T m_y;
};

template<typename T> class Vector2D : public Vector2D_traits<T>
{
// we will specialise the class for each type
};

/* *********************************************************************************************** */

template<> class Vector2D<int64_t> : public Vector2D_traits<int64_t> // not sure how to do?
{
public: // Ctors
  Vector2D() : Vector2D_traits<int64_t>(0, 0) {};
  Vector2D(int64_t x, int64_t y) : Vector2D_traits<int64_t>(x, y) {};
  Vector2D(const Vector2D<int64_t> & other) : Vector2D_traits<int64_t>(other) {};
};

/* *********************************************************************************************** */

template<> class Vector2D<uint64_t> : public Vector2D_traits<uint64_t> // not sure how to do?
{
public: // Ctors
  Vector2D() : Vector2D_traits<uint64_t>(0, 0) {};
  Vector2D(uint64_t x, uint64_t y) : Vector2D_traits<uint64_t>(x, y) {};
  Vector2D(const Vector2D<uint64_t> & other) : Vector2D_traits<uint64_t>(other) {};

public: // Methods
  Vector2D<uint64_t> & operator-=(const Vector2D<int64_t> & other);
  Vector2D<uint64_t> & operator+=(const Vector2D<int64_t> & other);
};

/* *********************************************************************************************** */

template<> class Vector2D<double> : public Vector2D_traits<double>
{
public: // Ctors
  Vector2D() : Vector2D_traits<double>(.0, .0) {};
  Vector2D(double x, double y) : Vector2D_traits<double>(x, y) {};
  Vector2D(const Vector2D<double> & other) : Vector2D_traits<double>(other) {};
  Vector2D(double angle);

public: // Methods
  void normalise();

  double magnitude_square() const;
  double magnitude() const;
  double slope() const;
  double slope_inverse() const;
  double orientation() const;
  double dot(const Vector2D<double> & other) const;
  double cross(const Vector2D<double> & other) const;
  bool is_parallel(const Vector2D<double> & other) const;
  bool is_orthogonal(const Vector2D<double> & other) const;
  double cos_with(const Vector2D<double> & other) const;
  double sin_with(const Vector2D<double> & other) const;
  double orientation_with(const Vector2D<double> & other) const;
  double deviation_with(const Vector2D<double> & other) const;
  Vector2D<double> rotate_counter_clockwise(double angle) const;
  Vector2D<double> rotate_counter_clockwise_90() const;
  Vector2D<double> rotate_clockwise_90() const; 
  Vector2D<double> rotate_180() const;
};

/* *********************************************************************************************** */

#endif /* __Vector_H__ */

/* *********************************************************************************************** */
