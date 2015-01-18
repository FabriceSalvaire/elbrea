/* *********************************************************************************************** *
 *
 * Label Connected Components
 *
 * *********************************************************************************************** */

/* *********************************************************************************************** */

#ifndef __Label_H__
#define __Label_H__

/* *********************************************************************************************** */

#include <stdint.h>
#include <string>
#include <vector>

using namespace std;

/* *********************************************************************************************** */

/*
 * Number of pixels:
 * 
 *   round(math.log(2*1392*1040)/math.log(2)) = 22 bits
 *
 */

/* *********************************************************************************************** */

#include "Island.hpp"

/* *********************************************************************************************** */

//! Index Range to Access the Row Segments in the Segment Array.
/*!
 * This class defines the first and last segment index for a row in
 * the segment array.  An empty row as start_index and stop_index set
 * to -1.
 *
 * \param start_index Index of the first segment in the row 
 * \param stop_index  Index of the last segment in the row 
 */
class IndexRange
{
public:
  IndexRange()
    : start_index(-1), stop_index(-1)
  {};

  IndexRange(int start_index, int stop_index)
    : start_index(start_index), stop_index(stop_index)
  {};

  string str() const;

public:
  int start_index;
  int stop_index;
};

/* *********************************************************************************************** */

//! Image Horizontal Segment
/*!
 * This class defines an horizontal segment for an Run-Length-Encoded image.
 *
 * \param r Row index
 * \param start_c Column index of the first pixel of the segment
 * \param stop_c  Column index of the last pixel of the segment
 * \param label Label index
 */
class Segment
{
public:
  Segment(size_t r, size_t start_c, size_t stop_c, int label)
    : r(r), start_c(start_c), stop_c(stop_c), label(label)
  {};

  inline size_t size()
  {
    return static_cast<size_t>(stop_c - start_c +1);
  };

  string str() const;

public:
  size_t r;
  int start_c; // int type for a - b arithmetic
  int stop_c;
  int label; // Fixme: why int?
};

/* *********************************************************************************************** */

// Fixme:
// take as input mask and raw image
// return vector<Island> and Pixel *
class Label
{
public:
  Label(size_t wave, size_t number_of_rows, size_t number_of_columns);
  ~Label();

  void run_length_encode(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns);
  void merge_segments();
  void generate_islands(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns);
  void analyse_islands();
  void make_label_image(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns);
  void make_colour_image(uint8_t *buffer, size_t number_of_rows, size_t number_of_columns, size_t number_of_channels);
  void print_row_map();
  void print_segments();
  void print_run_length_encoding();

public:
  vector<Island> islands;

private:
  size_t wave;
  size_t number_of_rows;
  size_t number_of_columns;
  size_t number_of_labels;
  size_t number_of_pixels;

  vector<IndexRange> row_map;
  vector<Segment> segments;

  vector<size_t> number_of_pixels_per_label;
  Pixel *pixels;
};

/* *********************************************************************************************** */

#endif /* __Label_H__ */

/* *********************************************************************************************** */
