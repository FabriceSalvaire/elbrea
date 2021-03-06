/* *********************************************************************************************** */

#include <stdint.h>
#include <stdlib.h>

#include <iostream>
using namespace std;

/* *********************************************************************************************** */

#include "Geometry.hpp"

/* *********************************************************************************************** */

int
main()
{
  Vector2D<int64_t> v1(1, 2);
  Vector2D<int64_t> v2(3, 4);
  Vector2D<int64_t> v3;

  v3 = v1 + v2;
  v3.print_object();

  return EXIT_SUCCESS;
}

/* *********************************************************************************************** */
