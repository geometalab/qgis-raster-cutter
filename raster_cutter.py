# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterCutter
                                 A QGIS plugin
 This Plugin allows the export of JPG files with a JPGL Sidecar file.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-04-26
        git sha              : $Format:%H$
        copyright            : (C) 2022 by IFS Institute for Software
        email                : feedback.ifs@ost.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QWhatsThis, QMessageBox
from qgis.core import (QgsProject,
                       QgsMapLayer,
                       QgsCoordinateReferenceSystem,
                       QgsTask,
                       Qgis,
                       QgsRasterLayer,
                       QgsApplication,
                       QgsMessageLog,
                       QgsMessageLog,
                       QgsApplication,
                       QgsProject)

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .raster_cutter_dialog import RasterCutterDialog
from .tooltips import *
import os.path
from osgeo import gdal

import shutil
from urllib.parse import unquote
from PIL import Image  # for reading dimensions of image

MESSAGE_CATEGORY = 'Raster Cutter'

gdal.UseExceptions()


# TODO help button
# TODO imports?
# TODO add QgsSubTask for splitting tasks (report progress?)

class RasterCutter:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RasterCutter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Raster Cutter')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RasterCutter', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/raster_cutter/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Cut out raster layer to...'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Raster Cutter'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start:
            self.first_start = False
            self.dlg = RasterCutterDialog()
            self.dlg.file_dest_field.setFilePath(default_filepath())  # set path to user home
            widget_init(self)

        layers = [layer for layer in QgsProject.instance().mapLayers().values()]
        if layers:  # if there are layers in the project, we can set extent box extents and crs's
            # extentbox init
            self.dlg.extent_box.setOriginalExtent(originalExtent=self.dlg.layer_combobox.currentLayer().extent(),
                                                  originalCrs=self.dlg.layer_combobox.currentLayer().crs())
            self.dlg.extent_box.setOutputCrs(self.dlg.layer_combobox.currentLayer().crs())
            self.dlg.proj_selection.setCrs(self.dlg.layer_combobox.currentLayer().crs())
            self.dlg.extent_box.setCurrentExtent(currentExtent=self.iface.mapCanvas().extent(),
                                                 currentCrs=QgsProject.instance().crs())
        on_lexocad_toggled(
            self)  # check if checkbox is still checked and apply CRS if needed (this ensures CRS is always correct)
        globals()['self'] = self  # for throwing an error without having to pass it around
        add_tooltips(self)
        select_current_layer(self)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            directory_url = self.dlg.file_dest_field.filePath()  # read the file location from form label

            # if file already exists, ask user if he is sure.
            if os.path.exists(directory_url):
                reply = QMessageBox.question(self.dlg, 'Message', "This file already exists. Overwrite?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    return  # TODO is there a way to open the dialog again if "No" is selected

            # get selected layer and check if layer is valid
            selected_layer = self.dlg.layer_combobox.currentLayer()
            data_provider = selected_layer.dataProvider()
            error = pre_process_checks(selected_layer, data_provider)
            if error is not None:
                error_message(error)
                return

            # open the dataset
            src, error = open_dataset(data_provider)
            if error is not None:
                error_message(error)
                return

            # initialize strings
            options_string = ""
            format_string = ""

            # Set format string and format specific settings
            # worldfile is always generated for non georeferenced types, as wished by stefan
            if directory_url.endswith(".jpg"):
                format_string = "JPEG"
                # enables progressive jpg creation (https://gdal.org/drivers/raster/jpeg.html#creation-options)
                # options_string += "-co PROGRESSIVE=ON, "
                options_string += "-co WORLDFILE=YES, "
            elif directory_url.endswith(".png"):
                format_string = "PNG"
                options_string += "-co WORLDFILE=YES, "
            elif directory_url.endswith(".tif"):
                pass

            # create the task which contains the actual calculations and add the task to the task manager, starting it
            # the task is saved in a global variable to avoid a bug (https://gis.stackexchange.com/questions/390652/qgstask-fromfunction-not-running-on-finished-method-unless-an-exception-is-raise)
            globals()['process_task'] = QgsTask.fromFunction("Creating Files", process,
                                                             on_finished=completed,
                                                             src=src,
                                                             iface=self.iface,
                                                             directory_url=directory_url,
                                                             dest_srs=get_target_projection(self).authid(),
                                                             format_string=format_string,
                                                             options_string=options_string,
                                                             extent_win_string=get_extent_win(self),
                                                             generate_lexocad=self.dlg.lexocad_checkbox.isChecked(),
                                                             generate_worldfile=True,
                                                             add_to_map=self.dlg.add_to_map_checkbox.isChecked(),
                                                             target_resolution=get_target_resolution(self))
            QgsApplication.taskManager().addTask(globals()['process_task'])
            QgsMessageLog.logMessage('Starting process...', MESSAGE_CATEGORY, Qgis.Info)


# initializes some connections, only needed once
def widget_init(self):
    self.dlg.layer_combobox.setShowCrs(True)
    self.dlg.lexocad_checkbox.toggled.connect(lambda: on_lexocad_toggled(self))
    self.dlg.resolution_checkbox.toggled.connect(lambda: on_resolution_checkbox_toggled(self))
    on_resolution_checkbox_toggled(self)
    self.dlg.button_box.helpRequested.connect(lambda: help_mode())


# enables/disables x & y resolution spin boxes depending on resolution checkbox state
def on_resolution_checkbox_toggled(self):
    if self.dlg.resolution_checkbox.isChecked():
        self.dlg.x_resolution_box.setEnabled(True)
        self.dlg.y_resolution_box.setEnabled(True)
    else:
        self.dlg.x_resolution_box.setEnabled(False)
        self.dlg.y_resolution_box.setEnabled(False)


def on_lexocad_toggled(self):
    # enables/disables crs selection widget and sets CRS depending on lexocad checkbox state
    if self.dlg.lexocad_checkbox.isChecked():
        self.dlg.proj_selection.setEnabled(False)
        self.dlg.proj_selection.setCrs(QgsCoordinateReferenceSystem.fromEpsgId(2056))
    else:
        self.dlg.proj_selection.setEnabled(True)


# sets the layer dropdown to the selected layer in the QGIS layer manager, if one is selected
def select_current_layer(self):
    if self.iface.layerTreeView().selectedLayers():
        self.dlg.layer_combobox.setLayer(
            self.iface.layerTreeView().selectedLayers()[0])  # select the selected layer in the dropdown


def get_target_projection(self):
    return self.dlg.proj_selection.crs()


# returns extent window as a string for use in gdal
def get_extent_win(self):
    e = self.dlg.extent_box.outputExtent()
    return f"{e.xMinimum()} {e.yMaximum()} {e.xMaximum()} {e.yMinimum()}"


# this is where all calculations actually happen
def process(task, src, iface, directory_url, dest_srs, format_string, extent_win_string, options_string,
            generate_lexocad: bool,
            generate_worldfile: bool, add_to_map: bool, target_resolution: {"x": float, "y": float}):
    # Crop raster, so that only the needed parts are reprojected, saving processing time
    QgsMessageLog.logMessage('Cropping raster (possibly downloading)...', MESSAGE_CATEGORY, Qgis.Info)
    cropped = crop('/vsimem/cropped.tif', src, extent_win_string, dest_srs)
    if task.isCanceled():  # check if task was cancelled between each step
        stopped(task)
        return None

    # reproject and set resolution
    QgsMessageLog.logMessage('Warping raster...', MESSAGE_CATEGORY, Qgis.Info)
    warped = warp('/vsimem/warped.tif', cropped, dest_srs, extent_win_string, target_resolution)
    if task.isCanceled():
        stopped(task)
        return None

    # translate to PNG/JPG and generate worldfile
    QgsMessageLog.logMessage('Translating raster...', MESSAGE_CATEGORY, Qgis.Info)
    translated = translate(directory_url, warped, format_string, options_string)
    if task.isCanceled():
        stopped(task)
        return None

    # close all datasets properly
    src = None
    warped = None
    cropped = None

    # if image should be added to map, get filename (without extension) of the resulting file for layer name
    # and put it into filename. If filename is empty, map will not get added
    file_name = ""
    if add_to_map:
        file = os.path.basename(directory_url)
        file_name_no_ext, file_ext = os.path.splitext(file)
        file_name = f"{file_name_no_ext} cropped"

    manage_files(generate_lexocad, generate_worldfile, directory_url)

    return {"ds": translated, "iface": iface, "path": translated.GetDescription(), "file_name": file_name}


# generate lexocad file and delete worldfile if wanted
def manage_files(generate_lexocad, generate_worldfile, dir_url):
    if not generate_worldfile and not generate_lexocad:
        return
    QgsMessageLog.logMessage("Creating sidecar files", MESSAGE_CATEGORY, Qgis.Info)
    if generate_lexocad:
        generate_lexocad_files(dir_url)
    if not generate_worldfile and generate_lexocad:
        delete_world_file(dir_url)
    delete_tms_xml()  # is only necessary if layer was XYZ, but executes always


# takes the data provider of a layer and opens it as a gdal dataset to be used further
def open_dataset(data_provider):
    if data_provider.name() == "wms":
        # find the type and url parameter in the dataSourceUri string. if either is not found, raise error
        type_string = None
        url = None
        args = data_provider.dataSourceUri().split("&")

        for arg in args:
            if arg.find("type=") is not -1:
                type_string = arg
                type_string = type_string.replace("type=", "")
            if arg.find("url=") is not -1:
                url = arg
                url = url.replace("url=", "")
        if url is None:
            raise Exception("Could not find type parameter in data source")
        # if the wms datasource contains a "type=xyz", a different approach is required
        if type_string == "xyz":
            xml_file_path = generate_tms_xml(url)
            return xml_file_path, None
        else:
            gdal_string = "WMS:" + url + "?" + data_provider.dataSourceUri()


    elif data_provider.name() == "gdal":
        gdal_string = data_provider.dataSourceUri()
    else:
        return None, "Could not open given dataset: %s" % data_provider.name()

    return gdal.Open(gdal_string, gdal.GA_ReadOnly), None


def generate_tms_xml(url):
    model_file_path = get_file_path('xyz_tms.xml')
    temp_file_path = get_file_path('xyz_tms_tmp.xml')
    shutil.copyfile(model_file_path, temp_file_path)
    with open(temp_file_path, 'r', encoding="utf-8") as file:
        data = file.read()
        data = data.replace("URL_HERE", unquote(url).replace('{', '${'))
    with open(temp_file_path, 'w', encoding="utf-8") as file:
        file.write(data)
    return temp_file_path

def delete_tms_xml():
    temp_file_path = get_file_path('xyz_tms_tmp.xml')
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

def get_file_path(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)

def crop(out, src, extent_win_string, extent_srs):
    return gdal.Translate(out, src, options="-projwin %s, -projwin_srs %s, -outsize 2000 0, -r bilinear" % (
        extent_win_string, extent_srs))


def warp(out, src, dst_srs, extent_win_string, target_resolution):
    options_string = "-t_srs %s, " % dst_srs
    if target_resolution['x'] > 0 and target_resolution[
        'y'] > 0:  # if no custom target res is defined, these should both be 0
        options_string += "-tr %s %s" % (target_resolution['x'], target_resolution['y'])
    return gdal.Warp(out, src, options=options_string)


def translate(directory_url, src, format_string, options_string):
    return gdal.Translate(directory_url, src, format=format_string,
                          options=options_string)


# This is called if the task is finished
def completed(exception, result=None):
    if exception is None:
        if result['file_name'] is not "":
            QgsMessageLog.logMessage('Adding file to map...', MESSAGE_CATEGORY, Qgis.Info)
            add_file_to_map(result['iface'], result['path'], result['file_name'])
        QgsMessageLog.logMessage('Done!', MESSAGE_CATEGORY, Qgis.Info)
        globals()['self'].iface.messageBar().pushMessage("Success", f"Layer exported to {result['path']}", level=Qgis.Info)
    else:
        error_message("Exception: {}".format(exception))


def stopped(task):
    error_message('Task "{name}" was canceled'.format(name=task.description()))


# gets the contents of the worldfile and makes some calculations, as a lexocad sidecar file doesn't contain quite the
# same information, but contains all the necessary to calculate the contents.
# After the calculations, a file is created and the contents are written into it
def generate_lexocad_files(directoryUrl):
    worldfile_path = get_worldfile_url_from_dir(directoryUrl)
    with open(worldfile_path, "r") as worldfile:
        lines = worldfile.readlines()
    with Image.open(directoryUrl) as img:
        src_width, src_height = img.size

    width = abs(src_width * float(lines[0]))
    height = abs(src_height * float(lines[3]))
    xMinimum = float(lines[4])
    yMinimum = float(lines[5]) - height
    with open(directoryUrl + "l", 'w') as f:
        f.write(f"{str(xMinimum)}"
                f"{str(yMinimum)}"
                f"str(float(width))"
                f"str(float(height))"
                f"# cadwork swisstopo"
                f"# {str(xMinimum)}  {str(yMinimum)}"
                f"# {str(width)}  {str(height)}"
                f"# projection: EPSG:2056 - CH1903+ / LV95"
                )


# adds the passed file to the map
def add_file_to_map(iface, map_uri, baseName):
    map_uri = map_uri.replace("\\", "/")
    iface.addRasterLayer(map_uri, baseName)


# the default filepath for the file selection dialogue
def default_filepath():
    return os.path.expanduser(f"~{os.path.sep}cropped.png")


def delete_world_file(directory_url):
    worldfile_path = get_worldfile_url_from_dir(directory_url)
    if os.path.exists(worldfile_path):
        os.remove(worldfile_path)


# generates the path where the worldfile can be found when given the path of the raster file
def get_worldfile_url_from_dir(directory_url):
    index = directory_url.find(".")
    if index != -1:
        worldfile_path = directory_url[:index]
        worldfile_path += ".wld"
    else:
        raise Exception("Could not find generate worldfile file name")
    return worldfile_path


# reads input from resolution spin boxes and returns them in a dict
def get_target_resolution(self):
    if self.dlg.resolution_checkbox.isChecked():
        return {'x': self.dlg.x_resolution_box.value(),
                'y': self.dlg.y_resolution_box.value()}
    else:
        return {'x': 0, 'y': 0}


# checks which should be run when clicking on "OK", before calculations are started.
def pre_process_checks(layer, data_provider):
    if layer.type() is QgsMapLayer.VectorLayer:
        return "Provided Layer is a vector layer. Please select a raster layer."
    if not data_provider.isValid():
        return "Provided Layer is not valid."
    if not data_provider.name() == "wms" and not data_provider.name() == "gdal":  # TODO are there more cases?
        return "Please select a valid raster layer."
    return None


# throw an error message for the user
def error_message(message):
    self = globals()['self']
    QgsMessageLog.logMessage(message, MESSAGE_CATEGORY, Qgis.Critical)
    self.iface.messageBar().pushMessage("Error", message, level=Qgis.Critical)
    raise Exception(message)


# enter WhatsThis mode
def help_mode():
    QWhatsThis.enterWhatsThisMode()
    self = globals()['self']
    print(self.dlg.extent_box.currentCrs())
