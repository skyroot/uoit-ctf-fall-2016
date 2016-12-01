obj-m := diamorphine.o
CC = gcc -Wall 
KDIR := /lib/modules/3.13.0-96-generic/build
PWD := $(shell pwd)

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean
