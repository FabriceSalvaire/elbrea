#ifndef __IMAGEPROFILE_H__
#define __IMAGEPROFILE_H__

/**************************************************************************************************/

#include <stdint.h>
#include <stdlib.h>
#include <exception>
#include <string>

using namespace std;

/* *********************************************************************************************** */

#include "Image.hpp"
#include "ImageGeometry.hpp"

/* *********************************************************************************************** */

class ImageProfileException : public exception
{
public:
  ImageProfileException(const char *error_message) throw() : m_error_message(error_message) {}
  ~ImageProfileException () throw () {}
  
  virtual const char * what() const throw()
  {
    return m_error_message.data();
  }
  
private:
  string m_error_message;
};

/* *********************************************************************************************** */

struct LineProfilePoint
{
  PositionType r;
  PositionType c;
  OffsetType r_min; // could be negative
  OffsetType r_max;
  PositionType step;
};

class LineProfile
{
public:
  LineProfile();
  LineProfile(size_t number_of_points, size_t radius);
  ~LineProfile();

  size_t number_of_points() const { return m_size; };

  void set(size_t i, PositionType r, PositionType c, bool step);
  // inline const LineProfilePoint & get(size_t i) { return m_points[i]; };
  inline const LineProfilePoint * get(size_t i) const { return &(m_points[i]); };
  inline const LineProfilePoint & operator[](size_t i) { return m_points[i]; };
  // inline const LineProfilePoint * operator[](size_t i) const { return &(m_points[i]); };

  // const Image profile_image() const;

private:
  size_t m_radius;
  size_t m_size;
  LineProfilePoint *m_points;
};

/* *********************************************************************************************** */

struct RowSlice
{
  PositionType r;
  PositionType c_start;
  PositionType c_stop;
};

class RowSlices
{
public:
  RowSlices();
  RowSlices(size_t number_of_slices);
  ~RowSlices();

  size_t number_of_slices() const { return m_size; };

  inline RowSlice & operator[](size_t i) { return m_data[i]; };

private:
  size_t m_size;
  RowSlice *m_data;
};

/* *********************************************************************************************** */

class ImageProfile
{
public:
  ImageProfile(const ImageSize & image_size, const Point2D & location1, const Point2D & location2, size_t radius);
  ~ImageProfile();

  void compute_profile_standard(const Image & image);
  void prepare_profile_computation() throw(ImageProfileException);
  void compute_profile(const Image & image);

  const LineProfile & line_profile() const { return m_line_profile; };
  const RowSlices & row_slices() const { return m_row_slices; };

  const Image * profile_image();

private:
  void reset();
  void check_image_size(const Image & image) throw(ImageProfileException);
  void bresenham();
  void row_slices_for_null_slope();
  void row_slices_for_negative_slope();
  void row_slices_for_positive_slope();
  void allocate_data();

private:
  const Point2D & m_location1;
  const Point2D & m_location2;
  Offset2D m_delta;
  ImageSize m_image_size;
  size_t m_radius;
  LineProfile m_line_profile;
  RowSlices m_row_slices;
  Image::PixelType * m_data;
  Image::PixelType * m_means;
  Image::PixelType * m_sigmas;
  Image * m_profile_image;
};

/* *********************************************************************************************** */

#endif /* __IMAGEPROFILE_H__ */

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
