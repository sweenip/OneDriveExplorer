# Syncing OneDrive Personal Vault Locally
How Personal Vault Works on Windows

Personal Vault is a special folder in your OneDrive that adds an extra layer of security by requiring two-factor authentication and storing files in an encrypted container on your PC. On Windows 10/11, OneDrive automatically downloads and keeps Personal Vault files in a BitLocker-encrypted area of your local hard drive, making them available offline whenever the vault is unlocked.

Step-by-Step: Enable Local Sync for Personal Vault
- Ensure BitLocker Is Enabled :Personal Vault requires BitLocker encryption on your system drive. If your PC isn’t already encrypted, Windows will prompt you to turn on BitLocker during the vault setup process.
- Set Up Personal Vault
- Open OneDrive and click the notification icon in the taskbar.
- Select Get started under Personal Vault (or open the Personal Vault folder directly).
- Follow the prompts to verify your identity using your chosen two-factor method (SMS, email, or Authenticator app).
- Unlock Your Personal Vault in File Explorer
- In File Explorer, navigate to OneDrive > Personal Vault.
- Authenticate again to unlock and access your files.
- Keep Files Synced Locally

Once unlocked, all files you add to or open from the Personal Vault folder are automatically downloaded into the encrypted area on your drive and will sync back to OneDrive whenever you’re online. There’s no separate “Always keep on this device” toggle—files remain available offline as long as the vault is unlocked.

Managing Offline Availability and Security
- Personal Vault locks automatically after a short period of inactivity (e.g., 20 minutes on the web, 3 minutes in mobile apps), but on Windows the encrypted files remain on disk and are only hidden until you re-unlock the vault.
- To manually secure your data, right-click the Personal Vault folder in File Explorer and select Lock Personal Vault.

Important Notes and Limitations
- Personal Vault sync and local encryption are only supported on OneDrive home/personal plans—not on OneDrive for Business or school accounts.
- You must use Windows 10 or later; Mac, Linux, and some mobile platforms only support accessing Personal Vault via the web or mobile apps.
- Because files are always stored locally in an encrypted container, Files On-Demand’s “online-only” placeholder mode does not apply to the Personal Vault folder.


# Querying the SQLite Database
If you have a SQLite copy of your settings (such as on macOS), use the built-in sqlite3 module:
```python
import os
import sqlite3

# Path to your SQLite OneDrive DB
db_path = os.path.expanduser("~/Library/Application Support/OneDrive/settings.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch Personal Vault entries
cursor.execute("""
  SELECT ItemID, Path, FileStatus, LastSyncTime
  FROM ItemProperties
  WHERE Path LIKE '%Personal Vault%'
  ORDER BY LastSyncTime DESC
""")

for item_id, path, status, last_sync in cursor.fetchall():
    print(f"{item_id}\t{status}\t{last_sync}\t{path}")

cursor.close()
conn.close()
```

# Interpreting FileStatus Values
After retrieving rows, map the numeric FileStatus to human-readable states:
- 1 → FILE_ADDED
- 2 → FILE_MODIFIED
- 6 → FILE_DOWNLOADED
- 7 → FILE_UPLOADING
- 8 → FILE_UPLOADED
- 9 → FILE_CONFLICT
- 11 → FILE_ERROR

You can embed the mapping in Python, for example:
```python
status_map = {
    1: "ADDED",
    2: "MODIFIED",
    6: "DOWNLOADED",
    7: "UPLOADING",
    8: "UPLOADED",
    9: "CONFLICT",
   11: "ERROR",
}

print(status_map.get(status, f"UNKNOWN({status})"))
```

# FileStatus Code Definitions
| Code | Name | Description | 
|---   |---   |---|
| 0 | FILE_PROVISIONAL | Initial placeholder record; no action taken yet | 
| 1 | FILE_ADDED | New local file created; awaiting upload to cloud | 
| 2 | FILE_MODIFIED | Existing file changed locally; awaiting upload | 
| 3 | FILE_DELETED_LOCAL | File deleted on device; awaiting deletion in cloud | 
| 4 | FILE_DELETED_REMOTE | File deleted in cloud; awaiting removal locally | 
| 5 | FILE_DOWNLOADING | File download in progress | 
| 6 | FILE_DOWNLOADED | File fully downloaded and stored locally | 
| 7 | FILE_UPLOADING | File upload in progress | 
| 8 | FILE_UPLOADED | File upload completed; cloud version up to date | 
| 9 | FILE_CONFLICT | Conflict detected (name or content); needs manual resolution | 
| 10 | FILE_IGNORED | Explicitly excluded from sync via ignore rules or policies | 
| 11 | FILE_ERROR | Last sync operation failed (e.g., network, permissions) | 
| 12 | FILE_REMOTE_CREATED | New cloud file detected; awaiting local download | 
| 13 | FILE_REMOTE_MODIFIED | Cloud file changed; awaiting local download | 
| 14 | FILE_LOCALLY_DELETED | Permanently removed locally and ignored for upload | 
| 15 | FILE_MIGRATED | File moved or renamed locally and in cloud; status resolved | 


# Mapping to UI Icons
Although the database uses numeric codes, the Windows Files On-Demand UI shows icons instead:
- Code 6 / 8 → Green checkmark
- Code 5 / 7 → Syncing arrows
- Code 1 / 2 / 3 / 12 / 13 → Blue cloud (online-only or pending)
- Code 9 → Red conflict badge
- Code 11 → Red X error badge

Beyond FileStatus
In the same database you’ll often find these related columns:
- ConflictReason – more detail on conflicts
- LastSyncTime – timestamp of the last attempt
- ETag, MD5 – checksums for change detection
- StorageProvider – identifies OneDrive vs. SharePoint

These let you build more advanced diagnostic or reporting scripts.
