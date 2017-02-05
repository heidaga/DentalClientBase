# DentalClientBase Changelog
*****************************

* v0.11.5.4:
- Bug fix: allow deleting any selected act in the preferences 
  default

* v0.11.5.3:
- Bug fix: when opening invoice, point directly on the 
  client export subfolder. If not possible, point on
  export directory

* v0.11.5.2:
- Create subfolder for each doctor when exporting invoice
- Changed order of patient column in table and invoice
- Logo is hardcoded into the html invoice

* v0.11.4.2:
- Add currency in interface and invoice when applicable
- Correct test function in Structs

* v0.11.3.2:
- Improvement: no warning if empty act type combo is clicked
- Improvement: warning if trying to edit unit price while act type combo is empty
- Slightly increase warning icon resolution

* v0.11.2.2:
- Improvement: shortcut to delete doctor (wihout confirmation) CTRL+Del_key
- Improvement: shortcut to create act CTRL+A
- Improvement: shortcut to delete act (wihout confirmation) CTRL+D
- Improvement: shortcut to create payment CTRL+P
- Improvement: shortcut to delete payment (wihout confirmation) CTRL+R
- Bug fix attempt: no need to re select another doctor to refresh table
- Bug fix: close application bug fix (reimplement via event handling)
- Bug fix: delete via shortcut causes invalid index (fixed model data function)
- Bug fix: doctor table regular column spacing
- Re enable open HTML invoice after exporting

* v0.11.1.1:
- signals emitted when prices get changed bug fix
- add reporting feature (direct via email)
- improved closing application with Save/Ignore/Cancel

* v0.11.0.0:
- Major change: compare doctor prices with settings
  and handle differences in acts
- Changes to DefaultPrices in settings or DoctorPrices
  are reported in a separate table for each doctor
- Feature: single click to edit table
- TODO: unhandled signals emitted when prices get changed

* v0.10.2.5:
- Add totals for acts and payments
- Update totals on doctor new selection
- Bug fix: date choice in payment table

* v0.10.1.4:
- Bug fix: refresh act table and payment table after adding
- Notes column is the last column
- Better column size policy
- New acts start with quantity 1 (not 0)
- Close using Esc key checks for validity

* v0.10.1.3:
- Bug fix: invoice number beginning from zero after reset

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


# DentalClientBase To-Do list
*****************************
* Add settings/switches to Settings window
* Reset Invoice counter
* Implement number validation rules in all tables (to refuse negatives, alphanumerics ...)