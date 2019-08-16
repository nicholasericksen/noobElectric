## Background
The following experiment is an attempt at studying the polarization response of common unknown houseplants.
Images are processed using cv2 for python.

```
To install opencv
brew install opencv3 --with-contrib --with-python3 --HEAD
```

The polarization of light has has inherent properties that are useful for applications in imaging.  Remote sensing technologies provide data on Earths various surfaces using different technologies that utilize properties of light.  Spectroscopy relies on different frequencies of wavelengths to response distinctly for different types of materials and conditions. Ellipsometry is a field focused on how light bends when interacting with surfaces under the basic guidance of Fresnel equations and Snells law.  Polarimetery utilizes the characteristic transformation materials produce when interacting with incident polarization states.

A Stokes vector represents the polarized and unpolarized portions of the electromagnetic wave.  Polarization in this mathematical form can be proven by starting with the equation of a wave, producing the polarization ellipse, and subsequently assigning components of this ellipse to a vectorized representation.

Mueller Matrices describe the transformation of light as it interacts with a material to produce an output Polarization state.  The signature transformation characteristics of a material can be useful for increasing the specifity and sensitivity in discrimination and classification problems.

In this study the interaction and scattering of light on leafs at various phases of the drying cycle are observed and quantified. It is known that the interaction of light on the leafs surface is determined by 3 main factors. [scattered vegetation] Properties of the Mueller Matrix are recorded for various samples to check for there usefulness in the staging of the leafs life cycles, as well as discriminating between various leaf types.  

[describe polarizance and MM]
[describe diattenuation and MM]

The polarization of light can be measured in many ways using different optical setups.  
[describe discrete optical setup]
[describe classical optical setup]

## Conclusion
These polarization measurements can be combined with other texture information such as Grey level co-occurrence matrices, to provide features for machine learning algorithms. This will increase the chances of determining the overall leaf health and age.

Big data techniques are utilized for processing the large amount of data that results from taking images.

Cells of plants were are used for microscopic inscpection of potentially staging cells in the various phases of the cell lifecycle.  Onion root tips in anapahse, metaphase, prophase and telephase were examined using similar techniques.
