// start stop / lower upper

/* *********************************************************************************************** */

#include <iostream>
#include <cstring>

#include "Math.hpp"
#include "ImageProfile.hpp"

/* *********************************************************************************************** */

LineProfile::LineProfile()
  : m_radius(0), m_size(0), m_points(NULL)
{
}

LineProfile::LineProfile(size_t number_of_points, size_t radius)
  : m_radius(radius), m_size(number_of_points), m_points(NULL)
{
  m_points = new LineProfilePoint[m_size];
}

LineProfile::~LineProfile()
{
  /*
  if (m_points)
    delete[] m_points;
  */
}

void
LineProfile::set(size_t i, PositionType r, PositionType c, bool step)
{
  LineProfilePoint & point = m_points[i];
  point.r = r;
  point.c = c;
  point.r_min = static_cast<OffsetType>(r) - static_cast<OffsetType>(m_radius);
  point.r_max = static_cast<OffsetType>(r + m_radius);
  point.step = static_cast<PositionType>(step);
}

/*
const Image
LineProfile::profile_image() const
{
  return Image<uint64_t>(m_points, 2, number_of_points());
}
*/

/* *********************************************************************************************** */

RowSlices::RowSlices()
  : m_size(0), m_data(NULL)
{
}

RowSlices::RowSlices(size_t number_of_slices)
  : m_size(number_of_slices), m_data(NULL)
{
  m_data = new RowSlice[m_size];
}

RowSlices::~RowSlices()
{
  /*
  if (m_data)
    delete[] m_data;
  */
}

/* *********************************************************************************************** */

ImageProfile::ImageProfile(const ImageSize & image_size, const Point2D & location1, const Point2D & location2, size_t radius)
  : m_location1(location1), m_location2(location2), m_delta(), m_image_size(image_size), m_radius(radius),
    m_line_profile(), m_row_slices(), m_data(NULL), m_means(NULL), m_sigmas(NULL), m_profile_image(NULL)
{
  // Check ! not unsigned - if 1<->2
  m_delta = Offset2D(location2) - Offset2D(location1);
}

/* *********************************************************************************************** */

ImageProfile::~ImageProfile()
{
  reset();
}

/* *********************************************************************************************** */

void
ImageProfile::reset()
{
  if (m_data)
    delete[] m_data;

  if (m_profile_image)
    delete m_profile_image;
}

/* *********************************************************************************************** */

void
ImageProfile::allocate_data()
{
  reset();
  size_t number_of_points = m_line_profile.number_of_points();
  m_data = new Image::PixelType[number_of_points*2];
  m_means = m_data;
  m_sigmas = &(m_data[number_of_points]);
}

/* *********************************************************************************************** */

void
ImageProfile::check_image_size(const Image & image) throw(ImageProfileException)
{
  if (image.image_size() != m_image_size)
    throw ImageProfileException("Image size differ");
}

/* *********************************************************************************************** */

void
ImageProfile::compute_profile_standard(const Image & image)
{
  check_image_size(image);

  bresenham();
  allocate_data();

  size_t number_of_points = m_line_profile.number_of_points();
  for (size_t i = 0; i < number_of_points; i++)
    {
      const LineProfilePoint & point = m_line_profile[i];
      size_t c = point.c;

      OffsetType r_start = max(0L, point.r_min);
      OffsetType r_stop = min(m_image_size.height(), static_cast<size_t>(point.r_max) +1);
      float sum = .0;
      float square = .0;
      size_t count = .0;
      for (OffsetType r = r_start; r < r_stop; r++)
	{
	  Image::PixelConstPointerType row_ptr = image.row_pointer(r);
	  Image::PixelType value = row_ptr[c];
	  sum += value;
	  square += value * value;
	  count += 1;
	}

      float mean = sum / static_cast<float>(count);
      float sigma = sqrt(square/count - mean*mean);
      m_means[i] = mean;
      m_sigmas[i] = sigma;
    }
}

/* *********************************************************************************************** */

