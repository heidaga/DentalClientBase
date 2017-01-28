# DentalClientBase Changelog

* v0.10.1.2:
- Completed feature of unique unit prices per doctor:
  changeable in the future without affecting 
  previous history entries
- Bug fix: cannot add acts in act table
- Bug fix: Pressing escape exits without saving to database
- Acts table row selection
- Changed selection color
- Changed closable tabs to normal tabs + shape change in UI 
- Strip New Doctor entry details from spaces

* v0.10.1.1:
- Added boolean switch to control PDF export
- Bug fix link between database payment and invoice

* v0.10.0.0:
- Major interface changes
- Added web viewer to visualize the html invoice inside app
- Added movable tabs with web page
- Fixed PDF export issues
- Fixed connection problem between acts and payments tables
- Added new boolean settings switches
- Minor changes to setup file

* v0.9.0.2:
- bug fix in py2exe setup (wrong path to icon)

* v0.9.0.1:
- bug fix in installer batch

* v0.9.0.0:
- finished implementation of payments table

* v0.8.1.0:
- switched installer to unicode

* v0.8.0.0:
- Added payments table (still inactive)
- bug fix: export not found, automatic creation
- canceled import weasyprint: py2exe bug 