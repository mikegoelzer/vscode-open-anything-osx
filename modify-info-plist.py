#!/usr/bin/env python3
import shutil
import plistlib
import subprocess
import os

def main():
    plist_path = '/Applications/Visual Studio Code.app/Contents/Info.plist'
    backup_path = plist_path + '-bak'
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Info.plist')
    
    # Step 1: Backup the original Info.plist
    shutil.copy(plist_path, backup_path)
    
    # Step 2: Copy the Info.plist to the desktop
    shutil.copy(plist_path, desktop_path)
    
    # Step 3: Load the plist and modify it
    with open(desktop_path, 'rb') as fp:
        plist_data = plistlib.load(fp)
    
    new_element = """
    <dict>
        <key>CFBundleTypeExtensions</key>
        <array>
            <string>*</string>  <!-- Wildcard for all files -->
        </array>
        <key>CFBundleTypeName</key>
        <string>Public Text File</string>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>LSItemContentTypes</key>
        <array>
            <string>public.text</string>
            <string>public.plain-text</string>
            <string>public.script</string>
            <string>public.source-code</string>
            <string>public.data</string>
        </array>
        <key>LSHandlerRank</key>
        <string>Alternate</string>
    </dict>
    """
    
    # Convert the string to a dictionary (assuming the string is XML formatted correctly)
    import xml.etree.ElementTree as ET
    element_tree = ET.fromstring(new_element)
    new_dict = plistlib.loads(ET.tostring(element_tree), fmt=plistlib.FMT_XML)
    # Append the new element to the CFBundleDocumentTypes array
    if 'CFBundleDocumentTypes' in plist_data:
        plist_data['CFBundleDocumentTypes'].append(new_dict)
    else:
        plist_data['CFBundleDocumentTypes'] = [new_dict]
    
    # Save the modified plist back to the desktop copy
    with open(desktop_path, 'wb') as fp:
        plistlib.dump(plist_data, fp)
    
    # Step 4: Open VS Code with both the original and modified plist files
    subprocess.run(['open', '-a', 'Visual Studio Code', plist_path, desktop_path])
    
    # Step 5: Give user instructions and wait for confirmation
    input("Please copy the contents of the modified Info.plist on the desktop to the original Info.plist in the application bundle, save the file, and then press Enter to continue...")
    
    # Step 6: Delete the desktop copy of Info.plist
    os.remove(desktop_path)
    
    # Step 7: Run the Launch Services refresh command as nop
    subprocess.run([
        '/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister',
        '-kill', '-r', '-domain', 'local', '-domain', 'system', '-domain', 'user'
    ])

if __name__ == '__main__':
    main()