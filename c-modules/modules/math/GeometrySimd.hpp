/* *********************************************************************************************** */

#ifndef __GeometrySimd_H__
#define __GeometrySimd_H__

/* *********************************************************************************************** */

#include <stdint.h>

#include <iostream>
using namespace std;

/* *********************************************************************************************** */

#include "../common/Simd.hpp"

/* *********************************************************************************************** */

template<typename T> class Vector2D;

template<typename T> class Vector2D_traits
{
public: // Standard typedef
  typedef Vector2D<T> Self;

public:
  const size_t X = 0;
  const size_t Y = 1;

public: // static
  static const char * class_name; // Fixme: Warning 451: Setting a const char * variable may leak memory.

public: // Accessors
  virtual T x() const = 0;
  virtual T y() const = 0;

public: // Methods
  bool operator==(const Vector2D<T> & other)
  {
    return x() == other.x() && y() == other.y();
  }

  void print_object() const // _object for Python
  {
    std::cout << class_name << " (" << x() << ", " << y() << ")" << std::endl;
  }
};

template<typename T> class Vector2D : public Vector2D_traits<T>
{
// we will specialise the class for each type
};

/* *********************************************************************************************** */

template<> class Vector2D<int64_t> : public Vector2D_traits<int64_t> // not sure how to do?
{
public: // Standard typedef
  typedef pvector_2_int64_t pvector_t;
  typedef vector_2_int64_t vector_t;

public: // Ctors
  Vector2D();
  Vector2D(const pvector_t v);
  Vector2D(const vector_t v);
  Vector2D(int64_t x, int64_t y);
  Vector2D(const Vector2D<int64_t> & other);

public: // Accessors
  inline int64_t x() const { return m_v.i[X]; };
  inline int64_t y() const { return m_v.i[Y]; };

  inline int64_t x(int64_t x) { m_v.i[X] = x; return m_v.i[X]; };
  inline int64_t y(int64_t y) { m_v.i[Y] = y; return m_v.i[Y]; };

public: // Methods
  Vector2D<int64_t> & operator=(const Vector2D<int64_t> & other)
  {
    m_v.p = other.m_v.p;
    return *this;
  }
  
  /*
  bool operator==(const Vector2D<int64_t> & other)
  {
    return m_v == other.m_v;
  }
  */

  Vector2D<int64_t> operator-(const Vector2D<int64_t> & other) const;
  Vector2D<int64_t> operator+(const Vector2D<int64_t> & other) const;
  Vector2D<int64_t> operator*(int64_t scale) const;

  Vector2D<int64_t> & operator-=(const Vector2D<int64_t> & other);
  Vector2D<int64_t> & operator+=(const Vector2D<int64_t> & other);
  Vector2D<int64_t> & operator*=(int64_t scale);

private: // Members
  vector_t m_v;
};

