/* *********************************************************************************************** */

#ifndef __Line_H__
#define __Line_H__

/* *********************************************************************************************** */

#include <iostream>

using namespace std;

/* *********************************************************************************************** */

#include "Vector.hpp"

/* *********************************************************************************************** */

class Line2D
{
public: // Ctors
  Line2D(const Vector2D<double> & point, const Vector2D<double> & vector);

public: // Accessors
  inline Vector2D<double> & point() { return m_point; };
  inline Vector2D<double> & vector() { return m_vector; };

public: // Methods
  void print_object() const;
  Vector2D<double> point_at_s(double s) const;
  Vector2D<double> point_at_distance(double d) const;
  double get_y_from_x(double x) const;
  double get_x_from_y(double y) const;
  Line2D shifted_parallel_line(double shift) const;
  Line2D orthogonal_line_at_abscissa(double s) const;
  bool is_parallel(const Line2D &  other) const;
  bool is_orthogonal(const Line2D & other) const;
  bool intersection_abscissae(const Line2D & other, double & s1, double & s2) const;
  Vector2D<double> intersection(const Line2D & other) const;
  void distance_to_line(const Vector2D<double> & at_point, double & s1, double & s2) const;

private: // Members
  Vector2D<double> m_point;
  Vector2D<double> m_vector;
};

/* *********************************************************************************************** */

#endif /* __Line_H__ */

/* *********************************************************************************************** */
