def add_tooltips(self):
    section_tips(self)
    input_layer_tips(self)
    extent_box_tips(self)
    file_dest_tips(self)
    checkbox_tips(self)
    crs_tips(self)
    resolution_tips(self)
    resampling_algorithm_tips(self)
    add_to_map_tooltips(self)


def section_tips(self):
    input_section_tooltip = '<p>A raster layer - i.e. an internet map image service (WMS, WMTS, XYZ/TMS) - or a local file (GeoTIFF format). A list of map services is available e.g. in the \"Quick Map Services\" plugin. Make sure your QGIS project has a matching CRS.</p>'
    input_section_whatsthis = input_section_tooltip + '<p>Select the raster data to cut and set the extent of the output raster with the two widgets below.</p>'
    output_section_tooltip = '<p>A raster file in an image format (PNG, JPG, GeoTIFF) with a certain smaller extent, possibly with a sidecar file (World File etc.) and eventually reprojected into a CRS and with certain resolution.</p>'
    output_section_whatsthis = output_section_tooltip
    self.dlg.input_section_label.setToolTip(input_section_tooltip)
    self.dlg.input_section_label.setToolTip(input_section_whatsthis)
    self.dlg.output_section_label.setToolTip(output_section_tooltip)
    self.dlg.output_section_label.setToolTip(output_section_whatsthis)


def input_layer_tips(self):
    input_layer_tooltip = '<p>Select the layer which should be saved as a image. Needs to be a raster layer.</p>'
    input_layer_whatsthis = input_layer_tooltip + '<p>Displayed in the list is the layer name, as well as the CRS (Coordinate Reference System) of the layer. The layer will be automatically reprojected into the selected CRS (see "CRS" further down).</p>'
    self.dlg.layer_label.setToolTip(input_layer_tooltip)
    self.dlg.layer_label.setWhatsThis(input_layer_whatsthis)
    self.dlg.layer_combobox.setWhatsThis(input_layer_tooltip)
    self.dlg.layer_combobox.setToolTip(input_layer_whatsthis)


def extent_box_tips(self):
    extent_box_tooltip = '<p>Define the extent which will be cut.</p>'
    extent_box_whatsthis = '<p><span style=" font-weight:600;">Current Layer Extent</span> sets the extent to match the currently selected layer, to ensure the whole layer will be visible on the exported image.</p><p><span style=" font-weight:600;">Calculate from Layer</span> allows you to set the extent to the extents of any other layer in your project.</p><p><span style=" font-weight:600;">Map Canvas Extent</span> sets the extent to your map canvas, e.g. what you currently see. This allows for easy cropping of a part of your layer.</p>'
    self.dlg.extent_box.setToolTip(extent_box_tooltip)
    self.dlg.extent_box.setWhatsThis(extent_box_whatsthis)


def file_dest_tips(self):
    file_dest_tooltip = '<p>Here, one can define where the output image as well as possible sidecar files should be saved.</p>'
    file_dest_whatsthis = file_dest_tooltip + '<p>Open the file explorer by clicking on the button on the right with the three dots. Here, you can select the directory where the file(s) should be saved. Enter a file name without the file extension.</p><p>Choose whether to save the image as a .png or a .jpg in the dropdown. This will also affect the lexocad sidecar file, which will have the same file name as the image, but with a .jpgl/.pngl instead of the .jpg/.png ending.</p>'
    self.dlg.file_dest_label.setToolTip(file_dest_tooltip)
    self.dlg.file_dest_label.setWhatsThis(file_dest_whatsthis)
    self.dlg.file_dest_field.setWhatsThis(file_dest_whatsthis)
    self.dlg.file_dest_field.setToolTip(file_dest_tooltip)


def checkbox_tips(self):
    # worldfile_checkbox_tooltip = '<p>When checked, a <span style=" font-weight:600;">.wld</span> sidecarfile will be created, which allows the image to be georeferenced in many applications.</p>'
    # worldfile_checkbox_whatsthis = worldfile_checkbox_tooltip
    lexocad_checkbox_tooltip = '<p>When checked, a <span style=" font-weight:600;">.jpgl</span> or <span style=" font-weight:600;">.pngl</span> sidecarfile will be created, which allows the image to be imported into Lexocad. Output CRS will be set to <span style=" font-weight:600;">EPGS:2056</span> as required.</p>'
    lexocad_checkbox_whatsthis = lexocad_checkbox_tooltip
    # self.dlg.worldfile_checkbox.setToolTip(worldfile_checkbox_tooltip)
    # self.dlg.worldfile_checkbox.setWhatsThis(worldfile_checkbox_whatsthis)
    self.dlg.lexocad_checkbox.setToolTip(lexocad_checkbox_tooltip)
    self.dlg.lexocad_checkbox.setWhatsThis(lexocad_checkbox_whatsthis)


