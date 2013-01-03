HouseAgent-Astral
=================

Provide sunrise, sunset, dawn, dusk and solar noon values to HouseAgent. 
Can be used to trigger events that depend on those times.

Uses the astral python library from:
http://www.sffjunkie.co.uk/python-astral.html

This plugin provides five values every minute:
- Sunrise delta
- Sunset delta
- Dawn delta
- Dusk delta
- Solar noon delta

These delta values are in minutes from the event. For example, a sunrise delta
value of -30 (minus 30) means that the sunrise time is 30 minutes from now.

Setup instructions
------------------

1. Install the astral library: 'pip install astral' or 'easy_install astral'
2. Add the plugin to HouseAgent via the 'Manage plugins' screen.
3. Manually create a device for the Astral plugin with address '1' via the
   'Manage devices' screen
4. Edit the 'astral.conf' file and put the generated Auth code (GUID) from the
   step 2 behind the 'id=' line in the general section
5. Also configure your city in the same configuration file. A list of available
   cities can be obtained from the astral source code:
   http://bazaar.launchpad.net/~sffjunkie/astral/trunk/view/head:/astral/astral.py
6. Run both HouseAgent itself and the HouseAgent-Astral plugin and within a
   minute the delta values should show up in HouseAgent
