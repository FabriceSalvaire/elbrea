/* *********************************************************************************************** */

#ifndef __Island_H__
#define __Island_H__

/* *********************************************************************************************** */

#include <stdint.h>

#include <string>
#include <vector>

using namespace std;

/* *********************************************************************************************** */

const size_t NUMBER_OF_PIXELS_MINIMUM = 2;

/* *********************************************************************************************** */

typedef struct
{
  // uint16 = 65536, for a 2000-pixel camera => 32 columns
  // This structure is 64-bit wide.
  uint16_t r;
  uint16_t c;
  uint16_t value;
  uint16_t padding;
} Pixel;

class Island
{
public:
  Island();
  Island(int wave, int label, Pixel *pixels, size_t number_of_pixels);

  void set_pixels(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns);

  void analyse(size_t number_of_pixels_minimum = NUMBER_OF_PIXELS_MINIMUM);
  string print_object();
  void paint(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns, uint16_t intensity);

  void set_pixel_image(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns);

private:

  void analyse_inertia_matrix(float &Ir, float &Ic, float &Irc,
			      float &vx, float &v1y, float &v2y,
			      float &lambda1, float &lambda2,
			      float &major_axis_angle,
			      float &major_axis, float &minor_axis,
			      float &axis_ratio);

public:
  int wave;
  int label;
  bool selected;
  bool excluded;

  bool analyse_more_done;

  Pixel *pixels; // extern pointer
  size_t number_of_pixels;

  size_t r_min, r_max, c_min, c_max;
  size_t number_of_rows, number_of_columns;

  unsigned long int intensity_integral;

  unsigned long int intensity_min;
  unsigned long int intensity_max;

  float cm_r_unweighted, cm_c_unweighted;
  float Ir_unweighted, Ic_unweighted, Irc_unweighted;
  float vx_unweighted, v1y_unweighted, v2y_unweighted;
  float lambda1_unweighted, lambda2_unweighted;
  float major_axis_angle_unweighted;
  float major_axis_unweighted, minor_axis_unweighted;
  float axis_ratio_unweighted;

  float cm_r_weighted, cm_c_weighted;
  float Ir_weighted, Ic_weighted, Irc_weighted;
  float vx_weighted, v1y_weighted, v2y_weighted;
  float lambda1_weighted, lambda2_weighted;
  float major_axis_angle_weighted;
  float major_axis_weighted, minor_axis_weighted;
  float axis_ratio_weighted;
};

class IslandOwned : public Island
{
public:
  IslandOwned(int wave, int label, size_t number_of_pixels);
  ~IslandOwned();

  void set_pixel(size_t i, uint16_t r, uint16_t c, uint16_t value);
};

/* *********************************************************************************************** */

#endif /* __Island_H__ */

/* *********************************************************************************************** */
