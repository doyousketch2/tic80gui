#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""  notes  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

##  tic80gui.py                                     Dec 2018
##  @ Doyousketch2
##  GNU GPLv3                  gnu.org/licenses/gpl-3.0.html

"""  modules  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

import sys                             ##  for exit command
import os                         ##  path.join and whatnot
import gi                         ##  GObject Introspection
gi .require_version( 'Gtk', '3.0' )
from gi .repository import Gtk
import subprocess as sp           ##  commandline processes
import pickle                  ## serialize data for saving

"""  vars  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

default_width  = 500
default_height  = -1  ##  whatever's clever

ver  = 1.7
appname  = os .path .basename(__file__)

"""  functs  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

class MainWindow( Gtk .Window ):
    def __init__(self):
        Gtk .Window .__init__( self,  title = appname )

        self .tic80  = []
        self .tic80pro  = []
        self .cart  = '~/Programming/TIC-80/carts/BestGameEver.tic'

        horiz_box, vert_box  = 0, 1
        spacing  = 0
        container  = Gtk .Box .new( vert_box,  spacing )

        top_row  = Gtk .Box .new( horiz_box,  spacing )

        self .surf_toggle  = Gtk .CheckButton( label = 'Surf' )
        self .surf_toggle .connect( 'toggled',  self .surf_toggled )

        self .nosound_toggle  = Gtk .CheckButton( label = 'Nosound' )
        self .nosound_toggle .connect( 'toggled',  self .nosound_toggled )

        self .fullscreen_toggle  = Gtk .CheckButton( label = 'Fullscreen' )
        self .fullscreen_toggle .connect( 'toggled',  self .fullscreen_toggled )

        self .skip_toggle  = Gtk .CheckButton( label = 'Skip intro' )
        self .skip_toggle .connect( 'toggled',  self .skip_toggled )
        self .skip_toggle .set_active( True )

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

        launch_button  = Gtk .Button( label = 'Launch TIC-80' )
        launch_button .connect( 'clicked',  self .launch_clicked )

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        right_column  = Gtk .Box .new( vert_box,  spacing )

        locate_pro_button  = Gtk .Button( label = 'Locate Pro' )
        locate_pro_button .connect( 'clicked',  self .locate_pro_clicked )

        launch_pro_button  = Gtk .Button( label = 'Launch Pro' )
        launch_pro_button .connect('clicked',  self .launch_pro_clicked )

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self .add( container )
        container .pack_start( top_row,  True,  True,  0 )

        top_row .pack_start( self .surf_toggle,  True,  True,  0 )
        top_row .pack_start( self .nosound_toggle,  True,  True,  0 )
        top_row .pack_start( self .fullscreen_toggle,  True,  True,  0 )
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

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def about_clicked( self,  widget ):
        popup  = Gtk .AboutDialog(  self,  logo  = None,
                                    authors  = [ 'Eli Innis',
                                                 'in-game:  Sketch2',
                                                 'twitter:  @Doyousketch2',
                                                 'email:  Doyousketch2 @ yahoo.com' ],
                                    copyright  = 'Copyright 2018',
                                    license_type  = Gtk .License .GPL_3_0,
                                    version  = ver  )
        Gtk .Dialog .run( popup )
        popup .destroy()


    def surf_toggled( self,  widget ):
        print( 'toggled surf '
               +str( self .surf_toggle .get_active() ) )


    def nosound_toggled( self,  widget ):
        print( 'toggled nosound '
                +str( self .nosound_toggle .get_active() ) )


    def fullscreen_toggled( self,  widget ):
        print( 'toggled fullscreen '
               +str( self .fullscreen_toggle .get_active() ) )


    def skip_toggled( self,  widget ):
        print( 'toggled skip '
               +str( self .skip_toggle .get_active() ) )


    def select_clicked( self,  widget ):
        print( 'Select cart' )

        dialog  = Gtk .FileChooserDialog(
                  title = 'Select cart',  parent = None,
                  action = Gtk .FileChooserAction .OPEN,
                  buttons = ( Gtk .STOCK_CANCEL, Gtk .ResponseType .CANCEL,
                              Gtk .STOCK_OK, Gtk .ResponseType .OK  )  )

        response  = dialog .run()
        if response == Gtk .ResponseType .OK:
            self .cart  = dialog .get_filename()
            print( 'Found a cart: ' +self .cart )
            self .game_name .set_text( self .cart )
        dialog .destroy()


    def locate_clicked( self,  widget ):
        print( 'Locate TIC-80' )

        dialog  = Gtk .FileChooserDialog(
                  title = 'Locate TIC-80',  parent = None,
                  action = Gtk .FileChooserAction .OPEN,
                  buttons = ( Gtk .STOCK_CANCEL, Gtk .ResponseType .CANCEL,
                              Gtk .STOCK_OK, Gtk .ResponseType .OK  )  )

        response  = dialog .run()
        if response == Gtk .ResponseType .OK:
            self .tic80  = dialog .get_filename()
            print( 'Found tic80: ' +self .tic80 )
        dialog .destroy()


    def locate_pro_clicked( self,  widget ):
        print( 'Locate TIC-80 Pro' )

        dialog  = Gtk .FileChooserDialog(
                  title = 'Locate TIC-80 Pro',  parent = None,
                  action = Gtk .FileChooserAction .OPEN,
                  buttons = ( Gtk .STOCK_CANCEL, Gtk .ResponseType .CANCEL,
                              Gtk .STOCK_OK, Gtk .ResponseType .OK  )  )

        response  = dialog .run()
        if response == Gtk .ResponseType .OK:
            self .tic80pro  = dialog .get_filename()
            print( 'Found tic80pro: ' +self .tic80pro )
        dialog .destroy()


    def launch_clicked( self,  widget ):
        print( 'Launching TIC-80' )
        commandline  = [ self .tic80,  self .cart ]

        if self .surf_toggle .get_active():
            commandline .append( '-surf' )

        if self .nosound_toggle .get_active():
            commandline .append( '-nosound' )

        if self .fullscreen_toggle .get_active():
            commandline .append( '-fullscreen' )

        if self .skip_toggle .get_active():
            commandline .append( '-skip' )

        sp .call( commandline )


    def launch_pro_clicked( self,  widget ):
        print( 'Launching TIC-80 Pro' )
        commandline  = [ self .tic80pro,  self.cart ]

        if self .surf_toggle .get_active():
            commandline .append( '-surf' )

        if self .nosound_toggle .get_active():
            commandline .append( '-nosound' )

        if self .fullscreen_toggle .get_active():
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
