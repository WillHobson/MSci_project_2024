import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import patches as pt

nx = 2
ny = 2

fig,ax = plt.subplots()
ax.set_aspect(1)

def init():
    #plot initialisation
    ax.set_xlim(0,2)
    ax.set_ylim(0,1)
    ax.get_yaxis().set_ticks([])
    ax.get_xaxis().set_ticks([])
    # initialize a circle
    centre_x = 0.5
    centre_y = 0.5
    patch = ax.add_patch(plt.Circle((centre_x,centre_y),0.42))
    ax.add_patch(plt.Circle((centre_x,centre_y),0.48, color='black'))
    ax.set_title('Visualisation of a shrinking core simulation', fontsize=15)


    ax.set_facecolor('lavender')
    return []

def animate(i):
    #clear previous frame
    ax.clear()
    ax.set_facecolor('lavender')
    ax.set_title('Visualisation of a shrinking core simulation', fontsize=15)

    #set plot parameters for new frame
    ax.set_xlim(0,2)
    ax.set_ylim(0,1)
    ax.get_yaxis().set_ticks([])
    ax.get_xaxis().set_ticks([])

    
    #circle parameters
    centre_x = 0.5
    centre_y = 0.5


    white_patch = pt.Patch(color='ghostwhite', label = 'H, conc at surface, ca')
    blue_patch = pt.Patch(color='blue', label='U')
    red_patch = pt.Patch(color='red', label='UH3')
    black_patch = pt.Patch(color='black', label='UO2')
    choc = pt.Patch(color='lavender', label = 'H, feed conc, cb')
    plt.legend(handles=[red_patch, blue_patch,black_patch, choc, white_patch], loc=7,
               facecolor='lightyellow',
               edgecolor='white')
    
    ax.annotate("R0", xy=(0.5, 0.5), xytext=(0.98, 0.49),arrowprops=dict(arrowstyle="]->", color='yellow'))

    
    #for Hydrogen breaking through oxide layer
    if i<70:
        ax.add_patch(plt.Circle((centre_x,centre_y),0.6, color='ghostwhite'))

        #draw red circle
        ax.add_patch(plt.Circle((centre_x,centre_y),0.45, color='red'))
        
        #decreasing radii value to iterate through
        someRadii = np.linspace(0.45,0,1001)
        
        #list to store circle
        patches = []
        
        #adding oxide layer
        patches.append(ax.add_patch(plt.Circle((centre_x,centre_y),someRadii[i], color='black')))
        
        #add U core
        ax.add_patch(plt.Circle((centre_x,centre_y),0.42))
        
        ax.annotate("Rc", xy=(0.5, 0.5), xytext=(0.47, 0.947),arrowprops=dict(arrowstyle="]->", color='yellow'))
        
        return patches
    
    #Hydrogen has broken through oxide layer
    else:
        ax.add_patch(plt.Circle((centre_x,centre_y),0.6, color='ghostwhite'))

        #draw hydride layer
        ax.add_patch(plt.Circle((centre_x,centre_y),0.45, color='red'))
        someRadii = np.linspace(0.4185,0,201)
        patches = []
        patches.append(ax.add_patch(plt.Circle((centre_x,centre_y),someRadii[i-70])))
        ax.annotate("Rc", xy=(0.5, 0.5), xytext=(0.465, someRadii[i-70]+0.53),arrowprops=dict(arrowstyle="]->", color='yellow'))
        return patches

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=1000, interval=50, blit=True)
plt.show()
