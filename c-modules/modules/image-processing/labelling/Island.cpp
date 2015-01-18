/* *********************************************************************************************** */

#include <climits>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <string>
#include <sstream>

#include "Island.hpp"
#include "Math.hpp"
#include "Geometry.hpp"

/* *********************************************************************************************** */

size_t
round_zero_trunc(double x)
{
  if (x < .0)
    return 0;
  else
    return static_cast<size_t>(floor(x));
}

/* *********************************************************************************************** */

// Zero all ctor

Island::Island()
  : wave(-1),
    label(-1),
    selected(false),
    excluded(false),

    analyse_more_done(false),

    pixels(NULL),
    number_of_pixels(0),

    r_min(0), r_max(0), c_min(0), c_max(0),
    number_of_rows(0), number_of_columns(0),

    intensity_integral(0),

    intensity_min(0),
    intensity_max(0),

    cm_r_unweighted(.0), cm_c_unweighted(.0),
    Ir_unweighted(.0), Ic_unweighted(.0), Irc_unweighted(.0),
    vx_unweighted(.0), v1y_unweighted(.0), v2y_unweighted(.0),
    lambda1_unweighted(.0), lambda2_unweighted(.0),
    major_axis_angle_unweighted(.0),
    major_axis_unweighted(.0), minor_axis_unweighted(.0),
    axis_ratio_unweighted(.0),

    cm_r_weighted(.0), cm_c_weighted(.0),
    Ir_weighted(.0), Ic_weighted(.0), Irc_weighted(.0),
    vx_weighted(.0), v1y_weighted(.0), v2y_weighted(.0),
    lambda1_weighted(.0), lambda2_weighted(.0),
    major_axis_angle_weighted(.0),
    major_axis_weighted(.0), minor_axis_weighted(.0),
    axis_ratio_weighted(.0)
{}

Island::Island(int wave, int label, Pixel *pixels, size_t number_of_pixels)
  : wave(wave),
    label(label),
    selected(false),
    excluded(false),
      
    analyse_more_done(false),

    pixels(pixels),
    number_of_pixels(number_of_pixels),

    r_min(0), r_max(0), c_min(0), c_max(0),
    number_of_rows(0), number_of_columns(0),

    intensity_integral(0),

    intensity_min(0),
    intensity_max(0),

    cm_r_unweighted(.0), cm_c_unweighted(.0),
    Ir_unweighted(.0), Ic_unweighted(.0), Irc_unweighted(.0),
    vx_unweighted(.0), v1y_unweighted(.0), v2y_unweighted(.0),
    lambda1_unweighted(.0), lambda2_unweighted(.0),
    major_axis_angle_unweighted(.0),
    major_axis_unweighted(.0), minor_axis_unweighted(.0),
    axis_ratio_unweighted(.0),

    cm_r_weighted(.0), cm_c_weighted(.0),
    Ir_weighted(.0), Ic_weighted(.0), Irc_weighted(.0),
    vx_weighted(.0), v1y_weighted(.0), v2y_weighted(.0),
    lambda1_weighted(.0), lambda2_weighted(.0),
    major_axis_angle_weighted(.0),
    major_axis_weighted(.0), minor_axis_weighted(.0),
    axis_ratio_weighted(.0)
{}

// Fixme: init function and overload
void
Island::set_pixels(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns)
{
  // pixels = static_cast<Pixel *>(buffer);
  pixels = (Pixel *)(buffer);
  number_of_pixels = number_of_rows;
}

