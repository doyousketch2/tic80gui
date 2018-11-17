#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""  notes  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

##  tic80gui.py                                    Dec 2018
##  @ Doyousketch2
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html

"""  requirments  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

##  sudo apt-get install python-gi-dev libgtk-3-dev gir1.2-gdkpixbuf-2.0

##  you'll need TIC-80 to get any use out of this little app.
##  github.com/nesbox/TIC-80
##  tic.computer

"""  credit  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

##  logo is from TIC-80 repository
##  github.com/nesbox/TIC-80/tree/master/docs/logo

"""  modules  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

import sys                             ##  for exit command
import os                         ##  path.join and whatnot
import gi                         ##  GObject Introspection
gi .require_version( 'Gtk', '3.0' )

from gi .repository import Gtk            ##  Gnome toolkit
from gi .repository import GdkPixbuf       ##  for the icon
import subprocess as sp           ##  commandline processes
import configparser

"""  vars  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

default_width  = 500
default_height  = -1  ##  whatever's clever

ver  = '2018.1217'  ##  Year.MonthDay
appname  = os .path .basename(__file__)

config  = configparser .ConfigParser()
configfile  = 'settings.cfg'

config ['location']  = {  ##  supply default values
    'tic80' : '~/Programming/TIC-80/bin/tic80',
    'tic80pro' : '~/Programming/TIC-80/bin/tic80pro',
    'cart' : '~/Programming/TIC-80/carts/BestGameEver.tic'  }

config ['toggle']  = {  ##  supply default values
    'surf' : 'False',
    'nosound' : 'False',
    'fullscreen' : 'False',
    'skip' : 'True'  }

config .read( configfile )  ##  load configfile, if exists

whereAt  = os .path .realpath(__file__)
cwd,  module  = os .path .split( whereAt )

