# Makefile for source rpm: libgcrypt
# $Id$
NAME := libgcrypt
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