void
Island::analyse(size_t number_of_pixels_minimum)
{
  if (number_of_pixels < number_of_pixels_minimum)
    return;

  r_min = c_min = UINT_MAX;
  r_max = c_max = 0;

  unsigned int sum_r_unweighted = 0;
  unsigned int sum_c_unweighted = 0;

  unsigned long int sum_r_weighted = 0;
  unsigned long int sum_c_weighted = 0;

  intensity_integral = 0;

  intensity_min = UINT_MAX;
  intensity_max = 0;

  for (size_t i = 0; i < number_of_pixels; i++)
    {
      Pixel &pixel = pixels[i];
      unsigned int r = pixel.r;
      unsigned int c = pixel.c;
      unsigned int v = pixel.value;

      // Bounding box finder

      if (r < r_min) r_min = r;
      if (r_max < r) r_max = r;
      if (c < c_min) c_min = c;
      if (c_max < c) c_max = c;

      // Intensity range

      if (v < intensity_min) intensity_min = v;
      if (intensity_max < v) intensity_max = v;

      // Inertia

      intensity_integral += v;

      sum_r_unweighted += r;
      sum_c_unweighted += c;

      sum_r_weighted += v * r;
      sum_c_weighted += v * c;
    }

  // Inertia

  cm_r_unweighted = (float)sum_r_unweighted/(float)number_of_pixels;
  cm_c_unweighted = (float)sum_c_unweighted/(float)number_of_pixels;

  cm_r_weighted = (float)sum_r_weighted/(float)intensity_integral;
  cm_c_weighted = (float)sum_c_weighted/(float)intensity_integral;

  // Columns statitic

  number_of_rows    = r_max - r_min +1;
  number_of_columns = c_max - c_min +1;

  // Inertia

  Ir_unweighted  = .0;
  Ic_unweighted  = .0;
  Irc_unweighted = .0;

  Ir_weighted  = .0;
  Ic_weighted  = .0;
  Irc_weighted = .0;

  for (size_t i = 0; i < number_of_pixels; i++)
    {
      Pixel &pixel = pixels[i];
      unsigned int r = pixel.r;
      unsigned int c = pixel.c;
      unsigned int v = pixel.value;

      // Inertia

      float rp_unweighted = (float)r - cm_r_unweighted;
      float cp_unweighted = (float)c - cm_c_unweighted;
            
      Ir_unweighted  += cp_unweighted*cp_unweighted;
      Ic_unweighted  += rp_unweighted*rp_unweighted;
      Irc_unweighted -= rp_unweighted*cp_unweighted;

      float rp_weighted = (float)r - cm_r_weighted;
      float cp_weighted = (float)c - cm_c_weighted;
            
      Ir_weighted  += (float)v * cp_weighted*cp_weighted;
      Ic_weighted  += (float)v * rp_weighted*rp_weighted;
      Irc_weighted -= (float)v * rp_weighted*cp_weighted; // Fixme: keep computation v * cp
    }

  // Inertia

  Ir_unweighted  /= number_of_pixels;
  Ic_unweighted  /= number_of_pixels;
  Irc_unweighted /= number_of_pixels;

  analyse_inertia_matrix(Ir_unweighted, Ic_unweighted, Irc_unweighted,
			 vx_unweighted, v1y_unweighted, v2y_unweighted,
			 lambda1_unweighted, lambda2_unweighted,
			 major_axis_angle_unweighted,
			 major_axis_unweighted, minor_axis_unweighted,
			 axis_ratio_unweighted);

  Ir_weighted  /= intensity_integral;
  Ic_weighted  /= intensity_integral;
  Irc_weighted /= intensity_integral;

  analyse_inertia_matrix(Ir_weighted, Ic_weighted, Irc_weighted,
			 vx_weighted, v1y_weighted, v2y_weighted,
			 lambda1_weighted, lambda2_weighted,
			 major_axis_angle_weighted,
			 major_axis_weighted, minor_axis_weighted,
			 axis_ratio_weighted);
}

void
Island::analyse_inertia_matrix(float &Ir, float &Ic, float &Irc,
			       float &vx, float &v1y, float &v2y,
			       float &lambda1, float &lambda2,
			       float &major_axis_angle,
			       float &major_axis, float &minor_axis,
			       float &axis_ratio)
{
  if (Irc == .0)
    {
      if (Ir >= Ic)
        {
          major_axis_angle = .0;

          lambda1 = Ir;
          lambda2 = Ic;

          vx  = .0;
          v1y = 1.;
          v2y = .0;
        }
      else
        {
          major_axis_angle = 90.;

          lambda1 = Ic;
          lambda2 = Ir;

          vx  = 1.;
          v1y = .0;
          v2y = 1.;
        }
    }
  else
    {
      float Is = Ir + Ic;
      float Id = Ic - Ir;

      float sqrt0 = sqrt(Id*Id + 4*Irc*Irc);

      lambda1 = .5*(Is + sqrt0);
      lambda2 = .5*(Is - sqrt0);

      vx  = Irc;
      v1y = .5*(Id + sqrt0);
      v2y = .5*(Id - sqrt0);

      if (lambda1 < lambda2)
        {
          float t = v2y;
          v2y = v1y;
          v1y = t;

          t = lambda2;
          lambda2 = lambda1;
          lambda1 = t;
        }

      major_axis_angle = - rad2deg(atan(v1y/vx));
    }

  major_axis = 4.*sqrt(fabs(lambda1));
  minor_axis = 4.*sqrt(fabs(lambda2));

  if (minor_axis != .0)
    axis_ratio = major_axis/minor_axis;
  else
    axis_ratio = .0;
}

