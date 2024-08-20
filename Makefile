# Variable for object files or other temporary files to clean up
CLEAN_FILES = main.c main

# Variable for source files
SRC_FILES = main.c

# Output executable name
OUTPUT = dotmastr

# Compiler
CC = gcc

# Compiler flags
CFLAGS = -I/usr/include/python3.12 -lpython3.12 -O2 -ffast-math -march=native -fomit-frame-pointer -flto -fno-exceptions

# Default rule (compiles the program)
all: build $(OUTPUT)

# Rule to compile the program
$(OUTPUT): $(SRC_FILES)
	$(CC) $(CFLAGS) -o $(OUTPUT) $(SRC_FILES)

# Rule to build (you can replace `echo "Building..."` with your custom command)
build:
	@echo "Generating C files with cython..."
	cython main.py --embed

# Rule to clean up files
clean:
	rm -f $(CLEAN_FILES) $(OUTPUT)

# Phony targets to avoid conflicts with file names
.PHONY: all build clean
