/***************************************************************************************************
 *
 * C Types:
 *    8-bit byte
 *   16-bit short int
 *   32-bit int, single precision float
 *   64-bit long long, double precision float
 *
 * Intel Intrinsics Data Types:
 *   __m64
 *   __m128  single-precision floating point
 *   __m128d double-precision floating point
 *   __m128i integer
 *   __m256  single-precision floating point
 *   __m256d double-precision floating point
 *   __m256i integer
 *
 * | x-bit | 128-bit | 256-bit | Base Type               |
 * |  8    | 16      | 32      | int8_t  uint8_t         |
 * | 16    |  8      | 16      | int16_t uint16_t        |
 * | 32    |  4      |  8      | int32_t uint32_t float  |
 * | 64    |  2      |  4      | int64_t uint64_t double |
 *
 * |         |           | 128-bit | 256-bit |
 * | int8_t  | char      | __v16qi | __v32qi |
 * | int16_t | short     | __v8hi  | __v16hi |
 * | int32_t | int       | __v4si  | __v8si  |
 * | int64_t | long long | __v2di  | __v4di  |
 * |         | float     | __v4sf  | __v8sf  |
 * |         | double    | __v2df  | __v4df  |
 *
 * mmintrin.h:  typedef int        __m64   __attribute__ ((__vector_size__ (8),  __may_alias__));
 * emmintrin.h: typedef long long  __m128i __attribute__ ((__vector_size__ (16), __may_alias__));
 * xmmintrin.h: typedef float      __m128  __attribute__ ((__vector_size__ (16), __may_alias__));
 * emmintrin.h: typedef double     __m128d __attribute__ ((__vector_size__ (16), __may_alias__));
 * avxintrin.h: typedef long long  __m256i __attribute__ ((__vector_size__ (32),
 * avxintrin.h: typedef float      __m256  __attribute__ ((__vector_size__ (32),
 * avxintrin.h: typedef double     __m256d __attribute__ ((__vector_size__ (32),
 *
 * mmintrin.h:  typedef char      __v8qi  __attribute__ ((__vector_size__ (8)));
 * mmintrin.h:  typedef float     __v2sf  __attribute__ ((__vector_size__ (8)));
 * mmintrin.h:  typedef int       __v2si  __attribute__ ((__vector_size__ (8)));
 * mmintrin.h:  typedef short     __v4hi  __attribute__ ((__vector_size__ (8)));
 *
 * emmintrin.h: typedef char      __v16qi __attribute__ ((__vector_size__ (16)));
 * emmintrin.h: typedef double    __v2df  __attribute__ ((__vector_size__ (16)));
 * emmintrin.h: typedef int       __v4si  __attribute__ ((__vector_size__ (16)));
 * emmintrin.h: typedef long long __v2di  __attribute__ ((__vector_size__ (16)));
 * emmintrin.h: typedef short     __v8hi  __attribute__ ((__vector_size__ (16)));
 * xmmintrin.h: typedef float     __v4sf  __attribute__ ((__vector_size__ (16)));
 *
 * avxintrin.h: typedef char      __v32qi __attribute__ ((__vector_size__ (32)));
 * avxintrin.h: typedef double    __v4df  __attribute__ ((__vector_size__ (32)));
 * avxintrin.h: typedef float     __v8sf  __attribute__ ((__vector_size__ (32)));
 * avxintrin.h: typedef int       __v8si  __attribute__ ((__vector_size__ (32)));
 * avxintrin.h: typedef long long __v4di  __attribute__ ((__vector_size__ (32)));
 * avxintrin.h: typedef short     __v16hi __attribute__ ((__vector_size__ (32)));
 *
 ***************************************************************************************************/

/* *********************************************************************************************** */

#ifndef __SIMD_H__
#define __SIMD_H__

/* *********************************************************************************************** */

#include <immintrin.h>
#include <stdint.h>

/* *********************************************************************************************** */

#define ALIGN_FOR_SIMD __attribute__ ((aligned(16)))

/* *********************************************************************************************** */

typedef uint8_t pvector_16_uint8_t __attribute__ ((vector_size (16)));
union vector_16_uint8_t
{
  __m128i g;
  pvector_16_uint8_t p;
  uint8_t i[16];
} ALIGN_FOR_SIMD;

typedef uint16_t pvector_8_uint16_t __attribute__ ((vector_size (16)));
union vector_8_uint16_t
{
  __m128i g;
  pvector_8_uint16_t p;
  uint16_t i[8];
}  ALIGN_FOR_SIMD;

typedef uint64_t pvector_2_uint64_t __attribute__ ((vector_size (16)));
union vector_2_uint64_t
{
  __m128i g;
  pvector_2_uint64_t p;
  uint64_t i[2];
}  ALIGN_FOR_SIMD;

typedef int64_t pvector_2_int64_t __attribute__ ((vector_size (16)));
union vector_2_int64_t
{
  __m128i g;
  pvector_2_int64_t p;
  int64_t i[2];
}  ALIGN_FOR_SIMD;

typedef float pvector_4_float_t __attribute__ ((vector_size (16)));
union vector_4_float_t
{
  __m128 g;
  pvector_4_float_t p;
  float i[4];
}  ALIGN_FOR_SIMD;

typedef double pvector_2_double_t __attribute__ ((vector_size (16)));
union vector_2_double_t
{
  __m128d g;
  pvector_2_double_t p;
  double i[2];
}  ALIGN_FOR_SIMD;

/* *********************************************************************************************** */

#ifdef USE_AVX
typedef uint8_t pvector_32_uint8_t __attribute__ ((vector_size (16)));
union vector_32_uint8_t
{
  __m256i g;
  pvector_32_uint8_t p;
  uint8_t i[32];
} ALIGN_FOR_SIMD;

typedef uint16_t pvector_16_uint16_t __attribute__ ((vector_size (16)));
union vector_16_uint16_t
{
  __m256i g;
  pvector_16_uint16_t p;
  uint16_t i[16];
}  ALIGN_FOR_SIMD;

typedef uint64_t pvector_4_uint64_t __attribute__ ((vector_size (16)));
union vector_4_uint64_t
{
  __m256i g;
  pvector_4_uint64_t p;
  uint64_t i[4];
}  ALIGN_FOR_SIMD;

typedef int64_t pvector_4_int64_t __attribute__ ((vector_size (16)));
union vector_4_int64_t
{
  __m256i g;
  pvector_4_int64_t p;
  int64_t i[4];
}  ALIGN_FOR_SIMD;

typedef float pvector_8_float_t __attribute__ ((vector_size (16)));
union vector_8_float_t
{
  __m256 g;
  pvector_8_float_t p;
  float i[8];
}  ALIGN_FOR_SIMD;

typedef double pvector_4_double_t __attribute__ ((vector_size (16)));
union vector_4_double_t
{
  __m256d g;
  pvector_4_double_t p;
  double i[4];
}  ALIGN_FOR_SIMD;
#endif

/* *********************************************************************************************** */

#endif /* __SIMD_H__ */

/* *********************************************************************************************** */
