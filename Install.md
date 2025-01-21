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
