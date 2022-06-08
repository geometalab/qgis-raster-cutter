def add_tooltips(self):
    resolution_tips(self)

def resolution_tips(self):
    resolution_tooltip = "<p>Set output file resolution (in target georeferenced units). The resolution defines the dimensions of a pixles in map units, for x and y. </p>"
    resolution_whatsthis = resolution_tooltip + "<p>For example, for CH1903+ / LV95, the map unit is a meter. This means that a resolution of x: 0.5 equals two pixels for each meter on the map on the horizontal axis. </p><p>It is generally advisable to set the x and y resolution to the same value. </p><p>If a image cannot be saved because of a too large file size, increase the x and y values.</p>"
    self.dlg.res_label.setToolTip(resolution_tooltip)
    self.dlg.res_label.setWhatsThis(resolution_whatsthis)
    self.dlg.x_res_label.setToolTip(resolution_tooltip)
    self.dlg.x_res_label.setWhatsThis(resolution_whatsthis)
    self.dlg.y_res_label.setToolTip(resolution_tooltip)
    self.dlg.y_res_label.setWhatsThis(resolution_whatsthis)
    self.dlg.x_res_box.setToolTip(resolution_tooltip)
    self.dlg.x_res_box.setWhatsThis(resolution_whatsthis)
    self.dlg.y_res_box.setToolTip(resolution_tooltip)
    self.dlg.y_res_box.setWhatsThis(resolution_whatsthis)

def checkbox_tips(self):
    lexocad_checkbox_tooltip = '<p>When checked, a <span style=" font-weight:600;">.jpgl</span> or <span style=" font-weight:600;">.pngl</span> sidecarfile will be created, which allows the image to be imported into Lexocad. Output CRS will be set to <span style=" font-weight:600;">EPGS:2056</span> as required.</p>'
    worldfile_checkbox_tooltip = '<p>When checked, a <span style=" font-weight:600;">.wld</span> sidecarfile will be created, which allows the image to be georeferenced in many applications.</p>'
    lexocad_checkbox_whatsthis = lexocad_checkbox_tooltip
    worldfile_checkbox_whatsthis = worldfile_checkbox_tooltip
    self.dlg.worldfile_checkbox.setToolTip(worldfile_checkbox_tooltip)
    self.dlg.worldfile_checkbox.setWhatsThis(worldfile_checkbox_whatsthis)
    self.dlg.worldfile_checkbox.setToolTip(lexocad_checkbox_tooltip)
    self.dlg.worldfile_checkbox.setWhatsThis(lexocad_checkbox_whatsthis)