void
ImageProfile::prepare_profile_computation() throw(ImageProfileException)
{
  if (! (labs(m_delta.r()) <= labs(m_delta.c())))
    throw ImageProfileException("delta r > delta c");

  if (m_location1.r() == m_location2.r())
    row_slices_for_null_slope();
  else if (m_location1.r() < m_location2.r())
    row_slices_for_positive_slope();
  else
    row_slices_for_negative_slope();

  allocate_data();
}

/* *********************************************************************************************** */

void
ImageProfile::compute_profile(const Image & image)
{
  check_image_size(image);

  size_t number_of_points = m_line_profile.number_of_points();
  size_t array_size = 3*number_of_points;
  float *tmp_data = new float[array_size];
  float *sums = tmp_data;
  float *squares = &(tmp_data[number_of_points]);
  float *counts = &(tmp_data[2*number_of_points]);
  memset(tmp_data, 0, array_size*sizeof(float));

  for (size_t i = 0; i < m_row_slices.number_of_slices(); i++)
    {
      const RowSlice & slice = m_row_slices[i];
      // std::cout << "slice " << i << " " << slice.r << " " << slice.c_start<< " " << slice.c_stop << std::endl << flush;
      Image::PixelConstPointerType row_ptr = image.row_pointer(slice.r);
      PositionType c = slice.c_start;
      size_t j = c - m_location1.c();
      for (; c <= slice.c_stop; c++, j++)
	{
	  Image::PixelType value = row_ptr[c];
	  sums[j] += value;
	  squares[j] += value * value;
	  counts[j] += 1;
	}
    }

  for (size_t i = 0; i < number_of_points; i++)
    {
      float sum = sums[i];
      float square = squares[i];
      float count = counts[i];
      float mean = sum / count;
      m_means[i] = mean;
      m_sigmas[i] = sqrt(square/count - mean*mean);
    }

  delete tmp_data;
}

/* *********************************************************************************************** */

const Image *
ImageProfile::profile_image()
{
  if (! m_profile_image)
    m_profile_image = new Image(m_data, 2, m_line_profile.number_of_points());

  return m_profile_image;
}

/* *********************************************************************************************** *
 * 
 * Digital Line Drawing
 * by Paul Heckbert
 * from "Graphics Gems", Academic Press, 1990
 * 
 * digline: draw digital line from (x1,y1) to (x2,y2), calling a user-supplied procedure at each
 * pixel.  Does no clipping.  Uses Bresenham's algorithm.
 * 
 * Paul Heckbert   3 Sep 85
 *
 */

void
ImageProfile::bresenham()
{
  OffsetType dc = m_delta.c();
  OffsetType ac = labs(dc) << 1;
  OffsetType sc = copy_sign(dc);

  OffsetType dr = m_delta.r();
  OffsetType ar = labs(dr) << 1;
  OffsetType sr = copy_sign(dr);

  PositionType c = m_location1.c();
  PositionType r = m_location1.r();
  OffsetType d;  
  bool step;
  size_t i = 0; // Fixme: iterator on line_profile

  if (ac > ar)
    {
      // x dominant, will generate dc +1 points
      size_t number_of_points = labs(dc) +1;
      m_line_profile = LineProfile(number_of_points, m_radius);
      d = ar - (ac >> 1);
      while (1)
	{
	  step = d >= 0;
	  m_line_profile.set(i, r, c, step);
	  if (c == m_location2.c()) // return;
	    break;
	  if (step)
	    {
	      r += sr;
	      d -= ac;
	    }
	  c += sc;
	  d += ar;
	  i++;
	}
    }
  else
    {
      // y dominant, will generate dr +1 points
      size_t number_of_points = labs(dr) +1;
      m_line_profile = LineProfile(number_of_points, m_radius);
      d = ac - (ar >> 1);
      while (1)
	{
	  step = d >= 0;
	  m_line_profile.set(i, r, c, step);
	  if (r == m_location2.r()) // return;
	    break;
	  if (step)
	    {
	      c += sc;
	      d -= ar;
	    }
	  r += sr;
	  d += ac;
	  i++;
	}
    }
}

