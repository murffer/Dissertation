Dissertation
============

Matthew J. Urffer's Ph.D. Dissertation on how to effectively design Radiation Portal Monitors capable of replacing He-3.

## Build and Compile Instructions
  This work utilizes latex for the document typesetting and GIT for the version control.  The latest stable version of this document is available as the head on the master branch.

      git clone https://github.com/murffer/Dissertation.git
      cd Dissertation/
      git submodule init 
      git submodule update 
  
A makefile is provided for the compilation of the latex document.  Sucucessful compiolaiton is depednant upon generating the code documentation and having a temporary directory for the graphics output.

      python createCodeDoc.py 
      mkdir tmp
      make
  
