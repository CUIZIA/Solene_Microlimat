### Step 1: Install VirtualBox and Create a Virtual Machine

**Helpful link:** [OpenClassrooms - Install Linux in a Virtual Machine](https://openclassrooms.com/fr/courses/43538-reprenez-le-controle-a-laide-de-linux/37630-installez-linux-dans-une-machine-virtuelle)

#### Instructions:
1. **Install VirtualBox**  
   - Download and install the latest version of VirtualBox for your operating system (Windows, Mac, or Linux).

2. **Create a New Virtual Machine**  
   - Open VirtualBox and create a new virtual machine.
   - Allocate sufficient **RAM** (stay in the green zone but close to the yellow for optimal performance) and assign a virtual hard disk size of at least **40GB**.

3. **Insert the `.iso` File**  
   - Before starting the virtual machine, insert the `.iso` file into the virtual CD drive in the machine settings.
   - Start the virtual machine and proceed with the installation of the `.iso` file:
     - When the screen turns pink, select the **second option**: `Install`.
     - During the installation, choose **Erase disk and install custom**. This will only affect the virtual machine, not your primary computer.

4. **Complete the Installation**  
   - Once the installation is finished, the Solene operating system should be installed.  
   - Note: The desktop window might appear very small at this stage—this is normal and will be addressed in Step 3.

5. **Remove the `.iso` File**  
   - After installation, the `.iso` file is no longer needed in the optical drive.  
   - Normally, VirtualBox will automatically eject the `.iso` if the installation was successful. If not, you can manually remove it in the **Settings > Storage** section of VirtualBox.

### Step 2: Change the Password  

**Helpful link:** [Ask Ubuntu - Reset a Lost Administrative Password](https://askubuntu.com/questions/24006/how-do-i-reset-a-lost-administrative-password#24024)  

#### Instructions:  
1. **Access Recovery Mode**  
   - To "boot" into recovery mode, press the **Shift** key (or **F2/F12** for specific systems like Sihem's) after the BIOS screen appears—this happens as soon as the virtual machine starts.  
   - Select the **Recovery Mode** option from the boot menu.  

2. **Remount the File System**  
   - In recovery mode, you need to remount the file system with write permissions. Open the terminal (you’ll be in a root shell by default) and enter:  
     ```bash
     mount -o remount,rw /
     ```  

3. **Change the Password**  
   - Change the password for the "Solene" user by typing:  
     ```bash
     passwd solene
     ```
   - Enter the new password when prompted. For example:  
     ```plaintext
     Enter new UNIX password: IRSTV-solene
     Retype new UNIX password: IRSTV-solene
     ```
   - If successful, you’ll see the message:  
     ```plaintext
     passwd: password updated successfully
     ```  

4. **Reboot the Virtual Machine**  
   - Exit recovery mode and reboot the virtual machine.  
   - If the boot process fails, you might need to try accessing recovery mode multiple times.  

### Step 3: Add "Guest Additions"  

**Helpful links:**  
1. [OpenClassrooms - Install Linux in a Virtual Machine](https://openclassrooms.com/fr/courses/43538-reprenez-le-controle-a-laide-de-linux/37630-installez-linux-dans-une-machine-virtuelle)  
2. [Linuxize - Install VirtualBox Guest Additions on Ubuntu](https://linuxize.com/post/how-to-install-virtualbox-guest-additions-in-ubuntu/)  

#### Instructions:  
1. **Start the Virtual Machine**  
   - Power on your virtual machine.

2. **Insert Guest Additions CD**  
   - **Option 1:** The Guest Additions CD may appear directly on the desktop as a virtual CD.  
   - **Option 2:** If not, go to the **Devices** menu in VirtualBox and select **Insert Guest Additions CD Image**.

3. **Mount the Guest Additions CD**  
   - Right-click on the Guest Additions CD icon and select **Mount**.

4. **Run the Installation Script**  
   - Open a terminal and navigate to the Guest Additions directory:  
     ```bash
     cd /media/solene/VBox_GAs_6.1.16/
     ```
   - Run the installation script using the following command:  
     ```bash
     sudo sh VBoxLinuxAdditions.run
     ```

5. **Reboot the Virtual Machine**  
   - Restart the virtual machine to apply the changes.  

#### Expected Outcome:  
- After restarting, the virtual machine’s display should automatically adjust to the size of your PC screen.  
- If it doesn’t, go to the **VirtualBox Settings** and modify the display settings to enable proper screen scaling.  

### Step 4: Share a Folder  

**Helpful links:**  
1. [IdéaGeek - How to Mount a Shared Folder on VirtualBox (Debian)](https://idealogeek.fr/comment-monter-dossier-partage-virtualbox-debian/)  
2. [Numelion - Create a Shared Folder for VirtualBox](https://www.numelion.com/creer-un-dossier-de-partage-pour-virtualbox.html)  

#### Instructions:  

1. **Create a Shared Folder**  
   - On your host system, create a folder on your **Desktop** or in the **Documents** directory. Name it "Partage".  

2. **Configure the Shared Folder in VirtualBox**  
   - Open the **VirtualBox interface** and click on the **Settings** tool for the virtual machine.  
   - Navigate to the **Shared Folders** section.  
   - Click the **+** icon at the top-right corner to add a shared folder.  
   - Select the folder you created ("Partage") and set the following options:  
     - **Permanent**: Checked  
     - **Auto-Mount**: Checked  

3. **Start the Virtual Machine**  
   - Boot up the virtual machine.  

4. **Mount the Shared Folder**  
   - Open a terminal in the virtual machine and run the following commands:  
     - Create a mount point:  
       ```bash
       sudo mkdir -p /media/Partage
       ```  
     - Mount the shared folder:  
       ```bash
       sudo mount -t vboxsf Partage /media/Partage
       ```  
     - Add the user to the `vboxsf` group:  
       ```bash
       sudo usermod -a -G vboxsf solene
       ```  

5. **Restart if Necessary**  
   - If the shared folder is not working, try restarting both the virtual machine and your host PC.  

#### Notes:  
- Once the shared folder is set up, it will be permanently accessible, allowing you to store files in the shared folder and avoid memory issues on the virtual machine.

Id: 
solene

MotPass:
IRSTV-solene