// // /* *********************************************************************************************** */
// // 
// // template<> class Vector2D<uint64_t> : public Vector2D_traits<uint64_t> // not sure how to do?
// // {
// // public: // Ctors
// //   Vector2D();
// //   Vector2D(uint64_t x, uint64_t y);
// //   Vector2D(const Vector2D<uint64_t> & other);
// // 
// // public: // Accessors
// //   inline uint64_t x() const { return m_v.i[X]; };
// //   inline uint64_t y() const { return m_v.i[Y]; };
// // 
// //   inline uint64_t x(uint64_t x) { m_v.i[X] = x; return m_v.i[X]; };
// //   inline uint64_t y(uint64_t y) { m_v.i[Y] = y; return m_v.i[Y]; };
// // 
// // public: // Methods
// //   /*
// //   bool operator==(const Vector2D<uint64_t> & other)
// //   {
// //     return m_v == other.m_v;
// //   }
// //   */
// // 
// //   Vector2D<uint64_t> operator-(const Vector2D<uint64_t> & other) const;
// //   Vector2D<uint64_t> operator+(const Vector2D<uint64_t> & other) const;
// //   Vector2D<uint64_t> operator*(uint64_t scale) const;
// // 
// //   Vector2D<uint64_t> & operator-=(const Vector2D<uint64_t> & other);
// //   Vector2D<uint64_t> & operator+=(const Vector2D<uint64_t> & other);
// //   Vector2D<uint64_t> & operator-=(const Vector2D<int64_t> & other);
// //   Vector2D<uint64_t> & operator+=(const Vector2D<int64_t> & other);
// //   Vector2D<uint64_t> & operator*=(uint64_t scale);
// // 
// // private: // Members
// //   vector_2_uint64_t m_v;
// // };
// // 
// // /* *********************************************************************************************** */
// // 
// // template<> class Vector2D<double> : public Vector2D_traits<double>
// // {
// // public: // Ctors
// //   Vector2D();
// //   Vector2D(double angle);
// //   Vector2D(double x, double y);
// //   Vector2D(const Vector2D<double> & other);
// // 
// // public: // Accessors
// //   inline double x() const { return m_v.i[X]; };
// //   inline double y() const { return m_v.i[Y]; };
// // 
// //   inline double x(double x) { m_v.i[X] = x; return m_v.i[X]; };
// //   inline double y(double y) { m_v.i[Y] = y; return m_v.i[Y]; };
// // 
// // public: // Methods
// //   /*
// //   bool operator==(const Vector2D<double> & other)
// //   {
// //     return m_v == other.m_v;
// //   }
// //   */
// // 
// //   Vector2D<double> operator-(const Vector2D<double> & other) const;
// //   Vector2D<double> operator+(const Vector2D<double> & other) const;
// //   Vector2D<double> operator*(double scale) const;
// // 
// //   Vector2D<double> & operator-=(const Vector2D<double> & other);
// //   Vector2D<double> & operator+=(const Vector2D<double> & other);
// //   Vector2D<double> & operator*=(double scale);
// // 
// //   void normalise();
// // 
// //   double magnitude_square() const;
// //   double magnitude() const;
// //   double slope() const;
// //   double slope_inverse() const;
// //   double orientation() const;
// //   double dot(const Vector2D<double> & other) const;
// //   double cross(const Vector2D<double> & other) const;
// //   bool is_parallel(const Vector2D<double> & other) const;
// //   bool is_orthogonal(const Vector2D<double> & other) const;
// //   double cos_with(const Vector2D<double> & other) const;
// //   double sin_with(const Vector2D<double> & other) const;
// //   double orientation_with(const Vector2D<double> & other) const;
// //   double deviation_with(const Vector2D<double> & other) const;
// //   Vector2D<double> rotate_counter_clockwise(double angle) const;
// //   Vector2D<double> rotate_counter_clockwise_90() const;
// //   Vector2D<double> rotate_clockwise_90() const; 
// //   Vector2D<double> rotate_180() const;
// // 
// // private: // Members
// //   vector_2_double_t m_v;  
// // };
// // 
// // /* *********************************************************************************************** */
// // 
// // class Line2D
// // {
// // public: // Ctors
// //   Line2D(const Vector2D<double> & point, const Vector2D<double> & vector);
// // 
// // public: // Accessors
// //   inline Vector2D<double> & point() { return m_point; };
// //   inline Vector2D<double> & vector() { return m_vector; };
// // 
// // public: // Methods
// //   void print_object() const;
// //   Vector2D<double> point_at_s(double s) const;
// //   Vector2D<double> point_at_distance(double d) const;
// //   double get_y_from_x(double x) const;
// //   double get_x_from_y(double y) const;
// //   Line2D shifted_parallel_line(double shift) const;
// //   Line2D orthogonal_line_at_abscissa(double s) const;
// //   bool is_parallel(const Line2D &  other) const;
// //   bool is_orthogonal(const Line2D & other) const;
// //   bool intersection_abscissae(const Line2D & other, double & s1, double & s2) const;
// //   Vector2D<double> intersection(const Line2D & other) const;
// //   void distance_to_line(const Vector2D<double> & at_point, double & s1, double & s2) const;
// // 
// // private: // Members
// //   Vector2D<double> m_point;
// //   Vector2D<double> m_vector;
// // };
// // 
// // /* *********************************************************************************************** */
// // 
// // template<typename T> class InertiaMatrix2D;
// // 
// // template<typename T> class InertiaMatrix2D_traits
// // {
// // public: // static
// //   static const char * class_name; // Fixme: Warning 451: Setting a const char * variable may leak memory.
// // 
// // public: // Accessors
// //   virtual T xx() const = 0;
// //   virtual T yy() const = 0;
// //   virtual T xy() const = 0;
// // 
// // public: // Methods
// //   bool operator==(const InertiaMatrix2D<T> & other)
// //   {
// //     return xx() == other.xx() && yy() == other.yy() && xy() == other.xy();
// //   }
// // 
// //   void print_object() const // _object for Python
// //   {
// //     std::cout << class_name << " (" << xx() << ", " << yy() << ", " << xy() << ")" << std::endl;
// //   }
// // };
// // 
// // template<typename T> class InertiaMatrix2D : public InertiaMatrix2D_traits<T>
// // {
// // // we will specialise the class for each type
// // };
// // 
// // /* *********************************************************************************************** */
// // 
// // template<> class InertiaMatrix2D<int> : public InertiaMatrix2D_traits<int>
// // {
// // public: // Ctors
// //   InertiaMatrix2D();
// //   InertiaMatrix2D(int xx, int yy, int xy);
// //   InertiaMatrix2D(const InertiaMatrix2D<int> & other);
// // 
// // public: // Accessors
// //   inline int xx() const { return m_xx; };
// //   inline int yy() const { return m_yy; };
// //   inline int xy() const { return m_xy; };
// // 
// // public: // Methods
// //   InertiaMatrix2D<int> & operator+=(const InertiaMatrix2D<int> & other);
// //   InertiaMatrix2D<int> & operator+=(const Vector2D<int> & vector);
// //   InertiaMatrix2D<int> & operator+=(const Vector2D<uint64_t> & vector);
// //   InertiaMatrix2D<int> & operator*=(int scale);
// // 
// // private: // Members
// //   int m_xx;
// //   int m_yy;
// //   int m_xy;
// // };
// // 
// // /* *********************************************************************************************** */
// // 
// // template<> class InertiaMatrix2D<double> : public InertiaMatrix2D_traits<double>
// // {
// // public: // Ctors
// //   InertiaMatrix2D();
// //   InertiaMatrix2D(double xx, double yy, double xy);
// //   InertiaMatrix2D(const InertiaMatrix2D<double> & other);
// // 
// // public: // Accessors
// //   inline double xx() const { return m_xx; };
// //   inline double yy() const { return m_yy; };
// //   inline double xy() const { return m_xy; };
// // 
// // public: // Methods
// //   InertiaMatrix2D<double> & operator+=(const InertiaMatrix2D<double> & other);
// //   InertiaMatrix2D<double> & operator+=(const Vector2D<double> & vector);
// //   InertiaMatrix2D<double> & operator+=(const Vector2D<uint64_t> & vector);
// //   InertiaMatrix2D<double> & operator*=(double scale);
// // 
// // private: // Members
// //   double m_xx;
// //   double m_yy;
// //   double m_xy;
// // };

/* *********************************************************************************************** */

#endif /* __GeometrySimd_H__ */

/* *********************************************************************************************** */
