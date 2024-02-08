import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML, Image
from ipywidgets import FileUpload
import os
import pandas as pd
import shrinkingcoremodel as scm
import warnings
from bokeh.plotting import figure, show
from bokeh.io import output_notebook

class Plots:
    def __init__(self, SM):
        #Use the shrinking core simulation class
        self.inst_sm = SM
        
        #create widgets to hold plots 1,2,3
        #self.plot2_output = widgets.Output(layout={'width': '500px', 'height': '405px'})
        #self.plot3_output = widgets.Output(layout={'width': '500px', 'height': '405px'})
        self.plot2_output = widgets.Output()
        self.plot3_output = widgets.Output()
        self.plot_output = widgets.Output(layout={'width': '420px', 'height': '405px'})
        self.plot4_output = widgets.Output(layout={'width': '420px', 'height': '110px'})
        self.plot5_output = widgets.Output(layout={'width': '900px', 'height': '50px' })
        self.plot6_output = widgets.Output()
        self.model_descriptions()

 

    def smallfig(self):
        with self.plot4_output:
            plt.figure(facecolor='#ADD8E6')  # Set figure size to match widget size
            plt.plot([0, 1], [1, 1], color='#ADD8E6')
            plt.axis('off')  # Turn off axis for a cleaner appearance
            plt.show()
            
    def model_descriptions(self):
        with self.plot5_output:
            
            text = 'The three models presented here are all derived from different principles and have different assumptions. The following links will provide a summary and mathematical derivation of each, providing the relevant literature: SCM, SB, CK'

            styled_text = (
                '<p style="font-family: Arial, Helvetica, sans-serif; font-size: 16px;text-align: justify;">'
                f'{text}'
                '</p>')

            # Display the HTML-formatted text
            display(HTML(styled_text))

            
            
        #function to update the plot showing simulation radius vs time        
    def update_plot3(self, r,t,p, model):
        self.plot3_output.clear_output(wait=True)
        self.plot3_output.layout.height = '405px'
        self.plot3_output.layout.width = '500px'

        #self.plot3_output = widgets.Output(layout={'width': '500px', 'height': '405px'})
        #clear previous display
        
        #on the cleared display plot ..
        output_notebook(hide_banner=True)
        p3 = figure(title= f'CORE RADIUS vs TIME (R={r} T={t} P={p})',
                    width = 400, height = 400, x_axis_label = "time (s)", 
                    y_axis_label = 'Radius of Uranium core (um)')
        p3.min_border_bottom = 120
        p3.sizing_mode = 'scale_both'
        
        with self.plot3_output:
            #new SCM simulation using inputted values
            sim = self.inst_sm.simulate(r,t,p)
            x = sim[0]
            y = sim[1]
            y_outer = sim[3]
            p3.line(x, y, legend_label = 'Core radius (SCM)')
            p3.line(x, y_outer, legend_label = 'Particle radius (SCM)', line_color='red')
            p3.legend.location = "bottom_left"
            show(p3)  
          
            
            
    def plot2(self, r,t,p, model):
        self.plot2_output.clear_output(wait=True)
        self.plot2_output.layout.height = '405px'
        self.plot2_output.layout.width = '500px'
        if model == 1:
            print('model 1')
            sim = self.inst_sm.simulate(r,t,p)
        elif model == 2:
            print('model 2')
            sim = self.inst_sm.simulate(r,t,p)
        else: 
            sim = self.inst_sm.simulate(r,t,p)
            
        output_notebook(hide_banner=True)
        p2 = figure(title= f'PROGRESSION vs TIME (R={r} T={t} P={p})',
                    width = 400, height = 400,
                    x_axis_label = "time (s)",
                    y_axis_label = "Reaction progression")
        
        p2.min_border_bottom = 120
        p2.sizing_mode = 'scale_both'

        with self.plot2_output:
            x = sim[0]
            y = (sim[2]-np.min(sim[2]))
            y= ((y/np.max(y))-1)*-1
            self.save_fitting_data(x,y)
            
            p2.line(x, y, legend_label = 'SCM')
            p2.legend.location = "bottom_right"
            show(p2)         
            
            
            
    def update_plot(self, change, value=None):
        if type(change)==str and value==None:
            print('going to clear plot')
            p1 = figure(title= f'Experimental data display')
            self.plot_output.clear_output(wait=True)

            with self.plot_output:
                x=[]
                y=[]
                p1.line(x,y)
                output_notebook(hide_banner=True)
                show(p1)

        else:
            if type(change)==str:
                selected_function = change
            else:
                selected_function = change['new']
            self.plot_output.clear_output(wait=True)
            data = pd.read_csv('stakebake_data/'+selected_function)
            output_notebook(hide_banner=True)
            p1 = figure(title= f'Plot of {selected_function}')#, width = 400, height = 400)
            p1.min_border_bottom = 40
            p1.sizing_mode = 'scale_both'
            data.columns = ['x', ' y']
            with self.plot_output:
                x = data['x']
                y=data[' y']
                if value==100:
                    p1.line(self.xfit, self.yfit, line_color='red', legend_label='model fit')


                p1.circle(x, y, legend_label = selected_function)
                p1.legend.location = "bottom_right"
                show(p1)        

            
            
            
    def save_fitting_data(self, xfit, yfit):
        self.xfit = xfit
        self.yfit = yfit
        
    def create_animation(self, r,t,p,model):
        self.plot6_output.layout.height = '405px'
        self.plot6_output.layout.width = '950px'
        with self.plot6_output:
            print('CREATING ANIMATION - please wait')
        res = self.inst_sm.simulate(r,t,p)
        TIME = res[0]
        ORAD = res[3]
        CRAD = res[1]
        PRES = res[2]
        title = f'Rad={r}_Temp={t}_Press={p}'
        self.inst_sm.visualise(TIME, ORAD, CRAD, PRES, title);

        

    def update_animation(self,title):
        self.plot6_output.clear_output(wait=True)
        with open(title+".gif", "rb") as file:
            image = file.read()

        play = widgets.Image(
            value=image,
            format='gif'
        )

        with self.plot6_output:
            display(play)
