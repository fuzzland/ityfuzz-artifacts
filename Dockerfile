FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-venv libz3-dev libssl-dev clang pkg-config cmake wget 
RUN apt install -y git
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN bash -c "curl https://sh.rustup.rs -sSf | sh -s -- -y"

# build ityfuzz
WORKDIR /app
RUN git clone https://github.com/fuzzland/ityfuzz.git
WORKDIR /app/ityfuzz
RUN git checkout 45ec9d59ae563d0aa599c3a0f6ba88b68e11a412
RUN wget https://raw.githubusercontent.com/fuzzland/ityfuzz-test-cache/master/eval.diff
RUN git apply eval.diff
RUN mv /root/.cargo/bin/* /usr/local/bin/
RUN bash -c "cargo build --release"

# build smartian
WORKDIR /app

RUN apt-get update && \
    apt-get -yy install \
      wget apt-transport-https git unzip \
      build-essential libtool libtool-bin gdb \
      automake autoconf bison flex sudo vim \
      curl software-properties-common \
      python3 python3-pip libssl-dev pkg-config \
      libsqlite3-0 libsqlite3-dev apt-utils locales \
      libleveldb-dev python3-setuptools \
      python3-dev pandoc python3-venv \
      libgmp-dev libbz2-dev libreadline-dev libsecp256k1-dev locales-all
RUN wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && apt-get -yy install dotnet-sdk-5.0 && \
    rm -f packages-microsoft-prod.deb

RUN git clone https://github.com/SoftSec-KAIST/Smartian.git && \
    cd Smartian && \
    git checkout v1.0 && \
    git submodule update --init --recursive

RUN sed  "/myget/d" ./Smartian/nethermind/src/NuGet.config > ./Smartian/nethermind/src/NuGet.config2 
RUN mv ./Smartian/nethermind/src/NuGet.config2 ./Smartian/nethermind/src/NuGet.config
RUN cd ./Smartian && make

RUN pip3 install tqdm web3 matplotlib

RUN git clone https://github.com/SoftSec-KAIST/Smartian-Artifact


# cleanup rust cache
RUN rm -rf /root/.cargo/registry
RUN rm -rf /app/ityfuzz/target/release/deps
RUN rm -rf /app/ityfuzz/target/release/build
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /root/.rustup
RUN rm -rf /root/.cache
RUN rm -rf /root/.nuget

COPY *.py /app/
COPY *.sh /app/
