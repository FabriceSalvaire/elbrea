/* *********************************************************************************************** */

#ifndef __InertiaMatrix_H__
#define __InertiaMatrix_H__

/* *********************************************************************************************** */

#include <iostream>

using namespace std;

/* *********************************************************************************************** */

#include "Vector.hpp"

/* *********************************************************************************************** */

template<typename T> class InertiaMatrix2D;

template<typename T> class InertiaMatrix2D_traits
{
public: // static
  static const char * class_name; // Fixme: Warning 451: Setting a const char * variable may leak memory.

public: // Accessors
  virtual T xx() const = 0;
  virtual T yy() const = 0;
  virtual T xy() const = 0;

public: // Methods
  bool operator==(const InertiaMatrix2D<T> & other)
  {
    return xx() == other.xx() && yy() == other.yy() && xy() == other.xy();
  }

  void print_object() const // _object for Python
  {
    std::cout << class_name << " (" << xx() << ", " << yy() << ", " << xy() << ")" << std::endl;
  }
};

template<typename T> class InertiaMatrix2D : public InertiaMatrix2D_traits<T>
{
// we will specialise the class for each type
};

/* *********************************************************************************************** */

template<> class InertiaMatrix2D<int> : public InertiaMatrix2D_traits<int>
{
public: // Ctors
  InertiaMatrix2D();
  InertiaMatrix2D(int xx, int yy, int xy);
  InertiaMatrix2D(const InertiaMatrix2D<int> & other);

public: // Accessors
  inline int xx() const { return m_xx; };
  inline int yy() const { return m_yy; };
  inline int xy() const { return m_xy; };

public: // Methods
  InertiaMatrix2D<int> & operator+=(const InertiaMatrix2D<int> & other);
  InertiaMatrix2D<int> & operator+=(const Vector2D<int> & vector);
  InertiaMatrix2D<int> & operator+=(const Vector2D<unsigned int> & vector);
  InertiaMatrix2D<int> & operator*=(int scale);

private: // Members
  int m_xx;
  int m_yy;
  int m_xy;
};

/* *********************************************************************************************** */

template<> class InertiaMatrix2D<double> : public InertiaMatrix2D_traits<double>
{
public: // Ctors
  InertiaMatrix2D();
  InertiaMatrix2D(double xx, double yy, double xy);
  InertiaMatrix2D(const InertiaMatrix2D<double> & other);

public: // Accessors
  inline double xx() const { return m_xx; };
  inline double yy() const { return m_yy; };
  inline double xy() const { return m_xy; };

public: // Methods
  InertiaMatrix2D<double> & operator+=(const InertiaMatrix2D<double> & other);
  InertiaMatrix2D<double> & operator+=(const Vector2D<double> & vector);
  InertiaMatrix2D<double> & operator+=(const Vector2D<unsigned int> & vector);
  InertiaMatrix2D<double> & operator*=(double scale);

private: // Members
  double m_xx;
  double m_yy;
  double m_xy;
};

/* *********************************************************************************************** */

#endif /* __InertiaMatrix_H__ */

/* *********************************************************************************************** */
