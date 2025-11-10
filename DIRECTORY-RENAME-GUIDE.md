# 📁 Directory Rename Guide

## Overview

All documentation has been updated to use the new, shorter repository name:

- **OLD**: `project-mc-serv-mc.galion.studio`
- **NEW**: `project-mc.galion.studio`

## ✅ What Was Updated

All references in the following files have been changed:

### Core Documentation
- ✅ README.md
- ✅ LICENSE
- ✅ CONTRIBUTING.md
- ✅ CONTRIBUTORS.md
- ✅ CHANGELOG.md

### Publishing Guides
- ✅ PUBLISHING-GUIDE.md
- ✅ OPEN-SOURCE-READY.md
- ✅ OPEN-SOURCE-SUMMARY.txt
- ✅ REPOSITORY-STRUCTURE.txt
- ✅ PUBLISH-TO-GITHUB.cmd

### New Repository Information

**GitHub URL**: https://github.com/galion-studio/project-mc.galion.studio
**Repository Name**: `project-mc.galion.studio`

## 🔄 How to Rename Your Local Directory

You need to rename the physical directory on your computer to match the new name.

### Option 1: Automated Script (Easiest)

#### Using Command Prompt:
```cmd
RENAME-DIRECTORY.cmd
```

#### Using PowerShell:
```powershell
.\RENAME-DIRECTORY.ps1
```

The script will:
1. Verify you're in the correct directory
2. Ask for confirmation
3. Rename the directory
4. Show success message

### Option 2: Manual Rename

#### Using File Explorer:
1. **Close all files** from this project
2. **Exit any terminals** in this directory  
3. **Navigate to**: `C:\Users\Gigabyte\Documents\`
4. **Right-click** on `project-mc-serv-mc.galion.studio`
5. **Select** "Rename"
6. **Change to**: `project-mc.galion.studio`
7. **Press Enter**

#### Using Command Line:
```cmd
cd C:\Users\Gigabyte\Documents
ren "project-mc-serv-mc.galion.studio" "project-mc.galion.studio"
cd project-mc.galion.studio
```

#### Using PowerShell:
```powershell
cd C:\Users\Gigabyte\Documents
Rename-Item "project-mc-serv-mc.galion.studio" "project-mc.galion.studio"
cd project-mc.galion.studio
```

## ⚠️ Important Notes

### Before Renaming:
- ✅ Close all files in your IDE/editor
- ✅ Exit all command prompts/terminals in this directory
- ✅ Close any applications using files from this directory
- ✅ Save any uncommitted work

### After Renaming:
- ✅ Open the project in the new location
- ✅ Your files are untouched - only the directory name changed
- ✅ All documentation now references the correct name
- ✅ You can proceed with publishing to GitHub

## 📊 New Directory Structure

```
C:\Users\Gigabyte\Documents\
└── project-mc.galion.studio\          ← NEW NAME (shorter!)
    ├── README.md
    ├── LICENSE
    ├── CONTRIBUTING.md
    ├── CODE_OF_CONDUCT.md
    ├── SECURITY.md
    ├── .gitignore
    ├── PUBLISH-TO-GITHUB.cmd          ← Ready to publish!
    ├── RENAME-DIRECTORY.cmd           ← Use this to rename
    ├── RENAME-DIRECTORY.ps1           ← Or this (PowerShell)
    └── ... (all your project files)
```

## 🚀 Publishing After Rename

Once you've renamed the directory:

1. **Create repository on GitHub**:
   - Go to: https://github.com/organizations/galion-studio/repositories/new
   - Name: `project-mc.galion.studio`
   - Public repository

2. **Run the publish script**:
   ```cmd
   cd C:\Users\Gigabyte\Documents\project-mc.galion.studio
   PUBLISH-TO-GITHUB.cmd
   ```

   Or manually:
   ```bash
   cd C:\Users\Gigabyte\Documents\project-mc.galion.studio
   git init
   git add .
   git commit -m "feat: initial commit - Project Titan open source release"
   git remote add origin https://github.com/galion-studio/project-mc.galion.studio.git
   git branch -M main
   git push -u origin main
   git tag -a v1.0.0-alpha -m "Initial alpha release"
   git push origin v1.0.0-alpha
   ```

## 🎯 Why This Change?

The new name is:
- ✅ **Shorter** - Easier to type and remember
- ✅ **Cleaner** - Less redundant
- ✅ **Professional** - Matches your domain name
- ✅ **Consistent** - Aligns with mc.galion.studio

## ✅ Verification Checklist

After renaming, verify:
- [ ] Directory name is `project-mc.galion.studio`
- [ ] You can open files in the new location
- [ ] No errors when accessing the directory
- [ ] All files are intact
- [ ] Ready to publish to GitHub

## ❓ Troubleshooting

### "Access Denied" or "File In Use"
**Solution**: Close all programs using files from this directory:
- IDE/Text editors
- Command prompts/terminals
- File explorers
- Git clients

### "Directory Already Exists"
**Solution**: 
- Check if you already renamed it
- Look in `C:\Users\Gigabyte\Documents\`
- If `project-mc.galion.studio` exists, you're done!

### Can't Find the Directory
**Solution**:
- Navigate to `C:\Users\Gigabyte\Documents\`
- Look for either old or new name
- If you see the new name, renaming was successful

## 📞 Need Help?

If you encounter issues:
1. Close all applications
2. Restart your computer
3. Try the rename again
4. Email: titan@galion.studio

---

## Quick Commands

### Rename (from inside project):
```cmd
RENAME-DIRECTORY.cmd
```

### Navigate to project (after rename):
```cmd
cd C:\Users\Gigabyte\Documents\project-mc.galion.studio
```

### Publish to GitHub (after rename):
```cmd
cd C:\Users\Gigabyte\Documents\project-mc.galion.studio
PUBLISH-TO-GITHUB.cmd
```

---

**Ready to rename?** Just run `RENAME-DIRECTORY.cmd` and follow the prompts! 🚀

