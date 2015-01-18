#ifndef __ImageEXCEPTION_H__
#define __ImageEXCEPTION_H__

/**************************************************************************************************/

#include <stdint.h>
#include <cstdlib>
#include <exception>
#include <string>

using namespace std;

/**************************************************************************************************/

class ImageException : public exception
{
public:
  ImageException(const char *error_message) throw() : m_error_message(error_message) {}
  ~ImageException () throw () {}
  
  virtual const char * what() const throw()
  {
    return m_error_message.data();
  }
  
private:
  string m_error_message;
};

/**************************************************************************************************/

#endif /* __ImageEXCEPTION_H__ */

/**************************************************************************************************/
