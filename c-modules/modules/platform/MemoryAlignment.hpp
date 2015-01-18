/* *********************************************************************************************** */

#ifndef __MEMORYALIGNMENT_H__
#define __MEMORYALIGNMENT_H__

/* *********************************************************************************************** */

#include <stdint.h>
#include <stdlib.h>

/* *********************************************************************************************** */

const size_t MMX_BYTE_ALIGNEMENT =  8; //  64-bit
const size_t SSE_BYTE_ALIGNEMENT = 16; // 128-bit
const size_t AVX_BYTE_ALIGNEMENT = 32; // 256-bit

const size_t MMX_BYTE_SIZE =  8; //  64-bit
const size_t SSE_BYTE_SIZE = 16; // 128-bit
const size_t AVX_BYTE_SIZE = 32; // 256-bit

extern "C" {
  bool is_pointer_aligned(size_t number_of_bytes, void *ptr);
  bool is_pointer_mmx_aligned(void *ptr);
  bool is_pointer_sse_aligned(void *ptr);
  bool is_pointer_avx_aligned(void *ptr);

  void* get_aligned_pointer(size_t number_of_bytes, void* unaligned_ptr);
  size_t get_byte_padding(size_t number_of_bytes, size_t size);

  /* posix_memalign(3) provides memory aligned allocation for POSIX Platform. */
  // glibc code is much more complicated
  int aligned_malloc(void **ptr, size_t number_of_bytes, size_t size);
  void aligned_free(void *aligned_ptr);
}

/* *********************************************************************************************** */

#endif /* __MEMORYALIGNMENT_H__ */

/* *********************************************************************************************** */
