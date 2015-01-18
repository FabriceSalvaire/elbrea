#ifndef __DISJOINTSET_H__
#define __DISJOINTSET_H__

/* *********************************************************************************************** */

// #include <cstdint>
#include <stdint.h>

#include <vector>

using namespace std;

/* *********************************************************************************************** */

class DisjointSet
{
public: // Typedef
  typedef unsigned int id_t;

public: // Ctor
  // default ctor, etc. ?
  DisjointSet(size_t size, bool compression_path=true);

public: // Methods
  void reset();
  // union is a reserved word
  id_t merge(id_t x, id_t y);
  id_t find(id_t x);

private: // Methods
  inline bool check_id(id_t x) const
  {
    return x < m_size;
  }

  id_t find_unchecked(id_t x);

private: // Members
  size_t m_size;
  bool m_compression_path;
  vector<id_t> m_parents;
  vector<size_t> m_ranks;
};

/* *********************************************************************************************** */

#endif /* __DISJOINTSET_H__ */

/* *********************************************************************************************** */
