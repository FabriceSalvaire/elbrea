/****************************************************************************************************
 * 
 *  Implements Tarjan Union-Find Algorithm
 * 
 *  To avoid dynamic allocation we have to define the set at the construction.  It is easy for a set
 *  (range) of integer.
 * 
 *  N = 1392*1040 * 10 = 14476800 * 10 = 14 476 800 pixels
 *  ceil(log2(N)) = 24 bits + sign bit => 32 signed integer => 4N B = 55 MB
 * 
 ***************************************************************************************************/

/* *********************************************************************************************** */

#include <iostream>
#include <sstream>
#include <stdexcept>

/* *********************************************************************************************** */

#include "DisjointSet.hpp"

/* *********************************************************************************************** */

DisjointSet::DisjointSet(size_t size, bool compression_path)
  : m_size(size),
    m_compression_path(compression_path),
    m_parents(size),
    m_ranks(size)
{
  reset();
}

void
DisjointSet::reset()
{
  // use an iterator instead?
  for (size_t i = 0; i < m_size; i++)
    {
      m_parents[i] = i;
      m_ranks[i] = 0;
    }
}

DisjointSet::id_t
DisjointSet::merge(DisjointSet::id_t x, DisjointSet::id_t y)
{
  id_t x_root = find(x);
  id_t y_root = find(y);
  
  id_t x_rank = m_ranks[x_root];
  id_t y_rank = m_ranks[y_root];
    
  if (x_rank > y_rank)
    {
      // exchange
      m_parents[y_root] = x_root;
      return x_root;
    }
  else if (x_rank < y_rank)
    {
      m_parents[x_root] = y_root;
      return y_root;
    }      
  else // x_rank == y_rank
    {
      if (x_root != y_root)
	{
	  m_ranks[y_root] += 1;
	  m_parents[x_root] = y_root;
	}

      return y_root; // right if == ?
    }
}

DisjointSet::id_t
DisjointSet::find(DisjointSet::id_t x) // not const
{
  if (check_id(x) == false)
    {
      std::ostringstream message;
      message << "DisjointSet::find id is out of range " << x;
      throw(out_of_range(message.str()));
    }

  return find_unchecked(x);
}

DisjointSet::id_t
DisjointSet::find_unchecked(DisjointSet::id_t x) // not const
{
  id_t x_parent = m_parents[x];

  // Descend recursively up to the root node for this set and then set
  // all the parent of the visited nodes to the root node during the
  // stack pop's sequence.
  //
  // Can we replace this recursive code by a while loop ?
  //   - path compression => to store the visited node during the descend.
  // 
  //     Stack node_stack;
  //     while (x_parent != x)
  //       {
  //         node_stack.push(x);
  //         x = x_parent
  //         x_parent = m_parents[x];
  //       }
  //     for (x in node_stack)
  //       m_parents[x] = x_parent;
  //
  //   - use void *alloca(size_t size) ?
  //   - implement in ASM to manipulate the stack ?
  //   

  if (x_parent != x)
    {
      x_parent = find(x_parent);
      m_parents[x] = x_parent;
    }
  
  return x_parent;
}

/* *********************************************************************************************** */
