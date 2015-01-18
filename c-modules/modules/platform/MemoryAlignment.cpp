/*
 * This code provides Memory Alignement Functions.
 * 
 * N-byte memory alignement means the address must be multiple of N,
 * thus the lowest N -1 bits must be null.
 *
 *  2-byte alignement <=>  16-bit alignement
 *  4-byte alignement <=>  32-bit alignement
 *  8-byte alignement <=>  64-bit alignement
 * 16-byte alignement <=> 128-bit alignement
 * 32-byte alignement <=> 256-bit alignement
 *
 * To align a pointer on N-byte boundary:
 *   we have to offset the pointer by N -1 and mask the value with ~(N-1).
 *   proof:
 *     p0 = m*N + o   with 0 <= o < N 
 *     p1 = p0 + N -1 = (m+1)*N + o -1
 *     p2 = p1 & ~(N-1) = (p1/N)*N = m*N if o = 0 else (m+1)*N
 *     where / denotes an integer division
 *
 */

/* *********************************************************************************************** */

#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

#include "MemoryAlignment.hpp"

/* *********************************************************************************************** */

#define DEBUG 1

/* *********************************************************************************************** */

//! Is the pointer N-byte aligned
/**
 *  \param number of bytes
 *  \param pointer
 *
 *  \return 1 if True else 0
 */
bool
is_pointer_aligned(size_t number_of_bytes, void *ptr)
{
  const size_t number_of_bytes_minus_1 = number_of_bytes -1;
  return ((size_t)ptr & number_of_bytes_minus_1) == 0L ? true : false;
}

bool
is_pointer_mmx_aligned(void *ptr)
{
  return is_pointer_aligned(MMX_BYTE_ALIGNEMENT, ptr);
}

bool
is_pointer_sse_aligned(void *ptr)
{
  return is_pointer_aligned(SSE_BYTE_ALIGNEMENT, ptr);
}

bool
is_pointer_avx_aligned(void *ptr)
{
  return is_pointer_aligned(AVX_BYTE_ALIGNEMENT, ptr);
}

//! Return a N-byte aligned pointer
/**
 *  \param number of bytes
 *  \param unaligned pointer
 *
 */
void*
get_aligned_pointer(size_t number_of_bytes, void* unaligned_ptr)
{
  const size_t number_of_bytes_minus_1 = number_of_bytes -1;
  size_t aligned_pointer = ((size_t)unaligned_ptr + number_of_bytes_minus_1) & (~number_of_bytes_minus_1);

  return (void*)aligned_pointer;
}

//! Return the padding in byte to align on N-byte boundary
/**
 *  \param number of bytes
 *  \param size in byte
 *
 */
size_t
get_byte_padding(size_t number_of_bytes, size_t size)
{
  return (size_t)(get_aligned_pointer(number_of_bytes, (void *)size)) - size;
}

/* *********************************************************************************************** */

/* POSIX_MEMALIGN(3) provides memory aligned allocation.
 * 
 * /!\ Check this code before to use it. /!\
 *
 */

const size_t POINTER_SIZE = sizeof(void*);

bool
not_a_power_of_two(size_t x)
{
  return x & (x - 1);
}

//! Return the original pointer
/**
 *  \param aligned pointer
 *
 */
void**
get_original_pointer_store(void* aligned_ptr)
{
  /* Proof:
   *   malloc ensures 8-byte alignement
   *   p0 = k*V = m*N + o   where V is the pointer size, 0 <= o < N and V <= N
   *   p1 = p0 + k = (k+1)*V = m*N + o + V
   *   p2 = p1 & ~(N-1) = (p1/N)*N = (m+i)*N   since o + V > 0   where i >= 1
   *   p2 - p1 = (m+i)*N - (m*N + o + V) = i*N - (o + V)
   *   p2 = p1 + i*N - (o + V) = (k+1)*V + i*N - (o + V) = k*V + i*N - o
   *
   *         p0                  p1          p2
   *   mN    mN+o                            (m+i)*N
   *         kv                  (k+1)v
   *   |<=o=>|<========v========>|<=i*N-o-V=>|
   *   |<===============i*N=================>| 
   *   
   */

  // Retrieve the previous 8-byte aligned address
  // should be the same for 8/16/32-byte alignement
  size_t ptr_8_byte_aligned = ((size_t)aligned_ptr) & (~(POINTER_SIZE - 1));
  // and move backward to get the original address
  void **original_pointer_store = ((void **)ptr_8_byte_aligned) - 1;

  return original_pointer_store;
}

//! Malloc on N-byte boundary
/**
 *  \param aligned pointer
 *  \param number of bytes
 *  \param size in byte
 *
 */
int
aligned_malloc(void **ptr, size_t number_of_bytes, size_t size)
{
  if (not_a_power_of_two(number_of_bytes))
    {
      // errno = EINVAL;
      return EINVAL;
    }

  // malloc ensures 8-byte alignement
  if (number_of_bytes < POINTER_SIZE)
    number_of_bytes = POINTER_SIZE;

  // The alignement padding is <= number_of_bytes -1
  // and we allocate a pointer in addition to store the original pointer.
  size_t allocated_size = size + number_of_bytes + POINTER_SIZE;
  void *unaligned_ptr = malloc(allocated_size);
  if (!unaligned_ptr)
      return ENOMEM;

  // shift unaligned pointer for the original pointer store
  void *shifted_unaligned_ptr = (void *)((size_t)unaligned_ptr + POINTER_SIZE);
  void *aligned_ptr = get_aligned_pointer(number_of_bytes, shifted_unaligned_ptr);
  // store the original pointer in front of the data
  void **original_pointer_store = get_original_pointer_store(aligned_ptr);
  *original_pointer_store = unaligned_ptr;

  #ifdef DEBUG
  printf("aligned_malloc:\n");
  printf("  alignement           %llu bytes\n", number_of_bytes);
  printf("  size                 %llu bytes\n", size);
  printf("  allocated size       %llu bytes\n", allocated_size);
  printf("  unaligned ptr        %llu\n", unaligned_ptr);
  printf("  aligned ptr          %llu\n", aligned_ptr);
  printf("  offset               %llu bytes\n", (size_t)aligned_ptr - (size_t)unaligned_ptr);
  printf("  original ptr store   %llu\n", original_pointer_store);
  for (size_t i = 0; i < 8; i++)
    printf("  [%llu][%2llu] %llu\n", unaligned_ptr + i * POINTER_SIZE, i * POINTER_SIZE, ((size_t *)unaligned_ptr)[i]);
  #endif

  *ptr = aligned_ptr; 

  return EXIT_SUCCESS;
}

//! Free Aligned Memory
/**
 *  \param aligned pointer
 *
 */
void
aligned_free(void *aligned_ptr)
{
  if (aligned_ptr)
    free(*get_original_pointer_store(aligned_ptr));
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
