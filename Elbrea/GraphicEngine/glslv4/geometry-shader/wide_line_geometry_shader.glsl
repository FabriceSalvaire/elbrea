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

layout(lines_adjacency) in;
layout(triangle_strip, max_vertices=4) out;
// layout(triangle_strip, max_vertices=6) out;

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
} vertex;

/* *********************************************************************************************** */

void emit_vertex(vec2 position, vec2 uv, vec4 colour)
{
  vertex.colour = colour;
  // vertex.colour = vec4(1);
  vertex.uv = uv;
  gl_Position =  model_view_projection_matrix * vec4(position, 0, 1);
  EmitVertex();
}

/* *********************************************************************************************** */

void main()
{
  // vertex.colour = vertexIn[0].colour;

  // If color is fully transparent we just will discard the fragment later
  /* if (vertex.colour.a <= .0) */
  /*   return; */
  
  vec2 pos0 = vertexIn[0].position;
  vec2 pos1 = vertexIn[1].position;
  vec2 pos2 = vertexIn[2].position;
  vec2 pos3 = vertexIn[3].position;

  float line_length = length(pos2 - pos1);
  vertex.line_length = line_length;
  
  // Thickness below 1 pixel are represented using a 1 pixel thickness
  // and a modified alpha
  vertex.colour.a = min(line_width, vertex.colour.a);
  vertex.line_width = max(line_width, 1.);

  // This is the actual half width of the line
  float w = ceil(1.25*antialias_diameter + line_width) / 2.;

  vec2 dir0 = normalize(pos1 - pos0);
  vec2 normal0 = vec2(-dir0.y, dir0.x);
  vec2 tangential_offset0 = dir0 * w;
  vec2 normal_offset0 = normal0 * w;
  
  vec2 dir1 = normalize(pos2 - pos1);
  vec2 normal1 = vec2(-dir1.y, dir1.x);
  vec2 tangential_offset1 = dir1 * w;
  vec2 normal_offset1 = normal1 * w;

  vec2 dir2 = normalize(pos3 - pos2);
  vec2 normal2 = vec2(-dir2.y, dir2.x);
  vec2 tangential_offset2 = dir2 * w;
  vec2 normal_offset2 = normal2 * w;

  float angle1 = atan(dir0.x*dir1.y - dir0.y*dir1.x,
		      dir0.x*dir1.x + dir0.y*dir1.y);
  vec2 t1 = normalize(dir0 + dir1);
  vec2 n1 = vec2(-t1.y, t1.x);
  vec2 l1 = w / cos(angle1/2.) * n1;
  float m1 = w * tan(angle1/2.); // sign of angle
    
  float angle2 = atan(dir1.x*dir2.y - dir1.y*dir2.x,
		      dir1.x*dir2.x + dir1.y*dir2.y);
  vec2 t2 = normalize(dir1 + dir2);
  vec2 n2 = vec2(-t2.y, t2.x);
  vec2 l2 = w / cos(angle2/2.) * n2;
  float m2 = w * tan(angle2/2.);

  /* float u_max = vertex.line_length + w; */
  /* emit_vertex(pos1 - tangential_offset1 - normal_offset1, vec2(-w, -w)); */
  /* emit_vertex(pos1 - tangential_offset1 + normal_offset1, vec2(-w, w)); */
  /* emit_vertex(pos2 + tangential_offset1 - normal_offset1, vec2(u_max, -w)); */
  /* emit_vertex(pos2 + tangential_offset1 + normal_offset1, vec2(u_max, w)); */

  emit_vertex(pos1 - l1, vec2(-m1, -w), vec4(1, 0, 0, 1));
  emit_vertex(pos1 + l1, vec2(m1, w), vec4(1, 0, 0, 1));
  emit_vertex(pos2 - l2, vec2(line_length + m2, -w), vec4(0, 1, 0, 1));
  emit_vertex(pos2 + l2, vec2(line_length - m2,  w), vec4(0, 1, 0, 1));

  /* m1 = 0; */
  /* m2 = 0; */
  
  /* emit_vertex(pos1 - abs(m1) * dir1 - normal_offset1, vec2(-abs(m1), -w), vec4(1, 1, 0, 1)); */
  /* emit_vertex(pos1 - abs(m1) * dir1 + normal_offset1, vec2(-abs(m1), w), vec4(1, 1, 0, 1)); */
  /* emit_vertex(pos2 + abs(m2) * dir1 - normal_offset1, vec2(line_length + abs(m2), -w), vec4(1, 1, 0, 1)); */
  /* EndPrimitive(); */

  /* emit_vertex(pos1 - abs(m1) * dir1 + normal_offset1, vec2(-abs(m1), w), vec4(0, 1, 1, 1)); */
  /* emit_vertex(pos2 + abs(m2) * dir1 + normal_offset1, vec2(line_length + abs(m2),  w), vec4(0, 1, 1, 1)); */
  /* emit_vertex(pos2 + abs(m2) * dir1 - normal_offset1, vec2(line_length + abs(m2), -w), vec4(0, 1, 1, 1)); */
  
  EndPrimitive();
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
