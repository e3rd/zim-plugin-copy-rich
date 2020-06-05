# Copy Rich plugin for Zim Wiki
Since migration to Python 3 we lost the feature to copy rich text due to a GTK+ long-term bug.
Till it is solved, you may use this plugin to rich copy formatted text from Zim.  
See more information at: https://github.com/zim-desktop-wiki/zim-desktop-wiki/issues/326

Note: When text is copied with Copy Rich, it can be only pasted to applications that accept `text/html`, ex: e-mail client, document processor. It will not be pasted in a plain text editors like Kate or gedit.

## Installation
* `sudo apt install pandoc xclip`
* Put the `copy-rich.py` into the plugins folder
  * something like `%appdata%\zim\data\zim\plugins` in Win, or `~/.local/share/zim/plugins/` in Linux
* You enable the plugin in `Zim / Edit / Preferences / Plugins`: check mark Copy Rich.
* Launch with `Edit / Copy Rich HTML`
* Enjoy

## Supported OS
The plugin is known to work on Linux Ubuntu. I do not think it might work on Windows, however I would be glad for any experience you post in the issues.