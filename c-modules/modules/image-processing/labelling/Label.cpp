/* *********************************************************************************************** *
 *
 * Label Connected Components
 *
 * *********************************************************************************************** */

/* *********************************************************************************************** */

#include <climits>
#include <cstdlib>
#include <iostream>
#include <sstream>

#include "Island.hpp"
#include "Label.hpp"
#include "RandomPixelColour.hpp"
#include "UnionFind.hpp"

/* *********************************************************************************************** */

string IndexRange::str() const
{
  std::ostringstream message;
  message << "[" << start_index << ", " << stop_index << "]";

  return message.str();
}

string Segment::str() const
{
  std::ostringstream message;
  message << "l" << label << " r" << r << " [" << start_c << ", " << stop_c << "]";

  return message.str();
}

/* *********************************************************************************************** */

// Fixme: pass image
//  labeler.run_length_encode(self.mask_image.buffer)
//  labeler.merge_segments()
//  labeler.generate_islands(self.data_image.buffer)
Label::Label(size_t wave, size_t number_of_rows, size_t number_of_columns)
  : islands(),
    wave(wave),
    number_of_rows(number_of_rows),
    number_of_columns(number_of_columns),
    number_of_labels(0),
    number_of_pixels(0),
    row_map(number_of_rows), // Init number_of_rows empty IndexRange
    segments(),
    number_of_pixels_per_label(),
    pixels(NULL)
{
}

/* *********************************************************************************************** */

Label::~Label()
{
  // std::cout << "~Label " << wave << std::endl;
  if (pixels != NULL)
    delete[] pixels;
}

/* *********************************************************************************************** */

//! Run Length Encode the Mask Image
/*
 * This algorithm do a forward scan of the image rows,
 *  - track and append the contiguous pixel-on segments,
 *  - fill the row_map structure for each row with the segment index range.
 *
 * The label of the segments is incremented from 1, the label 0
 * corresponds to the pixel off sea.
 */
void
Label::run_length_encode(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns)
{
  size_t last_c = number_of_columns -1;
  size_t pixel_index = 0;
  size_t start_segment_index = 0;
  int label = 1;
  for (size_t r = 0; r < number_of_rows; r++)
    {
      int start_c = -1; // -1 means undefined
      size_t stop_c;
      size_t number_of_segments = 0;

      for (size_t c = 0; c < number_of_columns; c++)
        {
	  // State Machine
          bool append = false;
	  // pixel on?
          if (buffer[pixel_index] != 0)
  	  {
  	    stop_c = c; // save curent c
	    // if new segment then save start c
	    if (start_c == -1)
	      start_c = c;
	    // if last c then append segment
  	    if (c == last_c)
	      append = true;
  	  }
	  // if pixel off and segment defined then append segment
          else if (start_c != -1)
	    append = true;

	  // Append segment if necessary
          if (append)
  	  {   
	    segments.push_back(Segment(r, start_c, stop_c, label));
	    number_of_segments++;
	    label++;
	    start_c = -1; // reset start_c
  	  }

	  pixel_index++;
        } // End column loop
 
      // Append Segment Index Range for the row if necessary
      if (number_of_segments > 0)
	{
	  int stop_segment_index = start_segment_index + number_of_segments -1;
	  IndexRange &index_range = row_map[r];
	  index_range.start_index = start_segment_index;
	  index_range.stop_index = stop_segment_index;
	  start_segment_index = stop_segment_index +1;
	}
    } // End row loop
}

/* *********************************************************************************************** */

//! Merge Connex Segments
/*
 * This algorithm merge the 8-connex segments and compute the final labels.
 * 
 */
void
Label::merge_segments()
{
  // Init a Disjoint-Set with( number_of_segments + sea) labels
  UnionFind union_find = UnionFind(segments.size() +1);

  // First Pass: merge connex segments
  //  - iterate over the couple of consecutive rows
  for (size_t r = 0; r < (number_of_rows -1); r++)
    {
      const IndexRange &row_map0 = row_map[r];
      const IndexRange &row_map1 = row_map[r +1];

      // Continue with next row if a row is empty
      if (row_map0.start_index == -1 || row_map1.start_index == -1)
	continue;

      // iterate over the segments of the row0
      int index1 = row_map1.start_index;
      for (int index0 = row_map0.start_index; index0 <= row_map0.stop_index; index0++)
	{
	  // Fixme: & -> bug ?
	  Segment segment0 = segments[index0];
	  Segment segment1 = segments[index1];
	  // std::cout << "  r" << r << "-" << r+1 << " | " << segment0.str() << " | " << segment1.str() << std::endl;

	  // Skip segment1 before segment0
	  //   we use an 8-connectivity
	  //     row 0           ?###
	  //     row 1 #s# #s# #!#? 
	  while ((segment0.start_c - segment1.stop_c) > 1)
	    {
	      // segment1 iterator
	      index1 += 1;
	      if (index1 > row_map1.stop_index)
		{
		  // std::cout << "    goto next row" << std::endl;
		  goto next_row;
		}
	      else
		{
		  segment1 = segments[index1];
		  // std::cout << "    skip & -> " << segment1.str() << std::endl;
		}
	    }
     
     	  // Merge until segments of 1 is connex with segment0
	  //     row 0  ###########?
	  //     row 1   #m# #m#  ?#m# ###
     	  while ((int)segment1.start_c - (int)segment0.stop_c <= 1)
     	    {
	      // std::cout << "    merge / " << segment1.str() << std::endl;
     	      union_find.make_union(segment0.label, segment1.label);
     	      
	      // same pattern for segment1 iterator
     	      index1 += 1;
     	      if (index1 > row_map1.stop_index)
		  break;
	      else
		{
		  segment1 = segments[index1];
		  // std::cout << "    -> " << segment1.str() << std::endl;
		}
     	    }

     	  // Start next loop iteration with precedent segment1 if not the first
	  //     row 0  #########   ######
	  //     row 1   ### ### #!# ###
     	  if (index1 != row_map1.start_index)
	    index1 -= 1;

	  continue;
	next_row:
	  break;
	} // End segments0 loop
    } // End row loop

  // Second Pass:
  //  - set the final label of the segments
  //  - count the pixels
  number_of_labels = union_find.generate_final_label();
  number_of_pixels = 0;
  number_of_pixels_per_label = vector<size_t>(number_of_labels);
  for (vector<Segment>::iterator s = segments.begin(); s != segments.end(); ++s)
    {
      Segment &segment = *s;
      int final_label = union_find.find(segment.label);
      segment.label = final_label;
      size_t number_of_pixels_of_segment = segment.size();
      number_of_pixels_per_label[final_label] += number_of_pixels_of_segment;
      number_of_pixels += number_of_pixels_of_segment;
    }
  
  // std::cout << "Number of labels: " << number_of_labels << std::endl;
  // std::cout << "Number of pixels: " << number_of_pixels << std::endl;
}

