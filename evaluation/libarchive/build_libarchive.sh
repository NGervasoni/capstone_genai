cd libarchive && autoreconf --force --install  && ./configure --disable-shared --without-nettle && 
  CXX=afl-g++-fast CC=fl-gcc-fast make