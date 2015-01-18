/* *********************************************************************************************** */

#include "DataType.hpp"

/* *********************************************************************************************** */

//! convert a precision in number of bits to a number of bytes
/**
 *  \param precision in number of bits
 *
 */
size_t precision_to_number_of_bytes(size_t precision)
{
  // shift the number of bits to the next byte chunk and perform an integer division
  // Why "& 255" ?
  return ((precision & 0XFF) + 7) / 8;
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
