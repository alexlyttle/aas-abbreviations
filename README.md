# ads-journal-abbreviations

An `abbreviations.json` file using the [NASA ADS Bibliographic Codes: Journal Abbreviations](https://adsabs.harvard.edu/abs_doc/journals1.html).

To use this with Zotero, copy the `abbreviations.json` file into your `Zotero` home directory.

This extends the default Zotero abbreviations file with the bibliographic codes used by NASA ADS.

To update the `abbreviations.json` file, run `update_abbreviations.py`.

```bash
git clone https://github.com/alexlyttle/ads-journal-abbreviations.git
cd ads-journal-abbreviations
pip install -r requirements.txt  # install required python packages
python update_abbreviations.py   # updates abbreviations.json file
```
