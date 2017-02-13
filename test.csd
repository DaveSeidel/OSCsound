<CsoundSynthesizer>
<CsInstruments>

sr=44100
ksmps=32
nchnls=2
0dbfs=1

instr Ladder
  kfreq   chnget "freq"
  kcutoff chnget "cutoff"
  kres    chnget "resonance"

  kcutoff port kcutoff, 0.05
  kres port kres, 0.05

  aout1 vco2 0.5, kfreq
  aout2 moogladder aout1, kcutoff, kres
  outs aout1, aout2
endin

alwayson "Ladder"

</CsInstruments>

<CsScore>
</CsScore>

</CsoundSynthesizer>
