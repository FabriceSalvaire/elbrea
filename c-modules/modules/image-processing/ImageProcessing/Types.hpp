#ifndef __TYPES_H__
#define __TYPES_H__

/* *********************************************************************************************** */

#include <stdint.h>
#include <cstdlib>
#include <typeinfo>

/**************************************************************************************************/

// Fixme: Improve
const uint16_t UINT16_INF = 0;
const uint16_t UINT16_SUP = (1 << 16) -1;

/**************************************************************************************************/

template<typename T> const char * type_name();

#define DEFINE_TYPE_NAME(T, NAME) template<> inline const char * type_name<T>() { return NAME; }

DEFINE_TYPE_NAME(uint8_t,  "uint8")
DEFINE_TYPE_NAME(uint16_t, "uint16")
DEFINE_TYPE_NAME(uint64_t, "uint64")

DEFINE_TYPE_NAME(int16_t, "int16")
DEFINE_TYPE_NAME(int64_t, "int64")

DEFINE_TYPE_NAME(float,  "float")
DEFINE_TYPE_NAME(double, "double")

/**************************************************************************************************/

/*
 * Type Traits Interface
 *
 */
class TypeTraits // Fixme: _traits
{
public:
  virtual const class std::type_info& type_info() const = 0;
  virtual const char* name() const = 0;
  virtual size_t byte_size() const = 0;
  inline size_t number_of_bits() const { return 8 * byte_size(); }; // Fixme: store or compute ?
  inline size_t number_of_bytes(size_t i) const { return i * byte_size(); };
};

/**************************************************************************************************/

/*
 * Signed: Two's complement
 *
 * 00...0 | 0
 * 01...0 | sup > 0 = (1 << (number_of_bits -1)) -1
 * 10...0 | inf < 0 = 1 << (number_of_bits -1)
 * 11...1 | -1
 *
 */

template<typename T>
class Type : public TypeTraits // Fixme: required ? cf. operator ==
{
public:
  typedef T ValueType;
  typedef T* ValueTypePointer;
  typedef const T* ValueTypeConstPointer;
  // typedef TypeTraits Interface; 
  // typedef Type Self;

public:
  Type()
    : m_type_info(typeid(T)), m_name(type_name<T>()), m_byte_size(sizeof(T))
  {};

public:
  inline const class std::type_info& type_info() const { return m_type_info; };
  inline const char* name() const { return m_name; };
  inline size_t byte_size() const { return m_byte_size; };

  // inf, sup, signed property
  // static const PixelType PIXEL_INF = 0;
  // static const PixelType PIXEL_SUP = (1 << NUMBER_OF_BITS) -1;

private:
  const class std::type_info& m_type_info;
  const char* m_name;
  const size_t m_byte_size;
};

bool operator==(const TypeTraits &type1, const TypeTraits &type2);

/**************************************************************************************************/

typedef Type<uint8_t>  TypeUint8;
typedef Type<uint16_t> TypeUint16;
typedef Type<uint64_t> TypeUint64;

typedef Type<int16_t> TypeInt16;
typedef Type<int64_t> TypeInt64;

typedef Type<float>  TypeFloat;
typedef Type<double> TypeDouble;

/**************************************************************************************************/

#endif /* __TYPES_H__ */

/***************************************************************************************************
 * 
 * End
 * 
 **************************************************************************************************/
