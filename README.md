## TunnelFrame Designer - EngTools Utility Suite

### General Information -TunnelFrame Utility

The TunnelFrame design program provides a utility for quickly creating a SAP2000 model for a standard type of
rectangular frame. Taking inputs of a frame's geometric dimensions, material modifiers and engineering inputs (ie
loadings values)
the utility creates a file containing a SAP2000 representation of the frame, bypassing a time-consuming process of
manual input of the frame values and geometry into SAP2000 by engineering staff.

This export file can then be easily imported into SAP-2000, and the engineer can continue with the design analysis,
rather than spending time meticulously entering and assigning values such as frame geometry, loadings and other
engineering modifiers.

### Current Project Status - Engtools

The EngTools Project is at an early stage of development. The current proof-of-concept contains a bare-bones front-end 
to display the SAP-2000 frame generation utility. A more mature product aims to incorporate a modern front-end with a 
webpack/babel/React JS pipeline, comprehensive user account controls & features, usage analytics, event logging & a 
robust testing suite.

The long-term product vision is a suite of engineering utilities accessible at one central website to automate some of the more 
mundane and tedious tasks (civil) engineering staff encounter during the design process. To find those areas where the industry standard
comprehensive software offerings are inefficient, not user-friendly, or simply lacking in functionality and fill those voids. 
The objective is to increase the productivity of Engineering Staff by allowing them to focus on Engineering Design where
the present software paradigm sometimes forces them into tedious and time-consuming basic-data entry (IE in the case 
of rectangular tunnel-frame design in SAP2000). 

Keeping the utility suite in one web application allows an easy pathway for future development, addition of new utilities 
to the suite, and easy, reliable access for engineering users at a central location. It keeps the door open for future commercial potential
of the utility suite using the Software-As-A-Service model, if the suite reaches a mature stage of development.

#### Open Source Libraries Utilized
* Pycairo for vector graphics
* Openpyxl for creating Excel Workbooks - SAP2000 compatable import file. 

#### Potential Front-End Design
* Webpack/Babel/React JS pipeline
* Material-UI for User Interface

#### Potential Django Deployment Strategy

* Django with gunicorn and NGINX w/ a MySQL backend on the same server. 
