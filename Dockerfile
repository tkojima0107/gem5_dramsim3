FROM ghcr.io/gem5/ubuntu-22.04_all-dependencies:latest

LABEL "maintainer"="Takuya Kojima (tkojima@hal.ipc.i.u-tokyo.ac.jp)"
LABEL "description"="Docker image for gem5 with DRAMSim3"

ARG BUILD_ISA=X86
ARG GEM5_VERSION=stable

RUN git clone https://github.com/gem5/gem5 && \
	cd gem5 && \
	git checkout ${GEM5_VERSION} && \
	cd ext/dramsim3/ && \
	git clone  https://github.com/umd-memsys/DRAMsim3 && \
	cd DRAMsim3 && \
	mkdir build && \
	cd build && \
	cmake .. && \
	make -j$(nproc) && \
	cd ../../../../ && \
	scons build/${BUILD_ISA}/gem5.opt -j$(nproc)

RUN pip3 install numpy matplotlib

COPY ./se_dramsim3.py /gem5/configs/example/se_dramsim3.py

ENTRYPOINT ["sleep", "infinity"]

