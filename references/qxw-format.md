# QLC+ Workspace Format (.qxw)

## Top-Level Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Workspace>
<Workspace xmlns="http://www.qlcplus.org/Workspace" CurrentWindow="VC">
 <Creator>
  <Name>Q Light Controller Plus</Name>
  <Version>5.0.1</Version>
  <Author>Author Name</Author>
 </Creator>
 <Engine>
  <!-- Fixtures, Functions, etc. -->
 </Engine>
 <VirtualConsole>
  <!-- UI layout -->
 </VirtualConsole>
 <Monitor DisplayMode="0" ShowLabels="0">
  <Font>Arial,12,-1,5,400,0,0,0,0,0,0,0,0,0,0,1</Font>
  <ChannelStyle>0</ChannelStyle>
  <ValueStyle>0</ValueStyle>
  <Grid Width="5" Height="3" Depth="5" Units="0"/>
  <StageItem>0</StageItem>
 </Monitor>
</Workspace>
```

## Engine Section

### Input/Output Mapping

```xml
<InputOutputMap>
 <BeatGenerator BeatType="Internal" BPM="174"/>
 <Universe Name="Universe 1" ID="0">
  <Output Plugin="ArtNet" UID="10.0.0.7" Line="0"/>
 </Universe>
</InputOutputMap>
```

Common output plugins: `ArtNet`, `E1.31`, `DMX USB`, `Loopback`.

### Fixture Definitions

```xml
<Fixture>
 <Manufacturer>Chauvet</Manufacturer>
 <Model>4BAR</Model>
 <Mode>15 Channel</Mode>
 <ID>0</ID>
 <Name>Chauvet 4BAR</Name>
 <Universe>0</Universe>
 <Address>0</Address>
 <Channels>15</Channels>
</Fixture>
```

`ID` is unique per fixture. `Address` is 0-indexed. `Universe` is 0-indexed.

### Scenes

```xml
<Function ID="0" Type="Scene" Name="Red All" Path="Base Colors">
 <Speed FadeIn="0" FadeOut="0" Duration="0"/>
 <FixtureVal ID="0">0,0,1,255,2,0,3,255,4,0,5,0,6,255,7,0,8,0,9,255,10,0,11,0,12,255,13,0,14,0</FixtureVal>
</Function>
```

- `ID`: Unique function identifier (integer)
- `Path`: Optional folder for organizing in the Function Manager
- `FixtureVal ID`: References the Fixture ID, not the function ID
- Values are comma-separated `channel,value` pairs (0-indexed channels)

### Chasers

```xml
<Function ID="100" Type="Chaser" Name="Strobe Snap" Path="High Energy">
 <Speed FadeIn="0" FadeOut="0" Duration="86"/>
 <Direction>Forward</Direction>
 <RunOrder>Loop</RunOrder>
 <SpeedModes FadeIn="Common" FadeOut="Common" Duration="Common"/>
 <Step Number="0" FadeIn="0" Hold="0" FadeOut="0">0</Step>
 <Step Number="1" FadeIn="0" Hold="0" FadeOut="0">1</Step>
</Function>
```

- Steps reference Scene function IDs
- `SpeedModes`: "Common" uses the Speed element values; "PerStep" uses each Step's individual timing
- `Duration` in Speed = hold time between fades
- Step attributes: `FadeIn`, `Hold`, `FadeOut` (used when SpeedModes is "PerStep")

#### PerStep Timing Example

For chasers with varying step durations (like accelerating strobes):

```xml
<Speed FadeIn="0" FadeOut="0" Duration="0"/>
<SpeedModes FadeIn="Common" FadeOut="Common" Duration="PerStep"/>
<Step Number="0" FadeIn="0" Hold="1379" FadeOut="0">10</Step>
<Step Number="1" FadeIn="0" Hold="690" FadeOut="0">11</Step>
<Step Number="2" FadeIn="0" Hold="345" FadeOut="0">12</Step>
<Step Number="3" FadeIn="0" Hold="172" FadeOut="0">13</Step>
<Step Number="4" FadeIn="0" Hold="86" FadeOut="0">14</Step>
```

### Collections

Group multiple functions to trigger simultaneously:

```xml
<Function ID="200" Type="Collection" Name="Full Show">
 <Step Number="0">100</Step>
 <Step Number="1">101</Step>
