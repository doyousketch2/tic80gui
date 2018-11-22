[![OpenSource](https://img.shields.io/badge/Open-Source-orange.svg)](https://github.com/doyousketch2)  [![PythonVersions](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)  [![License](https://img.shields.io/badge/license-GPL--v3-lightgrey.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)  [![Git.io](https://img.shields.io/badge/Git.io-fpZwp-233139.svg)](https://git.io/fpZwp)  


# tic80gui
Quick little frontend for TIC-80  

![image](https://raw.githubusercontent.com/doyousketch2/tic80gui/master/Screenshot.png)  

Requirements:  Python3 and GTK  
---

- [ ] Linux:  
    `sudo apt-get install libgtk-3-dev python-gi-dev gir1.2-gdkpixbuf-2.0`  

- [ ] Mac:  
    http://macappstore.org/gtk  
    http://macappstore.org/gdk-pixbuf  
    http://macappstore.org/gobject-introspection  

- [ ] Win:  
    https://www.python.org/downloads  
    https://www.gtk.org/download/windows.php  

- [x] You'll also need TIC-80 to get any use out of this little app:  
    https://github.com/nesbox/TIC-80  
    https://tic.computer  

To execute your Python3 script:  
---

- [ ] `./tic80gui.py`  
- [ ] `python3 -m tic80gui.py`  
- [ ] `py -3 tic80gui.py`  

---

**side note:**  to quickly open .tic files,  
many Linux file browsers let you specify custom commands.  
I believe Thunar, PCManFM, Nautilus, Caja all do.  

You'll want to specify the dir where your tic80 bin is located,  
but it would be something like this:  
    `~/Programming/TIC-80/bin/tic80 %f -skip`
