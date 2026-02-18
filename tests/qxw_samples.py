#!/usr/bin/env python3
from pathlib import Path


SIMPLE_QXW = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Workspace>
<Workspace xmlns="http://www.qlcplus.org/Workspace" CurrentWindow="VC">
 <Engine>
  <InputOutputMap>
   <BeatGenerator BeatType="Internal" BPM="120"/>
   <Universe Name="Universe 1" ID="0">
    <Output Plugin="ArtNet" UID="127.0.0.1" Line="0"/>
   </Universe>
  </InputOutputMap>
  <Fixture>
   <Manufacturer>Generic</Manufacturer>
   <Model>Test</Model>
   <Mode>3ch</Mode>
   <ID>1</ID>
   <Name>Fixture 1</Name>
   <Universe>0</Universe>
   <Address>0</Address>
   <Channels>3</Channels>
  </Fixture>
  <Function ID="0" Type="Scene" Name="Scene A" Path="Show">
   <Speed FadeIn="0" FadeOut="0" Duration="0"/>
   <FixtureVal ID="1">0,0,1,0,2,0</FixtureVal>
  </Function>
  <Function ID="1" Type="Scene" Name="Scene B" Path="Show">
   <Speed FadeIn="0" FadeOut="0" Duration="0"/>
   <FixtureVal ID="1">0,255,1,0,2,0</FixtureVal>
  </Function>
  <Function ID="2" Type="Chaser" Name="FULL SHOW" Path="Show">
   <Speed FadeIn="10" FadeOut="0" Duration="20"/>
   <Direction>Forward</Direction>
   <RunOrder>Loop</RunOrder>
   <SpeedModes FadeIn="PerStep" FadeOut="Common" Duration="PerStep"/>
   <Step Number="0" FadeIn="15" Hold="25" FadeOut="0">0</Step>
   <Step Number="1" FadeIn="15" Hold="25" FadeOut="0">1</Step>
  </Function>
 </Engine>
 <VirtualConsole>
  <Frame Caption="">
   <Button Caption="FULL SHOW" ID="10" Icon="">
    <WindowState Visible="True" X="10" Y="10" Width="100" Height="50"/>
    <Function ID="2"/>
    <Action>Toggle</Action>
   </Button>
  </Frame>
 </VirtualConsole>
</Workspace>
"""


def write_sample_qxw(path: Path) -> None:
    path.write_text(SIMPLE_QXW)

