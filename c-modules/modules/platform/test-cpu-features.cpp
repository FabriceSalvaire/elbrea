/* *********************************************************************************************** */

#include <iostream>

#include "IntelCpuTools.hpp"

using namespace std;

/* *********************************************************************************************** */

int
main()
{
  CpuFeatures cpu_features;

  cout << "Number of cores:" << number_of_cores() << endl;

  cout << "Has MMX:" << cpu_features.has[CpuFeatures::MMX] << endl;
  cout << "Has SSE:" << cpu_features.has[CpuFeatures::SSE] << endl;
  cout << "Has SSE2:" << cpu_features.has[CpuFeatures::SSE2] << endl;
  cout << "Has SSSE3:" << cpu_features.has[CpuFeatures::SSSE3] << endl;
  cout << "Has SSE3:" << cpu_features.has[CpuFeatures::SSE3] << endl;
  cout << "Has SSE4.1:" << cpu_features.has[CpuFeatures::SSE4_1] << endl;
  cout << "Has SSE4.2:" << cpu_features.has[CpuFeatures::SSE4_2] << endl;
  cout << "Has AVX:" << cpu_features.has[CpuFeatures::AVX] << endl;

  return 0;
}

/* *********************************************************************************************** */
