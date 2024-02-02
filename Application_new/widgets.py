import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from ipywidgets import FileUpload, interact
import os
import pandas as pd
import shrinkingcoremodel as scm
import warnings
from io import BytesIO


class ButtWidg:
    def __init__(self, SM, PL):
        
        #initialise an instance of plotting and shrinking core class
        self.inst_sm = SM
        self.inst_pl = PL
        
        #initialise all widgets
        self.upload_button()
        self.dropdown_button()
        self.radiobuttons()
        self.seemore()
        self.simulate()
        #self.de_slider()
        self.slider_output = widgets.Output()
        self.fit_output = widgets.Output()
        

        # Create an Output widget to hold the textboxes
        self.output_textboxes = widgets.Output()

        
        self.radiobuttons.observe(self.display_textboxes, names='value')
        
        self.micro_symbol = "\u03BC"


    #This is the dropdown button for experimental data selection        
    def dropdown_button(self):
        # find the current working directory
        self.current_directory = os.getcwd()
        #define a button widget where the options are the data files
        self.dropdown = widgets.Dropdown(
            options=sorted(self.get_file_list(self.current_directory+'/stakebake_data')),
            value = 'BM90.csv')
        # Observe the widgets to track changes
        self.dropdown.observe(self.inst_pl.update_plot, names='value')
        #self.dropdown.observe(lambda change: self.inst_pl.update_plot(change, 0), names='value')
        
    def update_dropdown(self, filename):
        #self.dropdown_button()
        file_list = sorted(self.get_file_list(self.current_directory+'/stakebake_data'))
        filtered_list = [x for x in file_list if x != '.DS_Store']
        self.dropdown.options = filtered_list
        self.dropdown.value = filename

    
    #This function is used to get the file names from data directory
    def get_file_list(self, folder_path):
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files
        

    #This button displays every parameter for the shrinking core sim.
    def seemore(self):
        self.seemore = widgets.Button(description='See all parameters')
        # Set the event handler for the button click
        self.seemore.on_click(self.toggle_plot_text_boxes)

   # Function which displays more parameters if seemore clicked and gets back to the plot
    def toggle_plot_text_boxes(self, b):
        with self.inst_pl.plot4_output:
            clear_output(wait=True)
            if self.seemore.description == 'Hide all parameters':
                self.inst_pl.smallfig()
                self.seemore.description = 'See all parameters'
            else:
                self.tb1 = widgets.Text(value = '79663.866', layout=widgets.Layout(width='100px'))
                rho ="\u03C1"
                desc1 = widgets.Label(f'{rho}U, '+ '$molm^{-3}$', 
                                      layout=widgets.Layout(width='150px'))
                
                self.tb2 = widgets.Text(value = '45435.68', layout=widgets.Layout(width='100px'))
                desc2 = widgets.Label(f'{rho}UH3, '+ '$molm^{-3}$', 
                                      layout=widgets.Layout(width='150px'))
                
                self.tb3 = widgets.Text(value = '0.67',layout=widgets.Layout(width='100px'))
                desc3 = widgets.Label('b', layout=widgets.Layout(width='150px'))
                
                self.tb4 = widgets.Text(value = '0.5', layout=widgets.Layout(width='100px'))
                desc4 = widgets.Label('Velocity $\mu m s^{-1}$', layout=widgets.Layout(width='150px'))
                
                self.tb5 = widgets.Text(value = '0.081', layout=widgets.Layout(width='100px'))
                desc5 = widgets.Label(f'{rho} H, '+'$molm^{-3}$', 
                                      layout=widgets.Layout(width='150px'))
                
                self.tb6 = widgets.Text(value = '1.11e-10',layout=widgets.Layout(width='100px'))
                desc6 = widgets.Label('a', layout=widgets.Layout(width='150px'))
                
                
                w1  = widgets.HBox([desc1, self.tb1])
                w2  = widgets.HBox([desc2, self.tb2])
                w3  = widgets.HBox([desc3, self.tb3])                
                w4  = widgets.HBox([desc4, self.tb4])                
                w5  = widgets.HBox([desc5, self.tb5])                
                w6  = widgets.HBox([desc6, self.tb6])      
                
                lhs = widgets.VBox([w1, w2,w3])
                rhs = widgets.VBox([w4,w5,w6])
                lhs.layout.margin_right = '150px'
                rhs.layout.margin_left = '150px'
                
                lay = widgets.HBox([lhs,rhs])
                display(lay)
                self.seemore.description = 'Hide all parameters'     

    #Button which runs simulation            
    def simulate(self):
        self.simulate = widgets.Button(description='Simulate')
        self.simulate.on_click(self.on_simulate_click)
    
    #Fetches the users values from textboxes and passes them to plot3 where sim is run
    def on_simulate_click(self,b):
        self.inst_pl.plot4_output.clear_output()
        try:
            r = self.textbox1.value
            t = self.textbox2.value
            p = self.textbox3.value
           
            model = self.radiobuttons.value
            if model == 'Shrinking Core':
                mod = 1
            elif model == 'Stakebake':
                mod = 2
            elif model == 'CK':
                mod = 3
         
            self.inst_pl.update_plot3(r,t,p,model)
            self.inst_pl.plot2(r,t,p, model)
            self.de_slider()
            self.fit()
        except:
            with self.inst_pl.plot4_output:
                self.inst_pl.plot4_output.clear_output()
                print('please select a model')
        
        
    #This allows for a selection between simulatory models
    def radiobuttons(self):
        self.radiobuttons = widgets.RadioButtons(
            options=['Shrinking Core', 'Stakebake', 'CK'],
            value=None,  # No default selection
            description='Select Model:',
            disabled=False)
    
    #Button to upload own data - needs work
    def upload_button(self):
        self.upload = FileUpload(accept='.csv', multiple=True)
        self.upload.observe(self.on_upload, names='_counter')
        
        
   # Handle CSV file upload event
    def on_upload(self,change):
        target_directory = self.current_directory + '/stakebake_data/'
        for filename, file_info in self.upload.value.items():
            content = file_info['content']
            target_path = os.path.join(target_directory, filename)

            # Check if the file is a CSV file
            if filename.endswith('.csv'):
                # Read the CSV content and save to target directory
                df = pd.read_csv(BytesIO(content))
                df.to_csv(target_path, index=False)
                
        self.update_dropdown(filename)
    

    #Dispplays textboxes where simulation parameters can be inserted      
    def display_textboxes(self, change):
        self.output_textboxes.clear_output(wait=True)

        if self.radiobuttons.value:  
            # Create multiple textboxes
            self.textbox1 = widgets.Text(value='300', description='',layout=widgets.Layout(width='60px'))
            self.textbox1.observe(self.check_rad_value, names='value')
            self.textbox2 = widgets.Text(value='90', description='',layout=widgets.Layout(width='60px'))
            self.textbox2.observe(self.check_temp_value, names='value')
            self.textbox3 = widgets.Text(value='10000', description='',layout=widgets.Layout(width='60px'))
            self.textbox3.observe(self.check_pressure_value, names='value')
             # Create descriptions with longer text
            desc1 = widgets.Label(f'Initial radius ({self.micro_symbol}m)', layout=widgets.Layout(width='150px'))
            desc2 = widgets.Label('Temperature (K)', layout=widgets.Layout(width='150px'))
            desc3 = widgets.Label('Pressure (Pa)', layout=widgets.Layout(width='150px'))
            
            butt = self.seemore

            # Display the textboxes and descriptions
            with self.output_textboxes:
                display(widgets.HBox([desc1, self.textbox1]))
                display(widgets.HBox([desc2, self.textbox2]))
                display(widgets.HBox([desc3, self.textbox3]))
                display(widgets.HBox([butt]))

        else:
            # Uncheck the checkbox and clear the output when it's unchecked
            self.checkbox.value = False
            self.close_textboxes(None)
            
    def check_rad_value(self, change):
        try:
            if float(change.new)<0 or float(change.new)>1000:
                with self.inst_pl.plot4_output:
                    print(f"Check radius is between 0 and 1000 {self.micro_symbol}m")
            else:
                with self.inst_pl.plot4_output:
                    self.inst_pl.plot4_output.clear_output()
                    
        except ValueError:
                with self.inst_pl.plot4_output:
                    self.inst_pl.plot4_output.clear_output()
                    print("Enter only numeric radii")
                    
    def check_temp_value(self, change):
        try:
            if float(change.new)<0 or float(change.new)>1000:
                with self.inst_pl.plot4_output:
                    print("Check temperature is between 0 and 1000 Kelvin")
            else:
                with self.inst_pl.plot4_output:
                    self.inst_pl.plot4_output.clear_output()
                    
        except ValueError:
                with self.inst_pl.plot4_output:
                    self.inst_pl.plot4_output.clear_output()
                    print("Enter only numeric temperatures")
                    
    def check_pressure_value(self, change):    
        try:
            if float(change.new)<0 or float(change.new)>1000000:
                with self.inst_pl.plot4_output:
                    print("please use reasonable pressure value in Pa")
            else:
                with self.inst_pl.plot4_output:
                    self.inst_pl.plot4_output.clear_output()
                    
        except ValueError:
                with self.inst_pl.plot4_output:
                    self.inst_pl.plot4_output.clear_output()
                    print("please enter only numeric pressure values")
    def de_slider(self):
        self.slider_output.clear_output(wait=True)
        with self.slider_output:
            self.slider = widgets.FloatSlider(
                value=0.0,   # Initial value
                min=-10.0,    # Minimum value
                max=10.0,     # Maximum value
                step=0.1,     # Step size
                description='Diffusivity:',  # Label for the slider
                orientation='horizontal')  # Orientation of the slider (horizontal or vertical)
            display(self.slider)
            
    def fit(self):
        self.fit_output.clear_output(wait=True)
        self.fit_button = widgets.Button(description='fit to experimental plot') 
        self.fit_button.on_click(self.on_fitting_click)
        with self.fit_output:            
            display(self.fit_button)
            
    def on_fitting_click(self, b):
        self.inst_pl.update_plot(self.dropdown.value, 100)