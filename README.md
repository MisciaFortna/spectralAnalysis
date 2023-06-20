# spectralAnalysis
## About The Project
Scripts for Graphing Spectral Data Using Standard TOPAS PHSP Phase-Space Data Files
## Getting Started
### Installation
git clone 'SSH-Key'
## Usage
### reader.py
Reader for obtaining csv files and energy histograms of sphere shell data
* python3 reader.py -t dataFile.txt
* python3 reader.py -r dataFile.csv -d 10 --scatter
### genReader.py
General reader for standard energy histograms 
* python3 genReader.py -t dataFile.txt
* python3 genReader.py -r dataFile.csv -p '22' -p '2112' -p '2212' -s
### neutronRatio.py
Gives a histogram of ratio of neutrons to photons and protons with respect to 10 degree bins around beamline
* python3 neutronRatio.py -n dataFile.csv
### specReadLib.py
Spectral Data Library for additional functions
## Roadmap
- [] Updating neutronRatio.py to be more user-friendly
- [] Completing documentation for the scripts
- [] Increase specReadLib module
## Contributing
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## Contacts
Miscia Fortna - mfortn5@lsu.edu
Project Link: https://github.com/MisciaFortna/spectralAnalysis.git 

