# 2025-07-12
In Windows git-bash
```bash
cd /c/D/code
git clone git@github.com:sweenip/OneDriveExplorer.git
cd OneDriveExplorer/
git branch -r | grep -v '\->' | while read remote; do git branch --track "${remote#origin/}" "$remote"; done 
git branch
#   dev
# * master
git checkout dev
uv venv .venv_win
source .venv_win/Scripts/activate
uv pip install -r OneDriveExplorer/requirements.txt
# Using Python 3.13.5 environment at: .venv_win
# Resolved 16 packages in 377ms
# Prepared 8 packages in 6.28s
# Installed 16 packages in 972ms
#  + cerberus==1.3.7
#  + dissect-cstruct==4.5
#  + enum-compat==0.0.3
#  + et-xmlfile==2.0.0
#  + numpy==2.3.1  
#  + openpyxl==3.1.5
#  + pandas==2.3.1 
#  + pycryptodome==3.23.0
#  + python-dateutil==2.9.0.post0
#  + python-registry==1.3.1
#  + pytz==2025.2
#  + ruamel-yaml==0.18.14
#  + ruamel-yaml-clib==0.2.12
#  + six==1.17.0
#  + tzdata==2025.2
#  + unicodecsv==0.14.1
python ./OneDriveExplorer/OneDriveExplorer.py -s //c:/D/code/OneDriveExplorer/tmp/ztsdaf1471/OneDrive_250709 --csv tmp
# C:\D\code\OneDriveExplorer\OneDriveExplorer\OneDriveExplorer.py:217: SyntaxWarning: invalid escape sequence '\ '
#   print('Error: Remove trailing \ from directory.\nExample: --json "c:\\temp" ')
# C:\D\code\OneDriveExplorer\OneDriveExplorer\OneDriveExplorer.py:225: SyntaxWarning: invalid escape sequence '\ '
#   print('Error: Remove trailing \ from directory.\nExample: --csv "c:\\temp" ')
# C:\D\code\OneDriveExplorer\OneDriveExplorer\OneDriveExplorer.py:233: SyntaxWarning: invalid escape sequence '\ '
#   print('Error: Remove trailing \ from directory.\nExample: --html "c:\\temp" ')

#      _____                ___                           ___                 _
#     (  _  )              (  _`\        _               (  _`\              (_ )
#     | ( ) |  ___     __  | | ) | _ __ (_) _   _    __  | (_(_)       _ _    | |    _    _ __   __   _ __
#     | | | |/' _ `\ /'__`\| | | )( '__)| |( ) ( ) /'__`\|  _)_ (`\/')( '_`\  | |  /'_`\ ( '__)/'__`\( '__)
#     | (_) || ( ) |(  ___/| |_) || |   | || \_/ |(  ___/| (_( ) >  < | (_) ) | | ( (_) )| |  (  ___/| |
#     (_____)(_) (_)`\____)(____/'(_)   (_)`\___/'`\____)(____/'(_/\_)| ,__/'(___)`\___/'(_)  `\____)(_) v2024.11.20
#                                                                     | |        by @bmmaloney97
#                                                                     (_)
    
# Saving OneDrive data. Please wait.... /

# 18825 files(s) - 0 deleted, 2583 folder(s) in 4.5411 seconds
```