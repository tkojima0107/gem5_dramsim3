# https://www.gem5.org/documentation/learning_gem5/part1/simple_config/

import m5
from m5.objects import *
from pathlib import Path

gem5_dir = Path(__file__).resolve().parents[2]

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = X86TimingSimpleCPU()

system.membus = SystemXBar()

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = DRAMsim3()
dramsim3_conf_name = "DDR4_8Gb_x4_2400"
system.mem_ctrl.configFile = f"{gem5_dir}/ext/dramsim3/DRAMsim3/configs/{dramsim3_conf_name}.ini"
system.mem_ctrl.filePath = "./"
print("DRAMSim3 instantiated with {}".format(system.mem_ctrl.configFile))
system.mem_ctrl.port = system.membus.mem_side_ports

binary = f"{gem5_dir}/tests/test-progs/hello/bin/x86/linux/hello"

# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
