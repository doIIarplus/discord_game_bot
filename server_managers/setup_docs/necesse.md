The server configuration file is named "server.cfg" and is located at C:\Users\Ya\AppData\Roaming\Necesse\cfg

The world configuration file is named "worldSettings.cfg" and is located at C:\Users\Ding\AppData\Roaming\Necesse\saves\YourWorldNamehere.zip

The save data is the .zip named according to the world name, and is located at C:\Users\Dong\AppData\Roaming\Necesse\saves\

The server logs are found at C:\Users\Chongus\AppData\Roaming\Necesse\logs
This looks like a guide for setting up a **Necesse Dedicated Server**. Here is the text formatted using Markdown:

-----

# Instructions are for Windows, double check the URLs and whatnot for the Mac/Linux versions instead

-----

## 🎮 Setting Up a Necesse Dedicated Server

### ⬇️ Downloading Server Files

Downloading the server files can be performed in three different ways:

#### Through Steam

1.  Navigate to your **Steam library** and filter for **tools**.
2.  Identify **'Necesse Dedicated Server'** and click **install**.

#### Through SteamCMD

1.  See Valve's developer wiki for how to download and install SteamCMD: **`https://developer.valvesoftware.com/wiki/SteamCMD`**
2.  Once installed, run **SteamCMD** by double-clicking the `steamcmd.exe` in the installation folder.
3.  In the SteamCMD window, type in the following:
    ```
    login anonymous
    ```
4.  To change where the dedicated server is installed, use the command:
    ```
    force_install_dir C:\Necesse
    ```
    *That would tell SteamCMD to install the Necesse Dedicated server files to a folder called Necesse on your PC's C drive.*
5.  Next, download the server files to the specified folder by typing:
    ```
    app_update 1169370 validate
    ```
6.  When the process has completed, it will say **"Success\! App '1169370' fully installed."** You can then close Steam CMD by typing:
    ```
    quit
    ```

#### Through Download

  * You can also download the server files located at **`https://necessegame.com/server/`**

-----

### 🛡️ Port Forwarding

The protocol and default port for Necesse is **UDP** and **port 14159**. You will need to open these ports on your **router** and **server's Windows Firewall**.

#### Router

1.  Login to your router.
2.  Navigate to your router's **port forwarding section**.
3.  Create the port forward entries in your router.

#### Windows Firewall

1.  Navigate to **Control Panel → System and Security → Windows Firewall**.
2.  Select **"Advanced settings"** and highlight **"Inbound Rules"** in the left pane.
3.  Right-click Inbound Rules and select **"New Rule..."**
4.  Click the **"Port"** circle and click **"Next"**.
5.  Select the protocol (**UDP**) and the port number (if you've followed this example, it would be **14159**) in the **"Specific local ports:"** text box and click **Next**.
6.  Select **"Allow the connection"** in the next window and click **Next**.
7.  Select the network type as you see fit and click **Next**.
8.  Name the rule **"Necesse Server"** and click **Finish**.

#### Port Forwarding Testing

  * Test that your ports are forwarded correctly by entering your public IP address and the port number on this site: **`https://portchecker.co/`**

> **Note:** Port checkers sometimes report false negatives. If you have done everything correct and you can see your server listening on a `netstat` scan, it may be worth checking if people can join anyway.

-----

### 🚀 Running the Server

1.  To run the server, navigate to wherever you installed the server files (if you've followed the exact steps from this guide, it would be `C:\Necesse`).
2.  Locate the file called **"StartServer.bat"** and **double-click it**. A new window will appear; this is the dedicated server program.
3.  You will be asked to name the world; type your desired world name and click **"Enter"**.
4.  If you want custom server options, type in **"y"** and click **"Enter"**. If you do not, type **"n"** and click **"Enter"**.
5.  It will ask you to specify the **"host port"**. This is the port we forwarded earlier, so type in **`14159`** and then click **"Enter"**.
6.  Then, it will ask for the amount of **player slots**. Type in a number between 1 and 250, and click **"Enter"**.
7.  Next, it will ask whether you want a **server password**. If you do, type it in (don't type anything if you don't want a password), and click **"Enter"**.
8.  It will ask you to specify a **custom spawn island**. Leave blank for random or enter a custom spawn island in the format: `<x>,<y>` and click **"Enter"**.
9.  Then you'll be asked to specify a **spawn seed**. Enter a random number or leave blank for random, and click **"Enter"**.
10. You'll then be asked to choose whether to **spawn the guide house**. Type in **"y"** for yes or **"n"** for no, and click **"Enter"**.
11. Click **"Enter"** one final time to start up the server.

> **To stop the server:** Leave the dedicated server program window open to keep the server running. When you want to shut down the server, type **`quit`** into the text box and click **"Enter"** or click the **X** at the top right of the window.

-----

### 🤝 How to Join the Server

1.  Run the game from Steam.
2.  Click **"Multiplayer"**.
3.  Click **"Add Server"**.
4.  Type a name that will help you remember the server in the **"Name"** field.
5.  Type your **public IPv4 address** (which can be found here: **`https://whatismyipaddress.com/`**) in the **"IP address"** field.
      * *Note: IPs in the `192.168.0.0-192.168.255.255` range are private, and others will not be able to connect to it unless they're on the same network.*
6.  Type your server port, which if you've followed this guide is **`14159`**, in the **"Port Number"** field.
7.  Click **"Add"**.
8.  Your server will now appear in the **"Multiplayer"** menu. **Double-click it to join** (or click it once then click "Join Server").
