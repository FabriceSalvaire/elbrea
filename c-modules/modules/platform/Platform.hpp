/* *********************************************************************************************** */

#ifndef __Plateform_H__
#define __Plateform_H__

/* *********************************************************************************************** */

#include <stdint.h>

/* *********************************************************************************************** */

// Return an estimate of the CPU clock frequency [hz]
//  waiting_time [s] set the accumulation time for the TSC
unsigned int calibrate_cpu_clock(unsigned int waiting_time = 1);

/* *********************************************************************************************** */

const unsigned int ONE_MHZ = 1000000;

class CpuTSC
{
public: // Ctor
  CpuTSC(unsigned int cpu_hz = ONE_MHZ);

public: // Methods
  void set();
  uint64_t delta(bool set_timer = false);
  double delta_us(bool set_timer = false);

private: // Members
  unsigned int m_cpu_hz;
  double m_inverse_cpu_Mhz;
  uint64_t m_tsc0;
};

/* *********************************************************************************************** */

class DeltaTime
{
public:
  // Ctor
  DeltaTime();

public:
  // Methods
  void set();
  uint64_t delta_us(bool set_timer = false);

private: // Static Methods
  static int get_time_of_day(uint64_t & seconds, uint64_t & micro_seconds);

private: // Members
  uint64_t m_seconds0;
  uint64_t m_micro_seconds0;
};

/* *********************************************************************************************** */

#endif /* __Plateform_H__ */

/* *********************************************************************************************** */
