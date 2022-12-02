CPPFLAGS = -std=c++17
SRC_DIR = ./
LAST_MODIFIED_CXX_FILE = $(shell ls -rt $(SRC_DIR)/*\.cc | tail -1)

# Compile and run the last modified file.
.PHONY: last
last: $(notdir $(basename $(LAST_MODIFIED_CXX_FILE))).out

%.out: %.cc  
	$(CXX) $(CPPFLAGS) -o $@ $<  # Compile n.cc into n.out
	./$@  # execute the compiled binary

.PHONY: clean
clean:
	rm -rf *.out
