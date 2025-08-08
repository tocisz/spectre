# What is it?

## Source and first manual step
Original file was taken from [here](https://cs.uwaterloo.ca/~csk/spectre/examples/patch.pdf) (`patch.pdf`).
It was edited in Inkscape to get `unclipped.svg`.

## Normalization
```
python3 normalize6.py unclipped.svg normalized.svg
```
This gives rotations in `<defs>` and `<uses>` that follow:
```
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <path id="rep0" d="m 0,0 -5.197,-8.996 h -20.77 L -31.165,0 -40.161,-5.197 -49.157,0 l 5.198,8.996 h 10.385 v 10.385 l 8.996,5.197 5.197,-8.996 H -8.996 V 5.197 Z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep1" d="m 0,0 h 10.385 l 10.385,-17.992 -5.188,-8.996 9,-5.188 V -42.571 H 14.184 L 8.996,-33.575 0,-38.762 l -8.996,5.187 5.188,8.997 -5.188,8.996 8.996,5.197 z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep2" d="M 0,0 -5.197,8.996 5.197,26.988 h 10.385 v 10.385 l 8.996,5.198 5.188,-8.996 -5.188,-8.997 9,-5.197 V 8.996 H 23.18 L 17.992,0 8.996,5.197 Z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep3" d="M 0,0 5.197,-8.996 -5.197,-26.988 h -10.385 v -10.385 l -8.996,-5.198 -5.188,8.997 5.188,8.996 -8.996,5.197 v 10.385 h 10.381 L -17.992,0 -8.996,-5.197 Z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep4" d="m 0,0 5.197,8.996 h 20.77 L 31.165,0 40.164,5.188 49.16,0 43.96,-8.996 H 33.574 v -10.385 l -8.996,-5.197 -5.197,8.996 H 8.996 v 10.385 z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep5" d="m 0,0 h -10.385 l -10.385,17.992 5.188,8.996 -9,5.201 v 10.385 h 10.398 L -8.996,33.575 0,38.762 8.996,33.575 3.799,24.578 8.996,15.582 0,10.385 Z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep6" d="m 0,0 -8.988,-5.199 -17.998,10.392 0.008,10.383 -10.393,-0.002 -5.192,9 8.991,5.197 8.994,-5.193 5.192,8.994 10.39,0.003 0.003,-10.39 L 0,17.993 -5.192,8.999 Z" style="fill:none;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1" clip-path="none"/>
    <path id="rep7" d="m 0,0 8.988,5.199 17.998,-10.392 -0.008,-10.383 10.393,0.002 5.192,-9 -8.991,-5.197 -8.994,5.193 -5.192,-8.994 -10.39,-0.003 -0.003,10.39 -8.993,5.192 5.192,8.994 z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" clip-path="none"/>
    <path id="rep8" d="M 0,0 -8.996,5.184 V 25.967 L 0,31.152 -5.197,40.151 0,49.147 8.996,43.959 V 33.574 h 10.385 l 5.197,-8.996 -8.996,-5.197 V 8.996 H 5.197 Z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep9" d="M 0,0 8.996,-5.184 V -25.967 L 0,-31.152 5.197,-40.151 0,-49.147 l -8.996,5.188 v 10.385 h -10.385 l -5.197,8.996 8.996,5.197 v 10.385 h 10.385 z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep10" d="m 0,0 -0.008,10.383 17.998,10.392 8.988,-5.199 5.195,9.001 10.39,-0.003 0.005,-10.385 -8.994,-5.193 5.193,-8.993 -5.192,-8.999 -8.999,5.192 -8.994,-5.193 -5.193,8.994 z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <path id="rep11" d="m 0,0 0.008,-10.383 -17.998,-10.392 -8.988,5.199 -5.195,-9.001 -10.39,0.003 -0.005,10.385 8.994,5.193 -5.193,8.993 5.192,8.999 8.999,-5.192 8.994,5.193 5.193,-8.994 z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
  </defs>

  <use xlink:href="#rep0" transform="matrix(1.3333333,0,0,-1.3333333,729.7188,-11.360933)" />
  <use xlink:href="#rep0" transform="matrix(1.3333333,0,0,-1.3333333,598.6424,6.2026667)" />
  ...
  ```

  Manually substituted rotations of `rep0` to others:
  ```
    <g
     id="g304"
     style="display:inline"
     transform="translate(-88.147572,55.798008)">
    <path
       id="rep0"
       d="m 0,0 -5.197,-8.996 h -20.77 L -31.165,0 -40.161,-5.197 -49.157,0 l 5.198,8.996 h 10.385 v 10.385 l 8.996,5.197 5.197,-8.996 H -8.996 V 5.197 Z"
       transform="scale(1.3333333,-1.3333333)"
       style="fill:#000000;fill-opacity:1" />
    <use
       id="rep6"
       xlink:href="#rep0"
       transform="rotate(30)" />
    <use
       id="rep5"
       xlink:href="#rep0"
       transform="rotate(60)" />
    <use
       id="rep8"
       xlink:href="#rep0"
       transform="rotate(90)" />
    <use
       id="rep2"
       xlink:href="#rep0"
       transform="rotate(120)" />
    <use
       id="rep10"
       xlink:href="#rep0"
       transform="rotate(150)" />
    <use
       id="rep4"
       xlink:href="#rep0"
       transform="scale(-1)" />
    <use
       id="rep7"
       xlink:href="#rep0"
       transform="rotate(-150)" />
    <use
       id="rep1"
       xlink:href="#rep0"
       transform="rotate(-120)" />
    <use
       id="rep9"
       xlink:href="#rep0"
       transform="rotate(-90)" />
    <use
       id="rep3"
       xlink:href="#rep0"
       transform="rotate(-60)" />
    <use
       id="rep11"
       xlink:href="#rep0"
       transform="rotate(-30)" />
  </g>
```
Giving `normalized2.svg`.

## Expansion
This was edited further into `jigsaw1.svg` and `jigsaw3.1.svg`.

`jigsaw3.2.svg` is created by:
```
python /home/tci/python-projects/spectre/expand10.py
```

Note: **Path** of `rep0` has to have `stroke:#ff0000`.

## Final edits
Before laser cutting it's necessary to clip it to size and remove not needed cuts.