string
Island::print_object()
{
  ostringstream output;

  output
    << std::endl
    << "=================================================================================" << std::endl
    << "Island label " << label << std::endl
    << "  selected " << selected << std::endl
    << "  excluded " << excluded << std::endl
    << "  wave " << wave << std::endl
    << "  number of pixels " << number_of_pixels << std::endl
    << "  bbox " << r_min << "-" << r_max << " " << c_min << "-" << c_max << std::endl
    << "  intensity integral " << intensity_integral << std::endl
    << " Unweighted "  << std::endl
    << "  cm_r " << cm_r_unweighted
    << "  cm_c " << cm_c_unweighted << std::endl
    << "  Ir " << Ir_unweighted
    << "  Ic " << Ic_unweighted
    << "  Irc " << Irc_unweighted << std::endl
    << "  vx " << vx_unweighted
    << "  v1y " << v1y_unweighted
    << "  v2y " << v2y_unweighted << std::endl
    << "  lambda1 " << lambda1_unweighted
    << "  lambda2 " << lambda2_unweighted << std::endl
    << "  major_axis_angle " << major_axis_angle_unweighted << std::endl
    << "  major_axis " << major_axis_unweighted
    << "  minor_axis " << minor_axis_unweighted << std::endl
    << "  axis_ratio " << axis_ratio_unweighted << std::endl
    << " Weighted "  << std::endl
    << "  cm_r " << cm_r_weighted
    << "  cm_c " << cm_c_weighted << std::endl
    << "  Ir " << Ir_weighted
    << "  Ic " << Ic_weighted
    << "  Irc " << Irc_weighted << std::endl
    << "  vx " << vx_weighted
    << "  v1y " << v1y_weighted
    << "  v2y " << v2y_weighted << std::endl
    << "  lambda1 " << lambda1_weighted
    << "  lambda2 " << lambda2_weighted << std::endl
    << "  major_axis_angle " << major_axis_angle_weighted << std::endl
    << "  major_axis " << major_axis_weighted
    << "  minor_axis " << minor_axis_weighted << std::endl
    << "  axis_ratio " << axis_ratio_weighted
//  << std::endl
//  << "=================================================================================" << std::endl
    << std::endl;

  return output.str();
}

void
Island::paint(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns,
	      uint16_t intensity)
{
  for (size_t i = 0; i < number_of_pixels; i++)
    {
      Pixel &pixel = pixels[i];
      unsigned int r = pixel.r;
      unsigned int c = pixel.c;

      size_t buffer_index = r * number_of_columns + c;
	  
      buffer[buffer_index] = intensity;
    }
}

void
Island::set_pixel_image(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns)
{
  /*
   * Pixel Image:
   *
   *   R C V
   * 0
   * ...
   * N
   * 
   */

  for (size_t i = 0; i < number_of_pixels; i++)
    {
      Pixel &pixel = pixels[i];
      size_t location = 3*i;
      buffer[location] = pixel.r;
      buffer[location +1] = pixel.c;
      buffer[location +2] = pixel.value;
    }
}

/* *********************************************************************************************** */

IslandOwned::IslandOwned(int wave, int label, size_t number_of_pixels)
  : Island(wave, label, NULL, number_of_pixels)
{
  pixels = new Pixel[number_of_pixels];
}

IslandOwned::~IslandOwned()
{
  if (pixels != NULL)
    delete[] pixels;
}

void
IslandOwned::set_pixel(size_t i, uint16_t r, uint16_t c, uint16_t value)
{
  Pixel &pixel = pixels[i];
  pixel.r = r;
  pixel.c = c;
  pixel.value = value;
  pixel.padding = 0;
}

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
