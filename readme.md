# What is it?

## Source and first manual step
Original file was taken from [here](https://cs.uwaterloo.ca/~csk/spectre/examples/patch.pdf) (`patch.pdf`).
It was edited in Inkscape to get `unclipped.svg`.

## Normalization
```
python3 normalize7.py unclipped.svg normalized.svg
```
This gives rotations in `<defs>` and `<uses>` that follow:
```
  <defs>
    <path id="rep0" d="m 0,0 -5.197,-8.996 h -20.77 L -31.165,0 -40.161,-5.197 -49.157,0 l 5.198,8.996 h 10.385 v 10.385 l 8.996,5.197 5.197,-8.996 H -8.996 V 5.197 Z" style="fill:none;fill-opacity:1;fill-rule:nonzero;stroke:#231f20;stroke-width:0.99975002;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"/>
    <use id="rep1" xlink:href="#path246" transform="rotate(120)" />
    <use id="rep2" xlink:href="#path246" transform="rotate(240)" />
    <use id="rep3" xlink:href="#path246" transform="rotate(60)" />
    <use id="rep4" xlink:href="#path246" transform="rotate(180)" />
    <use id="rep5" xlink:href="#path246" transform="rotate(300)" />
    <use id="rep6" xlink:href="#path246" transform="rotate(330)" />
    <use id="rep7" xlink:href="#path246" transform="rotate(150)" />
    <use id="rep8" xlink:href="#path246" transform="rotate(270)" />
    <use id="rep9" xlink:href="#path246" transform="rotate(90)" />
    <use id="rep10" xlink:href="#path246" transform="rotate(210)" />
    <use id="rep11" xlink:href="#path246" transform="rotate(30)" />
  </defs>

  <use xlink:href="#rep0" transform="matrix(1.3333333,0,0,-1.3333333,729.7188,-11.360933)" />
  <use xlink:href="#rep0" transform="matrix(1.3333333,0,0,-1.3333333,598.6424,6.2026667)" />
  ...
  ```

## Expansion
This was edited further into `jigsaw1.svg` and `jigsaw3.1.svg`.

`jigsaw3.2.svg` is created by:
```
python /home/tci/python-projects/spectre/expand10.py
```

Note: **Path** of `rep0` has to have `stroke:#ff0000`.

## Final edits
Before laser cutting it's necessary to clip it to size and remove not needed cuts.