/* *********************************************************************************************** */

//! Generate the islands
/*!
 * Generate the islands using the raw image.
 *
 */
void
Label::generate_islands(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns)
{
  // Allocate the island and pixel vectors
  //  This strategy should allocate only one large memory block at once
  islands = vector<Island>(number_of_labels);
  pixels = new Pixel[number_of_pixels];

  // Store the current pixel index for each islands
  size_t island_indexes[number_of_labels];

  // Init the islands
  size_t current_index = 0;
  for (size_t label = 1; label < number_of_labels; label++)
    {
      size_t number_of_pixels_of_label = number_of_pixels_per_label[label];

      Island &island = islands[label];
      island.label = label;
      island.wave = wave;
      island.pixels = &(pixels[current_index]);
      island.number_of_pixels = number_of_pixels_of_label;
    
      island_indexes[label] = current_index;
      current_index += number_of_pixels_of_label;
    }

  // Init the pixel array from the segments
  for (vector<Segment>::const_iterator s = segments.begin(); s != segments.end(); ++s)
    {
      const Segment &segment = *s;
      size_t r = segment.r;
      size_t pixel_index_base = r * number_of_columns;
      size_t island_index = island_indexes[segment.label];

      for (size_t c = segment.start_c; c <= segment.stop_c; ++c)
	{
	  size_t buffer_index = pixel_index_base + c;
	  uint16_t value = buffer[buffer_index];

	  Pixel &pixel = pixels[island_index];
	  pixel.r = static_cast<uint16_t>(r);
	  pixel.c = static_cast<uint16_t>(c);
	  pixel.value = value;
	  	  
	  island_index++;
	}
      
      island_indexes[segment.label] = island_index;
    }
}

/* *********************************************************************************************** */

//! Make a gray image set with the labels
void
Label::make_label_image(uint16_t *buffer, size_t number_of_rows, size_t number_of_columns)
{
  for (vector<Segment>::const_iterator s = segments.begin(); s != segments.end(); ++s)
    {
      const Segment &segment = *s;
      for (size_t c = segment.start_c; c <= segment.stop_c; ++c)
	{
	  size_t buffer_index = segment.r * number_of_columns + c;
	  buffer[buffer_index] = segment.label;
	}
    }
}

/* *********************************************************************************************** */

//! Make a colour image set with the random label colours.
void
Label::make_colour_image(uint8_t *buffer, size_t number_of_rows, size_t number_of_columns, size_t number_of_channels)
{
  vector<RGBAColour> label_colours(number_of_labels);
  for (vector<RGBAColour>::iterator s = label_colours.begin(); s != label_colours.end(); ++s)
    {
      RGBAColour &rgba_colour = *s;
      rgba_colour.set_random_colour();
    }

  for (vector<Segment>::const_iterator s = segments.begin(); s != segments.end(); ++s)
    {
      const Segment &segment = *s;
      for (size_t c = segment.start_c; c <= segment.stop_c; ++c)
	{
	  size_t buffer_index = number_of_channels * (segment.r * number_of_columns + c);
	  const RGBAColour &rgba_colour = label_colours[segment.label];
	  buffer[buffer_index +0] = rgba_colour.red;
	  buffer[buffer_index +1] = rgba_colour.green;
	  buffer[buffer_index +2] = rgba_colour.blue;
	}
    }
}

/* *********************************************************************************************** */

void
Label::print_row_map()
{
  std::cout << "Row Map:" << std::endl;
  for (size_t r = 0; r < number_of_rows; ++r)
    std::cout << "  r" << r << " " << row_map[r].str() << std::endl;
}

/* *********************************************************************************************** */

void
Label::print_segments()
{
  std::cout << "Segments:" << std::endl;
  size_t i = 0;
  for (vector<Segment>::const_iterator s = segments.begin(); s != segments.end(); ++s)
    {
      const Segment &segment = *s;
      std::cout << "  s" << i << " " << segment.str() << std::endl;
      i++;
    }
}

/* *********************************************************************************************** */

void
Label::print_run_length_encoding()
{
  print_row_map();
  print_segments();
}

/* *********************************************************************************************** */

//! Analyse the islands
void
Label::analyse_islands()
{
  for (vector<Island>::iterator i = islands.begin(); i != islands.end(); ++i)
    {
      Island &island = *i;
      island.analyse();
    }
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
