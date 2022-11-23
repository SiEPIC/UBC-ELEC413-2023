# UBC-ELEC413-2023

The course project is to design a photonic integrated circuit that connects to an on-chip semiconductor laser.

This repository contains the merging framework and template example circuits.


# Submission details

  * Submissions into the fabrication run are done by [Pull Requests from forks of this repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
  


### Detailed Instructions for your creating and uploading your layout:

* Follow the instructions to install the [SiEPICfab EBeam ZEP Process Design Kit](https://github.com/SiEPIC/SiEPICfab-EBeam-ZEP-PDK), implemented in the open-source KLayout software and the SiEPIC-Tools Python plug-ins.

* Install GitHub Desktop, https://desktop.github.com

* Fork this repository

* Clone the repostory fork using GitHub Desktop. Do this by clicking on the green "Code" button, then "Open with GitHub Desktop"
  * Example below assumes it is installed in your Documents folder.

* in KLayout:
  * Create a new empty layout choosing Technology = SiEPICfab_EBeam_ZEP
    * you should see the layer table, and the SiEPIC menu
  * Install the forked project repository
    * menu Tools > Macro Development
	    * click on Python
		  * in the window below, right-click and choose Add Location, then find the UBC-ELEC413-2023 folder
		  * open the file UBC_ELEC413_TLDS_resonators
  		* Run it using the Play! button. You should see a layout with a laser and several individual designs

* Create your own design
  * in the Tools > Macro Development, find the folder UBC-ELEC413-2023/Layout/Designs
  * right-click on the folder, New, then Plain Python file (*.py)
  * type in the filename for your own design file, e.g., design_lukasc
  * open the file design_student1, select all, and copy the code
  * paste the code in your design file
  * replace "def design_student1" with "def design_lukasc" (the name has to match your filename *exactly*)
  * edit the script to create a design as you like

* Compile the layout generation code
  * open the file UBC_ELEC413_TLDS_resonators
	* Run it using the Play! button. You should see a layout with a laser and several individual designs
  * Debug, and complete the design

* Upload your design to GitHub
  * First upload it to your own Fork
    * in GitHub Desktop, choose the UBC-EELC413-2023 repository
    * In the "Changes" tab:
      * Change the selection of files: remove the merged layout files: Layout/UBC_ELEC413_TLDS_resonators*
      * bottom left, enter a summary (e.g., your name), 
      * click "Commit to main" 
    * top right: Fetch Origin
    * top right: Push Origin

* Make a Pull Request to get your design into the master course repository
  *   [Pull Requests from forks of this repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
  
  * Keep your local copy in sync with the online version:
     * Fetch - GitHub Desktop:
     * Current Repository = UBC-ELEC413-2023
     * top right: Fetch Origin


# Bragg grating design tips
  * Simulate the Bragg grating using ideal geometry (e.g., 350 nm width)
  * Fabrication process bias information is available in these [slides](https://docs.google.com/presentation/d/19F0aWFHHWYnfZA7-BLKOxTljj-T4D4Mc9Gzyav_P6xI).  Increase the size the Bragg grating to compensate for the fabrication process (e.g., increase by 36 nm, from 350 nm to 386 nm).
  
