import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from ipywidgets import FileUpload
import os
import pandas as pd
import shrinkingcoremodel as scm
import warnings




class Main:
    def __init__(self):
        import warnings
        from widgets import ButtWidg
        from plotting import Plots
        from master import FunctionPlotter, ShrinkingCore
        from bokeh.plotting import figure, show
        from bokeh.io import output_notebook

        warnings.filterwarnings('ignore')
        SM = ShrinkingCore()
        PL=Plots(SM)
        bw=ButtWidg(SM, PL)

        # Create an instance of the class
        self.function_plotter = FunctionPlotter(bw, PL)

class FunctionPlotter:

    def __init__(self, BW, PL):
        #initialise the instance of the button widgets class
        self.inst_bw = BW
        
        #initialise an instance of the plotting class
        self.inst_pl = PL
        
        #initialise an instance of an experimental plot
        self.inst_pl.update_plot('no display')
        
        # create vertical box containing radiobuttons and simulate button
        simbox = widgets.VBox([self.inst_bw.radiobuttons, self.inst_bw.simulate])
        simbox.layout.margin = '38px -75px 0px 0px'
        
        #create vertical box containing the parameter input boxes
        parambox = widgets.VBox([self.inst_bw.output_textboxes])
        parambox.layout.margin = '0px 40px 0px 0px'
        
        #align the simulation and parameter boxes horizontally
        box1 = widgets.HBox([simbox,parambox])
        
        #Arrange top left corner
        topleft = widgets.VBox([widgets.HBox([self.inst_bw.upload, self.inst_bw.dropdown]),box1, 
                                self.inst_pl.plot4_output])
        
        #arange top right corner
        topright = widgets.VBox([self.inst_pl.plot_output, self.inst_bw.clear_exp])
        
        #align top right and top left corner horizontally
        toprow = widgets.HBox([topleft, topright])
        
        # Create an HTML widget for the titles of the 2 main sections
        title_html = widgets.HTML('<h3 style="margin-bottom: -15px; font-family: cursive;font-size: 20px; font-weight: normal;">Model Results</h3>')
        title_html2 = widgets.HTML('<h3 style="margin-bottom: -15px; font-family: cursive;font-size: 20px; font-weight: normal;">Modelling Tool</h3>')
        
        #create a widget which is a line separating sections
        separator_html = widgets.HTML('<div style="border-top: 2px solid #3498db; margin: 10px 0;"></div>')
        
        #aligning the outputs from the simulation in the second row of the GUI
        secondrow = widgets.HBox([self.inst_pl.plot2_output, self.inst_pl.plot3_output])
        
        #Third row is for the fit to experiment button and sliders
        thirdrow = widgets.HBox([self.inst_bw.fit_output, self.inst_bw.slider_output])
        
        anim_butts = widgets.HBox([self.inst_bw.anim_butt_output, self.inst_bw.anim_close_output])
        #Line everything up vertically
        display_layout = widgets.VBox([self.inst_pl.plot5_output, title_html2, separator_html, toprow, title_html, separator_html, secondrow, thirdrow, self.inst_pl.plot6_output, anim_butts])

        #set background colour for GUI
        custom_style = '<style>.widget-container { background-color: #ADD8E6; }</style>'
        display(HTML(custom_style))
        
        #Display everything
        display(display_layout)
        

        
class ShrinkingCore:
    def simulate(self,r,t,p):
        R = int(r)
        T = int(t)
        P = int(p)
        N = 100
        rho_u = 79663.866
        rho_uh3 =  45435.68 #0.045/(100**3)
        b = 0.67
        velocity = 0.5
        rho_h = 0.081
        p = 100000 #1 bar
        a=1.11e-10
        initial_pellet_size = 360
        r = scm.simulation(R,T,P,100,1e-10,rho_h,rho_u,rho_uh3,velocity)
        times = r[0]/1000
        crad = r[1]
        press = r[2]
        outerrad = r[6]
        return times, crad, press, outerrad
   
    def visualise(self,T,O,C,P,t):
        scm.visualise(T,O,C,P,t);
    
    