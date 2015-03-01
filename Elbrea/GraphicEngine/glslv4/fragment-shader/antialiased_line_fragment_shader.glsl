/* *********************************************************************************************** */

// #shader_type fragment

#version 330

/* *********************************************************************************************** */

uniform int cap_type = 1;
uniform int line_join = 1;
uniform float antialias_diameter = 1.;

/* *********************************************************************************************** */

in VertexAttributes
{
  vec2 uv;
  float line_length;
  float line_width;
  vec4 colour;
} vertex;

/* *********************************************************************************************** */

out vec4 fragment_colour;

/* *********************************************************************************************** */

// Compute distance to cap 
float
cap(int type, float dx, float dy, float t)
{
  return sqrt(dx*dx + dy*dy);
}

// Compute distance to join
float
join(in vec2 uv, in float line_stop, in float line_width, inout vec4 colour)
{
  float dx = uv.x;
  float d = abs(uv.y);
  
  if (dx < .0) {
    d = max(d, length(uv));
    colour = vec4(1, 0, 0, .5);
  }
  else if (dx > line_stop) {
    d = max(d, length(uv - vec2(line_stop, .0)));
    colour = vec4(0, 1, 0, .5);
  }
  else {
    colour = vec4(1, 1, 1, .5);
  }
  
  return d;
}

/* *********************************************************************************************** */

void main()
{
  // If colour is fully transparent we just discard the fragment
  if (vertex.colour.a <= 0.0)
    discard;

  float u = vertex.uv.x;
  float v = vertex.uv.y;
  float t = vertex.line_width/2. - antialias_diameter;

  float dy = abs(v);
  
  float line_start = .0;
  float line_stop = vertex.line_length;
  
  float d = .0;
  // start cap
  /* if (u < line_start) */
  /*   d = cap(cap_type, abs(u), dy, t); */
  /* // stop cap */
  /* else if (u > line_stop) */
  /*   d = cap(cap_type, abs(u) - line_stop, dy, t); */
  /* else */
  /* d = dy; */
  vec4 colour = vertex.colour;
  d = join(vertex.uv, line_stop, vertex.line_width, colour);
  
  // Anti-alias test, distance to border
  d -= t;
  if (d < .0)
    fragment_colour = colour;
  else
    {
      d /= antialias_diameter;
      fragment_colour = vec4(colour.xyz, exp(-d*d) * colour.a);
      /* fragment_colour = vec4(0, 0, 1, 1); */
    }
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
