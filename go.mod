module github.com/kwsp/advent-of-code

go 1.21.4

require github.com/schollz/progressbar/v3 v3.14.1
require github.com/kwsp/gotlib v0.0.0

require (
	github.com/mitchellh/colorstring v0.0.0-20190213212951-d06e56a500db // indirect
	github.com/rivo/uniseg v0.4.4 // indirect
	golang.org/x/sys v0.15.0 // indirect
	golang.org/x/term v0.15.0 // indirect
)

replace (
  github.com/kwsp/gotlib => ./gotlib
)