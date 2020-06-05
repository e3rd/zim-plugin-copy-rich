#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import print_function

import logging
from subprocess import check_output
from threading import Thread

from zim.actions import action, get_gtk_actiongroup, ActionMethod
from zim.applications import Application
from zim.gui.mainwindow import MainWindowExtension
from zim.plugins import PluginClass

logger = logging.getLogger('zim.plugins.copy-rich')


class CopyRichPlugin(PluginClass):
    plugin_info = {
        'name': _('Copy Rich'),
        'description': _('''\
Launch by `Edit / Copy Rich HTML`

Note: When text is copied with Copy Rich, it can be only pasted to applications that accept `text/html`,
 ex: e-mail client, document processor. It will not be pasted in a plain text editors like Kate or gedit.

Since migration to Python 3 we lost the feature to copy rich text due to a GTK+ long-term bug.
See more information at https://github.com/zim-desktop-wiki/zim-desktop-wiki/issues/326 and 
https://github.com/e3rd/zim-plugin-copy-rich for repository homepage.
(V1.0)
'''),
        'author': "Edvard Rejthar",
    }

    @classmethod
    def check_dependencies(cls):
        xclip_cmd = ('xclip',)
        pandoc_cmd = ('pandoc',)
        has_xclip = Application(xclip_cmd).tryexec()
        has_pandoc = Application(pandoc_cmd).tryexec()
        return (has_xclip and has_pandoc), [('xclip', has_xclip, True), ('pandoc', has_pandoc, True)]


class RichCopyWindow(MainWindowExtension):

    def __init__(self, plugin, window):
        super().__init__(plugin, window)

    def _add_actions(self, uimanager):
        """ Set up menu items.
            Here we override parent function that adds menu items.

            If we did not override, all the items would be placed directly in Tools, not in Edit.
        """

        def get_actions(obj):
            import inspect
            return inspect.getmembers(obj.__class__, lambda m: isinstance(m, ActionMethod))

        actions = get_actions(self)
        if actions:
            self._uimanager = uimanager
            action_group = get_gtk_actiongroup(self)
            uimanager.insert_action_group(action_group, 0)

            xml = '''
                    <ui>
                    <menubar name='menubar'>
                            <menu action='edit_menu'>
                                <menuitem action='copy_rich'/>                                
                            </menu>
                    </menubar>
                    </ui>
                    '''

            self._uimanager.add_ui_from_string(xml)

    @action(_('Copy Rich _HTML'), accelerator='<ctrl><shift>c')
    def copy_rich(self):
        """ cut current text and call send to tasks dialog """
        self.window.pageview.textview.do_copy_clipboard("Markdown (pandoc)")

        def launch():
            # get markdown from clipboard
            contents = check_output(['xclip', '-selection', 'clipboard', '-o', '-t', 'text/plain']).decode("utf-8")
            # convert to text/html
            contents = check_output(['pandoc', '-f', 'markdown', '-t', 'html'], input=contents, text=True)
            # store text/html to clipboard
            check_output(["xclip", "-sel", "clip", "-t", "text/html", "-f"], input=contents, text=True)
            logger.debug("Copied to Rich.")

        # if pushed immediately without thread clipboard would not be ready.
        # I do not know why, may GTK does it in a loop or something.
        Thread(target=launch).start()
