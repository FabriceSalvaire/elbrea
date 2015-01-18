/* *********************************************************************************************** */

/*
 * Maximal value for 64-bit unsigned integer = 2**64 -1 = 18446744073709551615
 *
 */

/* *********************************************************************************************** */

#include <iostream>
#include <sys/time.h>
#include <unistd.h>

/* *********************************************************************************************** */

#include "IntelCpuTools.hpp"
#include "Platform.hpp"

/* *********************************************************************************************** */

/*
 * This information is available in the CPU name form CPUID or from dmidecode (BIOS).
 *
 * CPU clock is 100 or 133 Mhz * multiplier
 * This clock drives an unique Time Stamp Counter on platform.
 * 
 */

unsigned int
calibrate_cpu_clock(unsigned int waiting_time)
{
  CpuTSC cpu_tsc;
  sleep(waiting_time);
  uint64_t delta_tsc = cpu_tsc.delta();
  /* Error on clock is:
   * from propagation of uncertainty we have Vf/f**2 = Vd/d**2 + Vw/w**2
   * Ef = f * sqrt(Vd/d**2 + Vw/w**2)
   * f ~ f_measured * (1 +- Ew/w) if we neglect Vd
   * typical Ew is 100us, so Ef ~ 1 Mhz 
   */
  return delta_tsc / waiting_time;
}

/* *********************************************************************************************** */

CpuTSC::CpuTSC(unsigned int cpu_hz)
  : m_cpu_hz(cpu_hz)
{
  m_inverse_cpu_Mhz = 1e9 / static_cast<double>(m_cpu_hz);

  set();
}
  
void
CpuTSC::set()
{
  cpuid(); // start barrier,
	   //   cf. How to Benchmark Code Execution Times on Intel IA-32 and IA-64 Instruction Set Architectures
	   //   ref. 324264-001
  m_tsc0 = read_cpu_tsc();
}

uint64_t
CpuTSC::delta(bool set_timer)
{
  uint64_t tsc1 = read_cpu_tsc();
  cpuid(); // stop barrier

  uint64_t delta_tsc = tsc1 - m_tsc0;

  if (set_timer == true)
    m_tsc0 = tsc1;

  return delta_tsc;
}

double
CpuTSC::delta_us(bool set_timer)
{
  uint64_t delta_tsc = delta(set_timer);
  return static_cast<double>(delta_tsc) * m_inverse_cpu_Mhz;
}

/* *********************************************************************************************** */

DeltaTime::DeltaTime()
{
  set();
}

int
DeltaTime::get_time_of_day(uint64_t & seconds, uint64_t & micro_seconds)
{
  struct timeval time_value;
  int rc = gettimeofday(&time_value, NULL);
  if (rc != 0)
  {
    // both values are stored in long int
    seconds = time_value.tv_sec;
    micro_seconds = time_value.tv_usec;
    return 0;
  }
  else
    return 1;
}
  
void
DeltaTime::set()
{
  get_time_of_day(m_seconds0, m_micro_seconds0);
}

uint64_t
DeltaTime::delta_us(bool set_timer)
{
  uint64_t seconds1, micro_seconds1;
  get_time_of_day(seconds1, micro_seconds1);
  
  /* Overflow:
   *  1 day = 24*60*60 = 86 400 s
   *  1 year ~ 365*86400 = 31 536 000 s
   *  uint64_t ~ (2**64-1)/(365*86400)      ~ 584 942 417 355 years for seconds
   *           ~ (2**64-1)/(365*86400*1000) ~ 584 942 417     years for micro seconds
   */
  // seconds1 > seconds0
  uint64_t delta_seconds = seconds1 - m_seconds0;
  // micro_seconds should be < 1000
  int64_t delta_micro_seconds_int = static_cast<int64_t>(micro_seconds1) - static_cast<int64_t>(m_micro_seconds0);
  uint64_t delta_micro_seconds = static_cast<uint64_t>(static_cast<int64_t>(delta_seconds * 1000) + delta_micro_seconds_int);

  if (set_timer == true)
    {
      m_seconds0 = seconds1;
      m_micro_seconds0 = micro_seconds1;
    }

  return delta_micro_seconds;
}

/* *********************************************************************************************** */
