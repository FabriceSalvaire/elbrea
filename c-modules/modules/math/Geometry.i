// -*- C++ -*-

/* *********************************************************************************************** */

%module Geometry

/* *********************************************************************************************** */

%{
#include "Geometry.hpp"
%}

/* *********************************************************************************************** */

%apply double &OUTPUT { double &s1 };
%apply double &OUTPUT { double &s2 };

/* *********************************************************************************************** */

%include "Vector.hpp"
%include "Line.hpp"
%include "InertiaMatrix.hpp"

%template(Vector2D_traits_unsigned_int) Vector2D_traits<uint64_t>;
%template(Vector2D_traits_int) Vector2D_traits<int64_t>;
%template(Vector2D_traits_double) Vector2D_traits<double>;

%template(Vector2D_unsigned_int) Vector2D<uint64_t>;
%template(Vector2D_int) Vector2D<int64_t>;
%template(Vector2D_double) Vector2D<double>;

%template(InertiaMatrix2D_traits_int) InertiaMatrix2D_traits<int64_t>;
// %template(InertiaMatrix2D_traits_int) InertiaMatrix2D_traits<int64_t>;
%template(InertiaMatrix2D_traits_double) InertiaMatrix2D_traits<double>;

%template(InertiaMatrix2D_int) InertiaMatrix2D<int64_t>;
// %template(InertiaMatrix2D_int) InertiaMatrix2D<int64_t>;
%template(InertiaMatrix2D_double) InertiaMatrix2D<double>;

/* *********************************************************************************************** */

/*
 * End
 *
 ************************************************************************************************* */
