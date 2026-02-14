# QLC+ Fixture Definition Format (.qxf)

## Complete Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE FixtureDefinition>
<FixtureDefinition xmlns="http://www.qlcplus.org/FixtureDefinition">
 <Creator>
  <Name>Q Light Controller Plus</Name>
  <Version>4.13.1</Version>
  <Author>Author Name</Author>
 </Creator>
 <Manufacturer>Brand Name</Manufacturer>
 <Model>Model Name</Model>
 <Type>Color Changer</Type>

 <!-- Channel Definitions -->
 <Channel Name="Channel Name">...</Channel>

 <!-- Mode Definitions -->
 <Mode Name="Mode Name">...</Mode>

 <!-- Physical Properties -->
 <Physical>...</Physical>
</FixtureDefinition>
```

## Fixture Types

Common Type values: `Color Changer`, `Moving Head`, `Scanner`, `Dimmer`, `Strobe`, `Laser`, `LED Bar/Pixel`, `Flower`, `Hazer`, `Fan`, `Smoke`, `Effect`, `Other`.

## Channel Definitions

### Using Presets

For standard channel types, use the `Preset` attribute — QLC+ automatically assigns the correct Group, icon, and behavior:

```xml
<Channel Name="Master Dimmer" Preset="IntensityMasterDimmer"/>
<Channel Name="Red 1" Preset="IntensityRed"/>
<Channel Name="Green 1" Preset="IntensityGreen"/>
<Channel Name="Blue 1" Preset="IntensityBlue"/>
<Channel Name="White 1" Preset="IntensityWhite"/>
<Channel Name="Pan" Preset="PositionPan"/>
<Channel Name="Tilt" Preset="PositionTilt"/>
<Channel Name="Pan Fine" Preset="PositionPanFine"/>
<Channel Name="Tilt Fine" Preset="PositionTiltFine"/>
```

### Custom Channels with Capabilities

For channels with specific DMX value ranges (programs, gobos, strobes):

```xml
<Channel Name="Program">
 <Group Byte="0">Effect</Group>
 <Capability Min="0" Max="0">No Program</Capability>
 <Capability Min="1" Max="20">Auto Program 1</Capability>
 <Capability Min="21" Max="40">Auto Program 2</Capability>
 <!-- ... more capabilities ... -->
 <Capability Min="241" Max="255">Sound Active</Capability>
</Channel>

<Channel Name="Strobe">
 <Group Byte="0">Shutter</Group>
 <Capability Min="0" Max="0">No Strobe</Capability>
 <Capability Min="1" Max="255">Strobe Slow to Fast</Capability>
</Channel>
```

### Group Types

`Intensity`, `Colour`, `Gobo`, `Effect`, `Shutter`, `Beam`, `Pan`, `Tilt`, `Speed`, `Maintenance`, `Nothing`.

`Byte="0"` = coarse (MSB), `Byte="1"` = fine (LSB).

## Mode Definitions

A Mode maps channels to DMX offsets and defines Head groupings:

```xml
<Mode Name="15 Channel">
 <!-- Channel assignments (0-indexed) -->
 <Channel Number="0">Program</Channel>
 <Channel Number="1">Master Dimmer</Channel>
 <Channel Number="2">Strobe</Channel>
 <Channel Number="3">Red 1</Channel>
 <Channel Number="4">Green 1</Channel>
 <Channel Number="5">Blue 1</Channel>
 <!-- ... -->

 <!-- Head groupings (channel numbers from Mode, not fixture) -->
 <Head>
  <Channel>3</Channel>
  <Channel>4</Channel>
  <Channel>5</Channel>
 </Head>
 <Head>
  <Channel>6</Channel>
  <Channel>7</Channel>
  <Channel>8</Channel>
 </Head>
</Mode>
```

**Heads** group channels belonging to the same physical light source. For a 4-par bar, define 4 heads with their respective RGB (or RGBW) channels. Head channel numbers reference the Mode channel numbers, not absolute DMX addresses.

## Physical Properties

```xml
<Physical>
 <Bulb Type="LED" Lumens="0" ColourTemperature="0"/>
 <Dimensions Weight="5.5" Width="1050" Height="320" Depth="80"/>
 <Lens Name="Other" DegreesMin="0" DegreesMax="0"/>
 <Focus Type="Fixed" PanMax="0" TiltMax="0"/>
 <Technical PowerConsumption="36" DmxConnector="3-pin"/>
</Physical>
```

Focus Type values: `Fixed`, `Head`, `Mirror`, `Barrel`. DmxConnector: `3-pin`, `5-pin`, `3-pin and 5-pin`, `3.5mm`, `Wireless`.

## Common Multi-Head Fixtures

For fixtures with multiple independently controllable light sources (par bars, LED strips, pixel fixtures):

1. Define shared channels once (Program, Master Dimmer, Strobe)
2. Define per-head color channels with numbered suffixes (Red 1, Green 1, Blue 1, Red 2, Green 2, Blue 2...)
3. In the Mode, map all channels in the correct order
4. Create Head groups for each light source's color channels

The channel order in the Mode definition must exactly match the fixture's DMX protocol — verify against the manufacturer's manual.
