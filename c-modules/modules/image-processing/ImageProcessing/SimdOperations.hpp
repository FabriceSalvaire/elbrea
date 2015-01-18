/**************************************************************************************************/

// int _mm_testz_si128 (__m128i s1, __m128i s2)
// _mm_testz_si128 := ( (s1 & s2) == 0 ? 1 : 0 )

// Loads an unaligned 128-bit value. This differs from movdqu in that
//   it can provide higher performance in some cases. However, it also
//   may provide lower performance than movdqu if the memory value being
//   read was just previously written.
//   __m128i _mm_lddqu_si128(__m128i const *p);

// __m128i _mm_stream_load_si128(__m128i* v1);

// __m128i _mm_mulhi_epu16(__m128i a, __m128i b)
// __m128i _mm_mullo_epi16(__m128i a, __m128i b)

// Zero extend 4 words into 4 double words
// __m128i _mm_cvtepu16_epi32(__m128i a) 
// __m128i _mm_cvtepi16_epi32(__m128i a) 

/**************************************************************************************************/

#ifndef __SIMDOPERATIONS_H__
#define __SIMDOPERATIONS_H__

/**************************************************************************************************/

#include <immintrin.h>

/**************************************************************************************************/

#include "Image.hpp"

/**************************************************************************************************/

struct sse_saturated_addition_uint16
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_adds_epu16(a, b);
  }
};

struct sse_saturated_subtraction_uint16
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_subs_epu16(a, b);
  }
};

struct sse_shift_left_uint16
{
  __m128i operator()(const __m128i& a, Image::PixelType count) const
  {
    return _mm_slli_epi16(a, static_cast<int>(count));
  }
};

struct sse_shift_right_uint16
{
  __m128i operator()(const __m128i& a, Image::PixelType count) const
  {
    return _mm_srli_epi16(a, static_cast<int>(count));
  }
};

struct sse_and
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_and_si128(a, b);
  }
};

struct sse_not_a_and_b
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_andnot_si128(a, b);
  }
};

struct sse_or
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_or_si128(a, b);
  }
};

struct sse_xor
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_xor_si128(a, b);
  }
};

struct sse_min_uint16
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_min_epu16(a, b);
  }
};

struct sse_max_uint16
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_max_epu16(a, b);
  }
};

struct sse_equal_uint16
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    return _mm_cmpeq_epi16(a, b);
  }
};

struct sse_not_equal_uint16
{
  __m128i operator()(const __m128i& a, const __m128i& b) const
  {
    __m128i r1 = _mm_cmpeq_epi16(a, b);
    // Fixme: what does the compiler, define a global constant ?
    __m128i true_sse = _mm_set1_epi16(static_cast<int16_t>(Image::PIXEL_SUP));
    __m128i r2 = _mm_andnot_si128(r1, true_sse);
    return r2;
  }
};

struct sse_zero_up_to_uint16
{
  __m128i operator()(const __m128i& a, Image::PixelType value) const
  {
    // Fixme: what does the compiler, define a global constant ?
    __m128i value_sse = _mm_set1_epi16(static_cast<int16_t>(value));
    __m128i zero_sse = _mm_set1_epi16(static_cast<int16_t>(Image::PIXEL_INF));
    __m128i r1 = _mm_subs_epu16(a, value_sse);
    __m128i r2 = _mm_cmpeq_epi16(r1, zero_sse);
    __m128i r3 = _mm_andnot_si128(r2, a);
    return r3;
  }
};

/**************************************************************************************************/

#endif /* __SIMDOPERATIONS_H__ */

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
