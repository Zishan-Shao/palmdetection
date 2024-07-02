import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

output_dir = "Palm_Slices/tree_not_palm"
input_dir = "Palms_FullDataSet/Cropped_Images"

X_split = 6
Y_split = 6

def Palm_Spliting(input_dir, output_dir, X_Split, Y_Split):
    x = X_Split
    y = Y_Split
    
    ## Get file names array from input_dir
    img_list = os.listdir(input_dir)
        
    # we have done 2100 to 2300
    for file_name in img_list[300:350]:
        ## obtain img from file
        path=os.path.join(input_dir, file_name)
        image_name = os.path.basename(path) ## get name
        image_name = image_name.split(".")[0] ## remove the .tif from name
        
        print(image_name)
        
        
        #if ("Bottlebrush" in file_name):
        #    continue
        
        img = Image.open(path)
        # Use to show the uncut figure
        #fig1 = plt.figure()
        #plt.imshow(img)
        
        m, n = img.size
        step_x = m/x
        step_y = n/y

        ## Convert pillow into numpy array
        arr_img = np.array(img)
        arr_img = arr_img[:, :, 0:3]

        ## Create the grid of images
        fig, axs = plt.subplots(x, y)

        ## This is the 2d array of images that we will use to store the x*y cut pieces of images
        patches = [axs[i, j].imshow(np.zeros((int(step_x), int(step_y), 3))) for i in range(x) for j in range(y)]
        
        ## Whenever we detect a click then it creates a chain of events
        def on_click(event):
            if event.inaxes:
                for i in range(x):
                    for j in range(y):
                        if event.inaxes == axs[i, j]:
                            if patches[i*y+j] is not None:
                                ## Remove previously highlighted rectangle patch
                                if hasattr(patches[i*y+j], '_highlight_patch'):
                                    patches[i*y+j]._highlight_patch.remove()
                                    del patches[i*y+j]._highlight_patch
                                else:
                                    # add new rectangle patch around selected patch
                                    patch_img = patches[i*y + j].get_array()
                                    
                                    patch_height, patch_width = patch_img.shape[:2]

                                    highlight_rect = Rectangle((0, 0), patch_width - 1, patch_height - 1, fill=False, edgecolor='red')
                                    axs[i, j].add_patch(highlight_rect)
                                    axs[i, j].set_axis_off()
                                    patches[i*y+j]._highlight_patch = highlight_rect
                            fig.canvas.draw_idle()
                            break

        def on_key_press(event):
            if event.key == 'd':
                for i, patch in enumerate(patches):
                    if patch is not None and hasattr(patch, '_highlight_patch'):
                        # remove the red highlight
                        patch._highlight_patch.remove()
                        del patch._highlight_patch
                        
                        # save the patch image without the red highlight
                        if not (os.path.exists(output_dir)):
                            os.makedirs(output_dir)
                        patch_img = patch.get_array()
                        path = os.path.join(output_dir, f'{image_name_unique}_{i}.png')
                        plt.imsave(path, patch_img)
                plt.close()

        fig.canvas.mpl_connect('button_press_event', on_click)
        fig.canvas.mpl_connect('key_press_event', on_key_press)

        itr = 0
        for i in range(0, x):
            for j in range(0, y):
                from_x = int(i*step_x)
                to_x = int((i+1)*step_x)
                from_y = int(j*step_y)
                to_y = int((j+1)*step_y)

                patch = arr_img[from_x:to_x, from_y:to_y, :]

                # patches[itr] = Image.fromarray(patch)
                patches[itr] = axs[i, j].imshow(patch)
                axs[i, j].set_axis_off()
                image_name_unique = f'{image_name}_{itr + 1}.tif'

                itr = itr + 1

        plt.show(block=True)

Palm_Spliting(input_dir, output_dir, X_split, Y_split)
print("done")
