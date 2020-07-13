[![GPL](https://img.shields.io/github/license/glowfly/glowfly_mods)](https://github.com/glowfly/glowfly_mods/blob/master/LICENSE)  
[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A01MQZP)

# MODs

This repository contains all MODs written for the [**GlowFly**](https://github.com/glowfly/glowfly_station) system.

![COVER](https://raw.githubusercontent.com/glowfly/glowfly_mods/master/img/cover.jpg)

## BOM (for one MOD)

- 3D Printed Parts
- 1x 24LC32A
- 1x 1x5 DuPont Female Connector
- Superglue
- Wire

## Build

Building a MOD cartridge is quite easy. Just take a bit of wire, the *23LC32A* and the DuPont connector and solder it as shown in the schematics.

![GlowFly MOD - Schematics](https://raw.githubusercontent.com/glowfly/glowfly_mods/master/img/GlowFLy-circuit-mod.png)

Here is a picture of my first one. Not pretty, but it works.

![GlowFly MOD](https://raw.githubusercontent.com/glowfly/glowfly_mods/master/img/MOD-Chip.jpg)

Take a bit of superglue and attach the DuPont connector to the cartridge shell. Make sure that the *ground pin* is oriented to the side of the shell **without the gap** and that it sits in the middle of the gap! Otherwise you will have a hard time to insert it into the MOD slot.

![GlowFly MOD](https://raw.githubusercontent.com/glowfly/glowfly_mods/master/img/MOD-Cart.jpg)

Now just glue the two shell halves together and you are done.

### Create MODs

**GlowFly** uses [mJS](https://github.com/cesanta/mjs/) to execute the MODs.
On every loop the scripts will get some variables injected by the script engine.

- **vol** *The calculated volume is a value between 0 and 100*
- **freq** *The dominant frequency of the current loop*
- **lVol** *The volume of the last loop*
- **lFreq** *The dominant frequency of the last loop*
- **minF** *The lowest frequency registered by GlowFly - 130hz -> Lowest note for viola, mandola*
- **midF** *The middle frequency value - 1046hz -> Highest note reproducible by average female*
- **maxF** *The highest frequency registered by GlowFly - 3140 -> Between highest note on a flute and on a 88-key piano* 
- **mLedC** *The total number of LEDs in the longest mesh route*
- **pLedC** *Number of LEDs prior of the current executing node*
- **nLedC** *Number of LEDs of the current executing node*
- **pNodeC** *Number of previous nodes in route*

Every script has to implement the *init*, *update* and *getName* method:

```
function init() {}
function update(delta) {}
function getName(){ return "NAME"; }
```

The script API exposes some methods to work with:

- **map(x, in_min, in_max, out_min, out_max)** *Maps a number in a certain range to the corresponding number in the output range*
- **round(number)** *Rounds a number to the next whole integer*
- **xrgb(r, g, b)** *Returns the hex representation of the given RGB color*
- **xhsv(h, s, v)** *Returns the hex representation of the given HSV color*
- **setDelay(count)** *If set to a value >0 the script engine will delay the frequency updates. For example with a value of '1', the script engine would delay the frequency updates by one other frequency update.*
- **setLed(index, hexColor)** *Set the LED with the given index to the given hex color*
- **getLed(index)** *Get the hex color of the given LED*
- **setGroup(index, [led1, led2, ...])** *Set a group of an array of leds to the given index - For example setGroup(0, [0,1]): a setLed(0) would now set index 0 and 1 together*
- **clearGroups()** *Clear all previous group definitions*

Look into the *mod* folder for some examples. If you write your own mod, try to avoid objects and arrays as much as possible. They are perfomance killers!

### Write MODs

Use the *writeMod.py* script to write the scripts to the cartridge. Please make sure, that Python 3 is installed.
Connect the **GlowFly Station** to your PC, insert a cartridge and execute the script:

```
python writeMod.py COM4 simple.GlowFly
```

The python script will tell you, if something went wrong. The **GlowFly Station** will show a *MOD saved*, if everything went well.
If you run the script without any parameters, it will list all available COM ports.