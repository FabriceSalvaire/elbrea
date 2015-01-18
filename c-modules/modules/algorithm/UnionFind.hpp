/* *********************************************************************************************** */

#ifndef __UnionFind_H__
#define __UnionFind_H__

/* *********************************************************************************************** */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <stdint.h>

/* *********************************************************************************************** */

class UnionFind
{
public:
  UnionFind(size_t size);
  ~UnionFind();

  void make_union(int x, int y);
  int generate_final_label();
  int find(int x);
  
private:
  size_t size;
  int *parent;
  int *final_label;
};

/* *********************************************************************************************** */

#endif /* __UnionFind_H__ */

/* *********************************************************************************************** */
