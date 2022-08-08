.. _Version_History:

===============
Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized amongst CSCs.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each CSC link to whatever method of tracking is being used for that CSC until standardization occurs.
.. No new work should be required in order to complete this section.
.. Below is an example of a version history format.

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
