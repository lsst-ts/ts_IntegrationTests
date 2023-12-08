.. _Version_History:

===============
Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized amongst CSCs.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each CSC link to whatever method of tracking is being used for that CSC until standardization occurs.
.. No new work should be required in order to complete this section.
.. Below is an example of a version history format.

v0.17.2
-------
* Swapped the order of the Watcher and the OCPS:2||3 in the obssys_state_transition_configs.

v0.17.1
-------
* Updated the latiss_acquire_and_take_sequence 'test' and 'nominal' configs with Cycle34 changes.

v0.17.0
-------
* Parameterized the OCSP 2||3 index, determined by test environment.
* Updated love_stress_test to define the LOVE 'location' URL based on the test environment.
* Added LOVE kubernetes instance testing.

v0.16.0
-------
* Added Watcher to the ObsSys State transition tests.
* Added MTPtg park and stop tracking tests to MainTel Housekeeping.
* Consolidated the ObsSys 1 & 2 tests into just ObsSys.
* Added the auxtel_slew_and_take_image_checkout.py integration test module.

v0.15.0
-------
* Added the ESS:106 CSC.

v0.14.2
-------
* Added the parameterized build section to requirements in conda/meta.yaml.

v0.14.1
-------
* Updated noarch value to python in conda/meta.yaml.

v0.14.0
-------
* Made required arguments positional.

v0.13.0
-------
* Made the Watcher the first CSC to go offline.
* Removed the .playlist extension.
* Updated the auxtel_housekeeping.py script.
* Added ESS:301 to love_stress_test_configs.py.
* Updated Python version references in meta.yaml.

v0.12.0
-------
* Added the auxtel_latiss_checkout.py integration test module.

v0.11.0
-------
* Added the auxtel_telescope_dome_checkout.py integration test module.
* Updated script names and configurations.
* Fixed a bug in the wait_for_done function in base_script.py

v0.10.0
-------
* Removed the WeatherStation CSC.
* Added the ESS CSCs.

v0.9.3
------
* Added the Ending state and the timestampProcessEnd value to the ScriptQueue Controller and Base Clase. 

v0.9.2
------
* The ScriptQueue Controller and Base Clase now handle the Unknown, Unconfigured, Configured, Running and Stopping states.

v0.9.1
-------
* The Base Class now uses a callback to wait for each script to complete. 

v0.9.0
------
* Converted WeatherForecast CSC to Auto-Enabled.
* Base class now waits for the scripts to complete and returns the script_indexes and script_states.
* ScriptQueue Controller now mocks the ScriptQueue script event to indicate the script is complete.

v0.8.0
------
* Added the WeatherForecast CSC.
* Removed root user workaround from Jenkinsfile.

v0.7.0
------
* Added the LOVE Stress Test integration test.
* Updated the path to the prepare_for (OnSky, Flat) Standard scripts.
* Switched MTAlignment to LaserTracker:1, since it was renamed.
* Added an Auxtel Housekeeping task, to homeAzimuth for the ATDome.

v0.6.0
------
* Test:42 is indexed, not the name.
* Updated instrument port and filter names.
* Added auxtel_enable_atcs.
* AuxTelShutdown now ONLY shuts down the AuxTel.

v0.5.0
------
* Added the reset_offsets.py test, which is part of the AuxTel Night Operations integration test.
* Fixed some typos in comcam_calibrations.py.
* The load_camera_playlist.py script now correctly sets the index based on the Camera.
* Various minor configuration updates and improvements.

v0.4.1
------
* Fixed a script name.
* Correctly marked scripts as External.

v0.4.0
------
* Various miscellaneous tasks
   * Added the track-for argument to auxtel_track_target.py.
   * Added the --no-repeat flag to run_camera_playlist.py.
   * Renamed run_camera_playlist to load_camera_playlist.
   * Renamed auxtel_prepare_for_flatfield to auxtel_prepare_for_flat.
   * Removed standstill.yaml from configs/obssys2_state_transition_configs.py.
* Added the AuxTel and ComCam Image Taking Verification tests.
* Added the get_current_date classmethod to python/lsst/ts/IntegrationTests/base_script.py.
* Added the AuxTel and ComCam calibrations tests.
* Added the AuxTel Night Operations tests.
* Added the parameterized module to the install list.

v0.3.0
------
* Added the AuxTel and MainTel housekeeping tasks. These set the system to the desired state after the initial set of integration tests are complete.
* Added the Authorize CSC.

v0.2.1
------
* Fixed the order of scripts in enabled_offline.py so the ScriptQueue is shutoff last.

v.0.2.0
-------
* Added the standalone tests for the MTAirCompressor.
* Switched to pyproject.toml.
* Added many new integration test scripts.

v0.1.1
------
* Changed queue placement from AFTER to LAST.

v0.1.0
------
* Created base script class for handling common work.
* Create script controller for unit testing.
* Created registry mechanism for handling script configurations.
* Implemented first part of AuxTel visit test.

v0.0.1
------
* Initial version: integration test and documentation infrastructure in place, but no real content, yet.
