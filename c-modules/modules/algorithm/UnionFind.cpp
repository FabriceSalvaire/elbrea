/****************************************************************************************************
 *
 * Audit:
 *
 *   - optimize
 *
 ***************************************************************************************************/

/* *********************************************************************************************** */

#include <iostream>

/* *********************************************************************************************** */

#include "UnionFind.hpp"

/* *********************************************************************************************** */

UnionFind::UnionFind(size_t size)
  : size(size), parent(NULL), final_label(NULL)
{
  parent = new int[size];
  final_label = new int[size];

  for (size_t i = 0; i < size; ++i)
    {
      parent[i] = 0; 
      final_label[i] = 0;
    }
}

UnionFind::~UnionFind()
{
  // std::cout << "~UnionFind" << std::endl << std::flush;
  delete[] parent;
  delete[] final_label;
}

void
UnionFind::make_union(int x, int y)
{
  int i = x;
  while (parent[i] != 0)
    i = parent[i];

  int j = y;
  while (parent[j] != 0)
    j = parent[j];

  if (i != j)
    parent[j] = i;
}

int
UnionFind::generate_final_label()
{
  int label = 0;

  for (size_t i = 0; i < size; ++i)
    {
      if (parent[i] == 0)
	{
	  final_label[i] = label;
	  // std::cout << "Final label " << i << " -> " << label << std::endl;

	  label++;
	}
    }

  return label;
}
		      
int
UnionFind::find(int x)
{
  int i = x;
  while (parent[i] != 0)
    i = parent[i];

  return final_label[i];
}

/* *********************************************************************************************** */
