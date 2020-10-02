# vr-viewport-analysis

## Introduction

Optimizing VR videos is often a necessity as network usage exceeds the maximum bandwidth available to the device. Past researchers had made significant progress through predicting users' viewport based on previous head movements. However, we believe that the number of salient features in VR videos also play an important role in determining the areas of interest, which can aid efforts to decrease the amount of data transferred. By combining patterns observed through source videos and user's viewport data, it might be possible to further improve on the existing baseline.

## Hypothesis

Through the taxonomic classification of VR Viewport videos and the usage of machine learning algorithms on moving central objects we can significantly reduce data bandwidth with viewport prediction based on how fast user viewport speeds are.

## Progress

1. Goal: Determine the margin of error for the correlation between the viewport data and salient feature data with Python
2. **First part**: Determine if we can use salient features/if they correlate
3. **Second part**: if we determine that salient features are a good representation of what people are looking at, determine how we can use salient features