"""  functs  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def save():
    with open( configfile,  'w' ) as cfg:
        config .write( cfg )
save()


def loc( key ):
    return config ['location'] [ key ]


def boo( key ):
    return config ['toggle'] .getboolean( key )


class MainWindow( Gtk .Window ):
    def __init__( self ):
        Gtk .Window .__init__( self,  title = appname )

        self .tic80  = loc( 'tic80' )
        self .tic80pro  = loc( 'tic80pro' )
        self .cart  = loc( 'cart' )

        horiz_box, vert_box  = 0, 1
        spacing  = 0
        container  = Gtk .Box .new( vert_box,  spacing )

        top_row  = Gtk .Box .new( horiz_box,  spacing )

        self .surf_toggle  = Gtk .CheckButton( label = 'Surf' )
        self .surf_toggle .connect( 'toggled',  self .surf_toggled )
        self .surf_toggle .set_active( boo( 'surf' )  )

        self .nosound_toggle  = Gtk .CheckButton( label = 'Nosound' )
        self .nosound_toggle .connect( 'toggled',  self .nosound_toggled )
        self .nosound_toggle .set_active( boo( 'nosound')  )

        self .full_toggle  = Gtk .CheckButton( label = 'Fullscreen' )
        self .full_toggle .connect( 'toggled',  self .full_toggled )
        self .full_toggle .set_active( boo( 'fullscreen' )  )

        self .skip_toggle  = Gtk .CheckButton( label = 'Skip intro' )
        self .skip_toggle .connect( 'toggled',  self .skip_toggled )
        self .skip_toggle .set_active( boo( 'skip' )  )

        about_button  = Gtk .Button( label = 'About' )
        about_button .connect( 'clicked',  self .about_clicked )

        main_row  = Gtk .Box .new( horiz_box,  spacing )

        select_button  = Gtk .Button( label = 'Select Game' )
        select_button .connect( 'clicked',  self .select_clicked )

        self .game_name  = Gtk .Label( self .cart )

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        left_column  = Gtk .Box .new( vert_box,  spacing )

        locate_button  = Gtk .Button( label = 'Locate TIC-80' )
        locate_button .connect( 'clicked',  self .locate_clicked )

        logoname  = os .path .join( cwd, 'logo16.png' )
        tic80logo  = Gtk .Image .new_from_file( logoname )

        launch_button  = Gtk .Button(  label = 'Launch TIC-80',
                                       image = tic80logo  )
        launch_button .connect( 'clicked',  self .launch_clicked )

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        right_column  = Gtk .Box .new( vert_box,  spacing )

        locate_pro_button  = Gtk .Button( label = 'Locate Pro' )
        locate_pro_button .connect( 'clicked',  self .locate_pro_clicked )

        logoname  = os .path .join( cwd, 'logo16.png' )
        tic80prologo  = Gtk .Image .new_from_file( logoname )

        launch_pro_button  = Gtk .Button(  label = 'Launch Pro',
                                           image = tic80prologo  )

        launch_pro_button .connect('clicked',  self .launch_pro_clicked )

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self .add( container )
        container .pack_start( top_row,  True,  True,  0 )

        top_row .pack_start( self .surf_toggle,  True,  True,  0 )
        top_row .pack_start( self .nosound_toggle,  True,  True,  0 )
        top_row .pack_start( self .full_toggle,  True,  True,  0 )
        top_row .pack_start( self .skip_toggle,  True,  True,  0 )

        top_row .pack_start( about_button,  True,  True,  0 )

        container .pack_start( main_row,  True,  True,  0 )

        main_row .pack_start( left_column,  True,  True,  0 )
        left_column .pack_start( locate_button,  True,  True,  0 )
        left_column .pack_start( launch_button,  True,  True,  0 )

        main_row .pack_start( select_button,  True,  True,  0 )

        main_row .pack_start( right_column,  True,  True,  0 )
        right_column .pack_start( locate_pro_button,  True,  True,  0 )
        right_column .pack_start( launch_pro_button,  True,  True,  0 )

        container .pack_start( self .game_name,  True,  True,  8 )

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def about_clicked( self,  widget ):
        logoname  = os .path .join( cwd, 'logo48.png' )
        tic80logo  = GdkPixbuf .Pixbuf .new_from_file( logoname )

        popup  = Gtk .AboutDialog(  self,  logo  = tic80logo,
                     authors  = [ 'Eli Innis',
                                  'in-game:  Sketch2',
                                  'twitter:  @Doyousketch2',
                                  'email:  Doyousketch2 @ yahoo.com' ],
                     copyright  = 'Copyright 2018',
                     license_type  = Gtk .License .GPL_3_0,
                     version  = ver  )
        Gtk .Dialog .run( popup )
        popup .destroy()

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def surf_toggled( self,  widget ):
        value  = str( self .surf_toggle .get_active() )
        config ['toggle'] [ 'surf' ]  = value
        save()


    def nosound_toggled( self,  widget ):
        value  = str( self .nosound_toggle .get_active() )
        config ['toggle'] [ 'nosound' ]  = value
        save()


    def full_toggled( self,  widget ):
        value  = str( self .full_toggle .get_active() )
        config ['toggle'] [ 'fullscreen' ]  = value
        save()


    def skip_toggled( self,  widget ):
        value  = str( self .skip_toggle .get_active() )
        config ['toggle'] [ 'skip' ]  = value
        save()

    ##  center  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def select_clicked( self,  widget ):
        dialog  = Gtk .FileChooserDialog(
                title = 'Select cart',  parent = None,
                action = Gtk .FileChooserAction .OPEN,
                buttons = ( Gtk .STOCK_CANCEL,  Gtk .ResponseType .CANCEL,
                            Gtk .STOCK_OK,  Gtk .ResponseType .OK )  )

        folder1,  tail  = os .path .split( loc('cart') )
        folder2,  tail  = os .path .split( loc('tic80') )
        folder3,  tail  = os .path .split( loc('tic80pro') )

        if os .path .exists( folder1 ):
            dialog .set_current_folder( folder1 )
        elif os .path .exists( folder2 ):
            dialog .set_current_folder( folder2 )
        elif os .path .exists( folder3 ):
            dialog .set_current_folder( folder3 )

        file_filter  = Gtk .FileFilter()
        file_filter .set_name( '*.tic' )
        file_filter .add_pattern( '*.[Tt][Ii][Cc]' )
        dialog .add_filter( file_filter )

        file_filter  = Gtk .FileFilter()
        file_filter .set_name( 'All Files' )
        file_filter .add_pattern( '*' )
        dialog .add_filter( file_filter )

        response  = dialog .run()
        if response == Gtk .ResponseType .OK:
            self .cart  = dialog .get_filename()
            self .game_name .set_text( self .cart )

            config ['location'] [ 'cart' ]  = self .cart
            save()

        dialog .destroy()

    ##  left  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def locate_clicked( self,  widget ):
        dialog  = Gtk .FileChooserDialog(
                title = 'Locate TIC-80',  parent = None,
                action = Gtk .FileChooserAction .OPEN,
                buttons = ( Gtk .STOCK_CANCEL,  Gtk .ResponseType .CANCEL,
                            Gtk .STOCK_OK,  Gtk .ResponseType .OK )  )

        folder1,  tail  = os .path .split( loc('tic80') )
        folder2,  tail  = os .path .split( loc('tic80pro') )
        folder3,  tail  = os .path .split( loc('cart') )

        if os .path .exists( folder1 ):
            dialog .set_current_folder( folder1 )
        elif os .path .exists( folder2 ):
            dialog .set_current_folder( folder2 )
        elif os .path .exists( folder3 ):
            dialog .set_current_folder( folder3 )

        response  = dialog .run()
        if response == Gtk .ResponseType .OK:
            self .tic80  = dialog .get_filename()
            config ['location'] [ 'tic80' ]  = self .tic80
            save()

        dialog .destroy()


    def launch_clicked( self,  widget ):
        commandline  = [ self .tic80,  self .cart ]

        if self .surf_toggle .get_active():
            commandline .append( '-surf' )

        if self .nosound_toggle .get_active():
            commandline .append( '-nosound' )

        if self .full_toggle .get_active():
            commandline .append( '-fullscreen' )

        if self .skip_toggle .get_active():
            commandline .append( '-skip' )

        sp .call( commandline )

    ##  right  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def locate_pro_clicked( self,  widget ):
        dialog  = Gtk .FileChooserDialog(
                title = 'Locate TIC-80 Pro',  parent = None,
                action = Gtk .FileChooserAction .OPEN,
                buttons = ( Gtk .STOCK_CANCEL,  Gtk .ResponseType .CANCEL,
                            Gtk .STOCK_OK,  Gtk .ResponseType .OK )  )

        folder1,  tail  = os .path .split( loc('tic80pro') )
        folder2,  tail  = os .path .split( loc('tic80') )
        folder3,  tail  = os .path .split( loc('cart') )

        if os .path .exists( folder1 ):
            dialog .set_current_folder( folder1 )
        elif os .path .exists( folder2 ):
            dialog .set_current_folder( folder2 )
        elif os .path .exists( folder3 ):
            dialog .set_current_folder( folder3 )

        response  = dialog .run()
        if response == Gtk .ResponseType .OK:
            self .tic80pro  = dialog .get_filename()
            config ['location'] [ 'tic80pro' ]  = self .tic80pro
            save()

        dialog .destroy()


    def launch_pro_clicked( self,  widget ):
        commandline  = [ self .tic80pro,  self.cart ]

        if self .surf_toggle .get_active():
            commandline .append( '-surf' )

        if self .nosound_toggle .get_active():
            commandline .append( '-nosound' )

        if self .full_toggle .get_active():
            commandline .append( '-fullscreen' )

        if self .skip_toggle .get_active():
            commandline .append( '-skip' )

        sp .call( commandline )

"""  main  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

win  = MainWindow()
win .connect( 'destroy',  Gtk .main_quit )

win .set_default_size( default_width,  default_height )
win .set_position( Gtk .WindowPosition .CENTER_ALWAYS )

win .set_title( appname )
win .show_all()
Gtk .main()

"""  eof  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

