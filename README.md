## DRAMSim3 enabled Gem5 simulation environment

### Usage

1. Clone the repository
2. Docker image build
```
docker-compose build
```

3. Docker container run
```
docker-compose up -d
```

4. Docker container attach
```
docker exec -it gem5_sim_container /bin/bash
```

5. Run the simulation
```
cd /work
/gem5/build/X86/gem5.opt /gem5/configs/example/se_dramsim3.py
```

6. Visualize DRAMSim3 output
```
python3 /gem5/ext/dramsim3/DRAMsim3/scripts/plot_stats.py dramsim3.json
```