def crs_tips(self):
    proj_selection_tooltip = '<p>Set the Coordinate Reference System, which will be used in the worldfile.</p>'
    proj_selection_whatsthis = proj_selection_tooltip + '<p><span style=" font-weight:600;">This will not reproject the qgis layer.</span> It will only affect the output raster image (if the new projection causes the raster to be warped) and the worldfile.</p><p><span style=" font-weight:600;">If lexocad files (.jpgl/.pngl) are to be created, <span style=" font-weight:600;">EPGS:2056</span> will automatically be selected and cannot be changed. This is due to the fact that lexocad only supports this projection. </p>'
    self.dlg.proj_selection.setToolTip(proj_selection_tooltip)
    self.dlg.proj_selection.setWhatsThis(proj_selection_whatsthis)
    self.dlg.proj_selection_label.setWhatsThis(proj_selection_whatsthis)
    self.dlg.proj_selection_label.setToolTip(proj_selection_tooltip)


def resolution_tips(self):
    resolution_tooltip = '<p>Set output file resolution (in target georeferenced units). The resolution defines the dimensions of a pixles in map units, for x and y. </p>'
    resolution_whatsthis = resolution_tooltip + '<p>For example, for CH1903+ / LV95, the map unit is a meter. This means that a resolution of x: 0.5 equals two pixels for each meter on the map on the horizontal axis. </p><p>It is generally advisable to set the x and y resolution to the same value. </p><p>If a image cannot be saved because of a too large file size, increase the x and y values.</p>'
    self.dlg.resolution_checkbox.setToolTip(resolution_tooltip)
    self.dlg.resolution_checkbox.setWhatsThis(resolution_whatsthis)
    self.dlg.x_resolution_label.setToolTip(resolution_tooltip)
    self.dlg.x_resolution_label.setWhatsThis(resolution_whatsthis)
    self.dlg.y_resolution_label.setToolTip(resolution_tooltip)
    self.dlg.y_resolution_label.setWhatsThis(resolution_whatsthis)
    self.dlg.x_resolution_box.setToolTip(resolution_tooltip)
    self.dlg.x_resolution_box.setWhatsThis(resolution_whatsthis)
    self.dlg.y_resolution_box.setToolTip(resolution_tooltip)
    self.dlg.y_resolution_box.setWhatsThis(resolution_whatsthis)


def resampling_algorithm_tips(self):
    nearest_neighbour_tooltip = '<p>Suitable for categorical/classified <span style=" font-weight:600;">mono or full color</span> data. Pixel neighbor value is used without modification</p>'
    nearest_neighbour_whatsthis = nearest_neighbour_tooltip + ""

    cubic_spline_tooltip = '<p>Suitable for continuous <span style=" font-weight:600;">gray tone</span> data. Values are interpolated</p>'
    cubic_spline_whatsthis = cubic_spline_tooltip + ''

    resampling_algorithm_tooltip = '<p>Determines how values are interpolated between known data points. This affects how sharp the exported image looks.</p>'
    resampling_algorithm_whatsthis = resampling_algorithm_tooltip + f'<p><span style=" font-weight:600;">Nearest Neighbour</span></p>{nearest_neighbour_tooltip}<p><span style=" font-weight:600;">Cubic Spline</span></p>{cubic_spline_tooltip}'

    self.dlg.resampling_algorithm_label.setToolTip(resampling_algorithm_tooltip)
    self.dlg.resampling_algorithm_label.setWhatsThis(resampling_algorithm_whatsthis)

    self.dlg.nearest_neighbour_radio_button.setToolTip(nearest_neighbour_tooltip)
    self.dlg.nearest_neighbour_radio_button.setWhatsThis(nearest_neighbour_whatsthis)

    cubic_spline_tooltip = '<p>Suitable for continuous <span style=" font-weight:600;">gray tone</span> data. Values are interpolated</p>'
    cubic_spline_whatsthis = cubic_spline_tooltip + ""
    self.dlg.cubic_spline_radio_button.setToolTip(cubic_spline_tooltip)
    self.dlg.cubic_spline_radio_button.setWhatsThis(cubic_spline_whatsthis)


def add_to_map_tooltips(self):
    add_to_map_tooltip = '<p>When checked, the generated raster image will be added to the current project as a new layer after the image has been generated.</p>'
    add_to_map_whatsthis = add_to_map_tooltip + '<p>If checked, a sidecar file with the ending ".aux.xml" will be generated. This file lets QGIS and other applications know in which CRS the coordinates in the worldfile are defined.</p>'
    self.dlg.add_to_map_checkbox.setToolTip(add_to_map_tooltip)
    self.dlg.add_to_map_checkbox.setWhatsThis(add_to_map_whatsthis)
