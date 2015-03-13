/* *********************************************************************************************** */

// #shader_type geometry

#version 330
#extension GL_EXT_geometry_shader4 : enable

/* *********************************************************************************************** */

#include(../include/model_view_projection_matrix.glsl)

/* *********************************************************************************************** */

uniform float line_width = 5.;
uniform float antialias_diameter = 1.;

/* *********************************************************************************************** */

layout(lines) in;
layout(triangle_strip, max_vertices=4) out;

/* *********************************************************************************************** */

in VertexAttributesIn
{
  vec2 position;
  vec4 colour;
} vertexIn[];

/* *********************************************************************************************** */

out VertexAttributes
{
  vec2 uv;
  float line_width;
  float line_length;
  vec4 colour;
  float cap;
} vertex;

/* *********************************************************************************************** */

void
emit_vertex(in vec2 position, in vec2 uv, in float cap)
{
  vertex.cap = cap;
  vertex.uv = uv;
  gl_Position =  model_view_projection_matrix * vec4(position, 0, 1);
  EmitVertex();
}

/* *********************************************************************************************** */

void main()
{
  vertex.colour = vertexIn[0].colour;

  // If color is fully transparent we just will discard the fragment later
  /* if (vertex.colour.a <= .0) */
  /*   return; */
  
  vec2 pos1 = vertexIn[0].position;
  vec2 pos2 = vertexIn[1].position;

  float line_length = length(pos2 - pos1);
  vertex.line_length = line_length;
  
  // Thickness below 1 pixel are represented using a 1 pixel thickness
  // and a modified alpha
  float line_width = line_width;
  vertex.colour.a = min(line_width, vertex.colour.a);
  vertex.line_width = max(line_width, 1.);

  // This is the actual half width of the line
  float w = ceil(1.25*antialias_diameter + line_width) / 2.;

  vec2 dir1 = normalize(pos2 - pos1);
  vec2 normal1 = vec2(-dir1.y, dir1.x);
  vec2 tangential_offset1 = dir1 * w;
  vec2 normal_offset1 = normal1 * w;

  float cap1 = -1.;
  pos1 -= tangential_offset1;

  emit_vertex(pos1 - normal_offset1, vec2(-w, -w), cap1);
  emit_vertex(pos1 + normal_offset1, vec2(-w, w), cap1);

  float cap2 = 1.;
  pos2 += tangential_offset1;
  float u = line_length + w;

  emit_vertex(pos2 - normal_offset1, vec2(u, -w), cap2);
  emit_vertex(pos2 + normal_offset1, vec2(u, w), cap2);
  
  EndPrimitive();
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
