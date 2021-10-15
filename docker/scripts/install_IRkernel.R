#!/usr/bin/env Rscript
install.packages('IRkernel')
IRkernel::installspec(user=FALSE, sys_prefix=TRUE)  # to register the kernel in the current R installation