void
ImageProfile::row_slices_for_null_slope()
{
  // horizontal line

  // Fixme: only to set number_of_points
  OffsetType dc = m_delta.c();
  size_t number_of_points = labs(dc) +1;
  m_line_profile = LineProfile(number_of_points, m_radius);

  PositionType r = m_location1.r();
  PositionType r_start = max(0L, static_cast<OffsetType>(r) - static_cast<OffsetType>(m_radius));
  PositionType r_stop = min(m_image_size.height(), r + m_radius +1);

  size_t number_of_slices = r_stop - r_start;
  m_row_slices = RowSlices(number_of_slices);

  size_t i = 0;
  for (r = r_start; r < r_stop; r++)
    {
      RowSlice & slice = m_row_slices[i++];
      slice.r = r;
      slice.c_start = m_location1.c();
      slice.c_stop = m_location2.c();
    }
}

void
ImageProfile::row_slices_for_positive_slope()
{
  // r1 < r2
  bresenham();

  size_t i_start = 0;
  size_t i_stop = m_line_profile.number_of_points();

  const LineProfilePoint & start_point = m_line_profile[i_start];
  const LineProfilePoint & stop_point = m_line_profile[i_stop -1];

  OffsetType r_start = max(0L, start_point.r_min);
  OffsetType r_stop = min(m_image_size.height(), static_cast<size_t>(stop_point.r_max) +1);

  size_t number_of_slices = r_stop - r_start;
  m_row_slices = RowSlices(number_of_slices);

  size_t slice_index = 0;
  for (OffsetType r = r_start; r < r_stop; r++)
    {
      RowSlice & slice = m_row_slices[slice_index++];
      slice.r = r;

      const LineProfilePoint * point = m_line_profile.get(i_start);
      slice.c_start = point->c;

      size_t row_i_start = i_start;
      bool decrement = false;
      for (size_t i = row_i_start; i < i_stop; i++)
	{
	  if (i > row_i_start)
	    point = m_line_profile.get(i);
	  if (r < point->r_min) // should test only at step true
	    {
	      decrement = true;
	      break;
	    }
	  if (r == point->r_max) // should set i_start only at step
	    i_start = i + 1;
	}
      PositionType c_stop = point->c;
      if (decrement)
	c_stop -= 1;
      slice.c_stop = c_stop;
    }
}

void
ImageProfile::row_slices_for_negative_slope()
{
  // r1 > r2
  bresenham();

  size_t i_start = 0;
  size_t i_stop = m_line_profile.number_of_points();

  const LineProfilePoint & start_point = m_line_profile[i_start];
  const LineProfilePoint & stop_point = m_line_profile[i_stop -1];

  OffsetType r_start = max(0L, stop_point.r_min);
  OffsetType r_stop = min(m_image_size.height() -1, static_cast<size_t>(start_point.r_max));

  size_t number_of_slices = r_stop - r_start +1;
  m_row_slices = RowSlices(number_of_slices);

  size_t slice_index = number_of_slices -1;
  for (OffsetType r = r_stop; r >= r_start; r--)
    {
      RowSlice & slice = m_row_slices[slice_index--];
      slice.r = r;

      const LineProfilePoint * point = m_line_profile.get(i_start);
      slice.c_start = point->c;

      size_t row_i_start = i_start;
      bool decrement = false;
      for (size_t i = row_i_start; i < i_stop; i++)
	{
	  if (i > row_i_start)
	    point = m_line_profile.get(i);
	  if (point->r_max < r) // should test only at step true
	    {
	      decrement = true;
	      break;
	    }
	  if (r == point->r_min) // should set i_start only at step
	    i_start = i + 1;
	}
      PositionType c_stop = point->c;
      if (decrement)
	c_stop -= 1;
      slice.c_stop = c_stop;
    }
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
