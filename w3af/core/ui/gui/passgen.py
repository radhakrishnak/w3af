# -*- coding: utf8 -*-
"""
passgen.py

Copyright 2014 Radha Kandula

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import gtk
import string
import random

from w3af.core.controllers.exceptions import BaseFrameworkException
from w3af.core.ui.gui import entries

class Generate(entries.RememberingWindow):
    """Tool to generate random passwords.

    :author: Radha Kandula <rkandula =at= ufl =dot= edu>
    """
    def __init__(self, w3af):
        super(Generate, self).__init__(
            w3af, "passgen", _("w3af - Password Generator"),
            "password_generator")
        self.w3af = w3af
        vpan = entries.RememberingVPaned(w3af, "pane-passwordgenerator")

        # strength hbox
        hbox_1, strength_combo = self._pass_strength()

        # include symbols
        hbox_2, include_symbols = self._include_symbols()

        # include numbers
        hbox_3, include_numbers = self._include_numbers()

        # Generate button
        generate_btn = entries.SemiStockButton(
            "Generate", gtk.STOCK_EXECUTE, _("Generate random password"))
        # lower box
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.panedn = gtk.TextView()

        generate_btn.connect("clicked", self._genpass, strength_combo,\
                             include_symbols, include_numbers, self.panedn)

        vbox = gtk.VBox()
        vbox.pack_start(hbox_1)
        vbox.pack_start(hbox_2)
        vbox.pack_start(hbox_3)
        vbox.pack_start(generate_btn, False, False)

        vpan.pack1(vbox)

        sw.add(self.panedn)
        vpan.pack2(sw)

        self.vbox.pack_start(vpan, padding=10)
        self.show_all()

    def _pass_strength(self):
        hbox = self._hbox_helper()

        # combo box for strength of password
        strength_combo = gtk.combo_box_new_text()
        for i in range(4, 50):
            strength_combo.append_text(str(i))
        strength_combo.set_active(0)

        # Strength label
        label = gtk.Label("Password Strength")

        hbox.pack_start(label, True, False, padding=10)
        hbox.pack_end(strength_combo, True, False, padding=10)
        return hbox, strength_combo

    def _include_symbols(self):
        hbox = self._hbox_helper()

        # Include symbols label
        label = gtk.Label("Include symbols?")

        # symbols
        include_symbols = gtk.CheckButton("( eg. @#$% )")

        hbox.pack_start(label, True, False, padding=10)
        hbox.pack_end(include_symbols, True, False, padding=10)
        return hbox, include_symbols

    def _include_numbers(self):
        hbox = self._hbox_helper()

        # Include symbols label
        label = gtk.Label("Include numbers?")

        # symbols
        include_numbers = gtk.CheckButton("( eg. 123456 )")

        hbox.pack_start(label, True, False, padding=10)
        hbox.pack_end(include_numbers, True, False, padding=10)
        return hbox, include_numbers

    def _hbox_helper(self):
        hbox = gtk.HBox()
        hbox.set_homogeneous(True)
        hbox.set_spacing(30)
        return hbox

    def _genpass(self, widg, combo, symbols, numbers, panedn):
        # since we are starting from 4, add 4
        size = 4 + combo.get_active()
        if symbols.get_active() is True:
            sym = "$$#%@!&*#%@!&*"
        else:
            sym = ""

        if numbers.get_active() is True:
            num = "01234567890123456789"
        else:
            num = ""

        # the character set
        chars = string.ascii_uppercase + string.ascii_lowercase + sym + num
        # generated password
        generated_passwd = ''.join(random.choice(chars) for _ in range(size))
        text_buffer = panedn.get_buffer()
        text_buffer.set_text(generated_passwd)
        panedn.set_buffer(text_buffer)

