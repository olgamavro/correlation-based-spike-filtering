\# Correlation-Based Spike Filtering on DYNAP-SE1



This repository contains the code used for the project \*\*Correlation-Based Spike Filtering\*\*, where a spiking winner-take-all network was implemented on the DYNAP-SE1 neuromorphic processor. The network selects the input channel that is most temporally correlated with a reference spike train.



\## Repository Structure



\- `notebooks/`: experiment notebooks used to reproduce the reported results.

\- `src/`: reusable Python code for audio-to-spike conversion.

\- `config/`: DYNAP-SE1 parameter settings.

\- `audio/`: audio files used for keyword-spotting experiments.

\- `outputs/`: generated figures, spike files, and recordings.



\## Experiments



The repository includes notebooks for:



1\. Frequency matching and network validation

2\. Phase-shift matching

3\. Sequential frequency patterns

4\. Sinusoidal Poisson input signals

5\. Noise robustness

6\. Audio-based keyword spotting



\## Hardware Requirements



The experiments were designed for the DYNAP-SE1 neuromorphic processor and require Samna. Due to analog hardware variability, exact spike recordings may differ between chips or runs.



\## Code Availability



The code provides the network configuration, stimulus generation, recording, analysis, and plotting steps used in the report.