</Function>
```

### EFX (Effects)

For moving head pan/tilt patterns (circle, eight, line, etc.):

```xml
<Function ID="300" Type="EFX" Name="Circle Pan">
 <PropagationMode>Parallel</PropagationMode>
 <Speed FadeIn="0" FadeOut="0" Duration="5000"/>
 <Direction>Forward</Direction>
 <RunOrder>Loop</RunOrder>
 <Algorithm>Circle</Algorithm>
 <Width>127</Width>
 <Height>127</Height>
 <Rotation>0</Rotation>
 <Axis Name="X">
  <Offset>127</Offset>
  <Frequency>2</Frequency>
  <Phase>90</Phase>
 </Axis>
 <Axis Name="Y">
  <Offset>127</Offset>
  <Frequency>3</Frequency>
  <Phase>0</Phase>
 </Axis>
 <Fixture>
  <ID>0</ID>
  <Head>0</Head>
  <Direction>Forward</Direction>
  <StartOffset>0</StartOffset>
 </Fixture>
</Function>
```

## Virtual Console Section

### Frame (Container)

```xml
<Frame Caption="High Energy" ID="0">
 <Appearance>
  <FrameStyle>Sunken</FrameStyle>
  <ForegroundColor>Default</ForegroundColor>
  <BackgroundColor>Default</BackgroundColor>
  <Font>Default</Font>
 </Appearance>
 <WindowState Visible="True" X="0" Y="0" Width="400" Height="300"/>
 <!-- Buttons go inside frames -->
</Frame>
```

### Button

```xml
<Button Caption="Strobe Snap" ID="1" Icon="">
 <WindowState Visible="True" X="10" Y="40" Width="90" Height="90"/>
 <Appearance>
  <FrameStyle>None</FrameStyle>
  <ForegroundColor>4294967295</ForegroundColor>
  <BackgroundColor>4294901760</BackgroundColor>
  <Font>Default</Font>
 </Appearance>
 <Function ID="100"/>
 <Action>Toggle</Action>
 <Intensity Adjust="False">100</Intensity>
</Button>
```

### QLC+ 5 Color Format

QLC+ 5 uses unsigned 32-bit ARGB integers (stored as signed):

| Color | ARGB Hex | Integer |
|-------|----------|---------|
| Black | FF000000 | -16777216 |
| White | FFFFFFFF | -1 |
| Red | FFFF0000 | -65536 |
| Green | FF00FF00 | -16711936 |
| Blue | FF0000FF | -16776961 |
| Yellow | FFFFFF00 | -256 |
| Cyan | FF00FFFF | -16711681 |
| Purple | FF800080 | -8388480 |
| Orange | FFFF8C00 | -29440 |
| Dark Red | FF8B0000 | -7602176 |
| Dark Blue | FF00008B | -16777077 |

Formula: For a color with R,G,B values (0-255), the ARGB integer = `(0xFF << 24) | (R << 16) | (G << 8) | B`, interpreted as a signed 32-bit integer.

### Button Actions

- `Toggle`: Click on = start function, click off = stop
- `Flash`: Function runs while button is held down
- `Blackout`: Special — toggles blackout mode

### Slider

```xml
<Slider Caption="Master" ID="10" WidgetStyle="Slider" InvertedAppearance="false">
 <WindowState Visible="True" X="0" Y="0" Width="60" Height="200"/>
 <SliderMode ValueDisplayStyle="Percentage" ClickAndGoType="None" Monitor="false">Level</SliderMode>
 <Level LowLimit="0" HighLimit="255" Value="255">
  <Channel Fixture="0">1</Channel>
 </Level>
</Slider>
```

## ID Numbering Convention

Use consistent ID ranges for readability:
- Scenes: 0-99
- Chasers: 100-199
- Collections: 200-299
- EFX: 300-399
- VC widgets: sequential from 0

All function IDs must be unique across the entire workspace.
