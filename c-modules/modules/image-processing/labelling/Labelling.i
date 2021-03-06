// -*- C++ -*-

/* *********************************************************************************************** */

%module Labelling

/* *********************************************************************************************** */

%include "std_string.i"
%include "std_vector.i"
%include "numpy_common.i"

/* *********************************************************************************************** *
 *
 * Labelling
 *
 * 
 */

%{
#include "Island.hpp"
#include "Label.hpp"
#include "Geometry.hpp"
%}

%template(vector_island) std::vector<Island>;

%include "Island.hpp"
%include "Label.hpp"
%include "Geometry.hpp"

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
