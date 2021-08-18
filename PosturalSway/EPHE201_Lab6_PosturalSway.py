#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 19:35:28 2021


@author: vedasmith
"""
# import required modules
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from matplotlib.patches import Ellipse


st.write(""" 
         # Lab 6: Postural Sway 
         *Purpose:* To examine postural stability and sway under various conditions that challenge proprioception, vision, and the vestibular system.
         """) #title for streamlit
    
st.header('Pre-Lab Questions:') #header for streamlit
st.text_input('1. If posture is unstable what will you see on the graph of centre of pressure?') #short answer question
st.text_input('2. What measurement variables are recorded from the force platform during the assessment of postural stability?') #short answer question
              
# blank space and line for display           
text = '''



---



'''

st.header('Bounded Area of Ellipse') #header for streamlit
st.write('Calculating the bounded area of ellipse involves determining the maximum and minimum value in each axis to determine the diameter (d) of the ellipse.')
st.write('Use the slider to see how the bounded area of ellipse changes as the minimum and maximum values of excurion change.')

# create variables for the ellipse
u=1.     #x-position of the center
v=0.5    #y-position of the center
a=2.     #radius on the x-axis
b=1.5    #radius on the y-axis

col1, col2 = st.beta_columns(2) #make two columns
with col1: #isolate column 1 
    w = st.slider('Width (x)', 0, 10, 3) #slider for the width
    h = st.slider('Height (y)', 0, 10, 6) #slider for the height
with col2: #isolate column 2
    fig, ax = plt.subplots() 
    t = np.linspace(0, 2*pi, 100)
    plt.plot((u+a*np.cos(t))*w, (v+b*np.sin(t))*h, lw=4, color='#fd8d3c') #plot the ellipse, multiplying by slider variables to activate slider
    plt.grid(color='lightgray',linestyle='--')
    plt.xlim([-15,30]) #set axes limit so changes on slider can be seen clearly
    plt.ylim([-15,30]) #set axes limit so changes on slider can be seen clearly
    plt.show()
    st.pyplot(fig) #show figure
    st.write('Figure 1. Ellipse')

# blank space and line for display  
text = '''



---



'''

st.header('Measuring the Center of Pressure with Forceplate') #header for streamlit
st.write('Centre of pressure is measured with a force platform by calculating the difference in pressure between the [top and bottom] and [left and right] force sensors.')
st.image('/Users/vedasmith/Desktop/Streamlit/Lab 6 - Postural Sway/Screen Shot 2021-07-20 at 4.13.05 PM.png') #import image

st.write('Use the slider to see changes to X and Z as the forces at each sensor changes.')
col1, col2 = st.beta_columns(2) #make two columns
with col1: #isolate column 1
    Fxo = st.slider('Fxo', 0, 200, 100) #create slider for changing variables
    Fxz = st.slider('Fxz', 0, 200, 100)
    Foo = st.slider('Foo', 0, 200, 100)
    Foz = st.slider('Foz', 0, 200, 100)
Fy = 9.8 #label constant variables
x = 41.5
z = 42.5
with col2: #isolate column 2
    with st.echo(): #this displays the code below
        X = (x/2)*(1 + ((Fxo + Fxz) - (Foo + Foz)) / Fy)
    st.write('X = ', X)
    with st.echo(): #this displays the code below
        Z = (z/2)*(1 + ((Foz + Fxz) - (Foo + Fxo)) / Fy)
    st.write('Z = ', Z)

# blank space and line for display  
text = '''



---



'''

# import data
st.header('Step 1: Upload Postural Sway Data')
data = st.file_uploader('', type='.xlsx') #create a file uploader button
if st.checkbox('Confirm file upload'):
    sway_data = pd.read_excel(data, header=1)
else:
    st.error('You must confirm your file to proceed')
    st.stop() #stop streamlit until file is uploaded
    
columns = sway_data.columns #make an index for the column names

st.header('Step 2: Visualize the Data Table') #header for streamlit
st.write('It is important to initially visualize your data to ensure it has been uploaded correctly and to become familiar with the format you are working with.')
if st.button('Click to see the first rows of your data'): #create a button
    st.table(sway_data.head()) #display the first few rows of data

st.header('Step 3: Visualize Conditions with Scatter Plot') #header for streamlit
st.write('Data visualization through plots and figures is an important step in understanding your data.')
col1, col2 = st.beta_columns(2) #make two columns
# create 4 seperate scatterlpots
with col1: #isolate column1 row1
    if st.checkbox('Click to Visualize Condition 1'): #checkbox for condition 1
        fig, ax = plt.subplots()
        plt.scatter(sway_data[columns[0]], sway_data[columns[1]], color='#74a9cf', s =0.5) #create scatterplot
        plt.grid(color='lightgray',linestyle='--')
        plt.xlabel('X CoP Displacement (cm)') #label the x axis
        plt.ylabel('Y CoP Displacement (cm)') #label the y axis
        plt.xlim(10,20) #set x axis limit
        plt.ylim(5,25) #set y axis limit
        plt.title('Condition 1: Eyes Open') #add a title
        col1.pyplot(fig) #display the figure in column 1 in streamlit
with col2: #isolate column2 row1
    if st.checkbox('Click to Visualize Condition 2'): #checkbox for condition 2
        fig, ax = plt.subplots()
        plt.scatter(sway_data[columns[2]], sway_data[columns[3]], color='#74c476', s =0.5)
        plt.grid(color='lightgray',linestyle='--')
        plt.xlabel('X CoP Displacement (cm)')
        plt.ylabel('Y CoP Displacement (cm)')
        plt.xlim(10,20)
        plt.ylim(5,25)
        plt.title('Condition 2: Eyes Closed')
        col2.pyplot(fig)
with col1: #isolate column1 row2
    if st.checkbox('Click to Visualize Condition 3'): #checkbox for condition 3
        fig, ax = plt.subplots()
        plt.scatter(sway_data[columns[4]], sway_data[columns[5]], color='#fd8d3c', s =0.5)
        plt.grid(color='lightgray',linestyle='--')
        plt.xlabel('X CoP Displacement (cm)')
        plt.ylabel('Y CoP Displacement (cm)')
        plt.xlim(10,20)
        plt.ylim(5,25)
        plt.title('Condition 3: Eyes Open on Foam')
        col1.pyplot(fig)
with col2: #isolate column2 row2
    if st.checkbox('Click to Visualize Condition 4'): #checkbox for condition 4
        fig, ax = plt.subplots()
        plt.scatter(sway_data[columns[6]], sway_data[columns[7]], color='#807dba', s =0.5)
        plt.grid(color='lightgray',linestyle='--')
        plt.xlabel('X CoP Displacement (cm)')
        plt.ylabel('Y CoP Displacement (cm)')
        plt.xlim(10,20)
        plt.ylim(5,25)
        plt.title('Condition 4: Eyes Closed on Foam')
        col2.pyplot(fig)
plt.show()


st.header('Step 4: Calculate the Minimum and Maximum Excursion in the X and Y Axes') #header for streamlit
col1, col2 = st.beta_columns(2) #make two columns
with col1: #isolate column 1
    st.image('/Users/vedasmith/Desktop/Streamlit/Lab 6 - Postural Sway/bounded area of ellipse.png') #import image
    st.write('Figure 2. Bounded area of ellipse calculation')
with col2: #isolate column 2
    options = st.multiselect('What is needed to find a?', ['x min', 'range', 'x max', 'y max', 'median', 'center axis', 'y min']) #create a drop down menu with multiple right answers
    if options == ['x min','x max'] or options == ['x max','x min']: #if either option is chosen, the correct
        st.write('Correct!')
    else: #if neither of the above options are chosen, then try again
        st.write('Try Again.')
    
    options = st.multiselect('What is needed to find b?', ['x min', 'range', 'x max', 'y min', 'median', 'center axis', 'y max']) #create a drop down menu with multiple right answers
    if options == ['y min','y max']:
        st.write('Correct!')
    else:
        st.write('Try Again.')

# blank space and line for display  
text = '''



---



'''
    
col1, col2 = st.beta_columns(2) #make two columns
with col1: #isolate column 1
    st.write('*Find __a__ for each condition*') 
    cond = st.selectbox('Select Condition', [columns[0], columns[2], columns[4], columns[6]]) #drop down option to select a condition
    if st.checkbox('Confirm condition'):
        x_max = sway_data[cond].max() #find the max
        x_min = sway_data[cond].min() #find the min
        with st.echo(): #display the code below
            a = (x_max - x_min)/2
        st.write('a = ', a) #display the value for a for selected condition
    else:
        st.error('You must confirm condition to proceed')
with col2: #isolate column 2
    st.write('*Find __b__ for each condition*') 
    cond = st.selectbox('Select Condition', [columns[1], columns[3], columns[5], columns[7]])
    if st.checkbox('Confirm Condition'):
        y_max = sway_data[cond].max()
        y_min = sway_data[cond].min()
        with st.echo():
            b = (y_max - y_min)/2
        st.write('b = ', b) #display the value for b for selected condition
    else:
        st.error('You must confirm condition to proceed')

π = pi #label pi

st.header('Step 5: Calculate the Bounded Area of Excursion') #header for streamlit
option = st.radio('What is the equation for the Bounded Area of Excursion (A)?', ('A = (a)(b)/(ymax-ymin)','A = (π)/(a)(b)','A = (π)(a)(b)', 'A = (π)(xmin)(max)]')) #create a multiple choice question
if option == ('A = (π)(a)(b)'): #identify the correct answer
    st.write('Correct!')
else:
    st.write('Try Again.')

st.text_input('What are the advantages and disadvantages of using the bounding ellipse rather than a confidence ellipse?') #create a written question

# make lists for the min and max values of x and y for all conditions - used for future calculations
y_max = [sway_data[columns[1]].max(), sway_data[columns[3]].max(), sway_data[columns[5]].max(), sway_data[columns[7]].max()] #find the max of y values
y_min = [sway_data[columns[1]].min(), sway_data[columns[3]].min(), sway_data[columns[5]].min(), sway_data[columns[7]].min()] #find the min of y values
x_max = [sway_data[columns[0]].max(), sway_data[columns[2]].max(), sway_data[columns[4]].max(), sway_data[columns[6]].max()] #find the max of x values
x_min = [sway_data[columns[0]].min(), sway_data[columns[2]].min(), sway_data[columns[4]].min(), sway_data[columns[6]].min()] #find the min of x values

a_list = [] #create an empty list for a values
b_list = [] #create an empty list for b values

for i in range(4): #loop through 4 conditions
    a_list.append((x_max[i] - x_min[i])/2) #find a values and add them to a_list
    b_list.append((y_max[i] - y_min[i])/2) #find b values and add them to b_list

A_list = [] #create an empty list for A values

for i in range(4): #loop through 4 conditions
    A_list.append((pi * (a_list[i])* (b_list[i]))) #find A values and add them to A_list


st.header('Step 6: Add Bounded Area of Ellipse to Scatter Plot') #header for streamlit
st.write('*Check each box to see the Figures*')

center = [] #create an empty list for center values of each condition
for i in range(4): #loop through 4 conditions
    center.append([((x_max[i]+x_min[i])/2), ((y_max[i]+y_min[i])/2)]) #find center values of each conditon and add to center list


col1, col2 = st.beta_columns(2) #make two columns
with col1: #put something into column1 row1
    if st.checkbox('Condition 1'): #checkbox for condition 1
        fig, ax = plt.subplots() 
        plt.scatter(sway_data[columns[0]], sway_data[columns[1]], color='#74a9cf', s =0.5) #create scatterplot
        plt.grid(color='lightgray',linestyle='--')
        plt.xlabel('X CoP Displacement (cm)') #label x axis
        plt.ylabel('Y CoP Displacement (cm)') #label y axis
        plt.xlim(10,20) #set x axis limit
        plt.ylim(5,25) #set y axis limit
        plt.title('Condition 1: Eyes Open with Bounded Area of Ellipse') #add title
        plt.figure()
        ellipse0 = Ellipse(center[0], a_list[0]*2, b_list[0]*2, fc='none', ec='#000000', lw=2, linestyle='--') #add bounding ellipse to figure, multiple a_list and b_list by 2 for the width and heigh inputs
        ax.add_patch(ellipse0)
        plt.show()
        col1.pyplot(fig) #display on streamlit
with col2: #put something into column2 row1
    if st.checkbox('Condition 2'):  #checkbox for condition 2
        fig, ax = plt.subplots()
        plt.scatter(sway_data[columns[2]], sway_data[columns[3]], color='#74c476', s =0.5)
        plt.grid(color='lightgray',linestyle='--')
        plt.xlabel('X CoP Displacement (cm)')
        plt.ylabel('Y CoP Displacement (cm)')
        plt.xlim(10,20)
        plt.ylim(5,25)
        plt.title('Condition 2: Eyes Closed with Area of Bounded Ellipse')
        plt.figure()
        ellipse1 = Ellipse(center[1], a_list[1]*2, b_list[1]*2, fc='none', ec='#000000', lw=2, linestyle='--')
        ax.add_patch(ellipse1)
        plt.show()
        col2.pyplot(fig)
with col1: #put something into column1 row2
    if st.checkbox('Condition 3'):  #checkbox for condition 3
        fig, ax = plt.subplots()
        plt.scatter(sway_data[columns[4]], sway_data[columns[5]], color='#fd8d3c', s =0.5)
        plt.grid(color='lightgray',linestyle='--')
        plt.xlabel('X CoP Displacement (cm)')
        plt.ylabel('Y CoP Displacement (cm)')
        plt.xlim(10,20)
        plt.ylim(5,25)
        plt.title('Condition 3: Eyes Open on Foam with Bounded Area of Ellipse')
        plt.figure()
        ellipse2 = Ellipse(center[2], a_list[2]*2, b_list[2]*2, fc='none', ec='#000000', lw=2, linestyle='--')
        ax.add_patch(ellipse2)
        plt.show()
        col1.pyplot(fig)
with col2: #put something into column2 row2
    if st.checkbox('Condition 4'):  #checkbox for condition 4
        fig, ax = plt.subplots()
        plt.scatter(sway_data[columns[6]], sway_data[columns[7]], color='#807dba', s =0.5)
        plt.grid(color='lightgray',linestyle='--')
        plt.xlabel('X CoP Displacement (cm)')
        plt.ylabel('Y CoP Displacement (cm)')
        plt.xlim(10,20)
        plt.ylim(5,25)
        plt.title('Condition 4: Eyes Closed on Foam with Bounded Area of Ellipse')
        plt.figure()
        ellipse3 = Ellipse(center[3], a_list[3]*2, b_list[3]*2, fc='none', ec='#000000', lw=2, linestyle='--')
        ax.add_patch(ellipse3)
        plt.show()
        col2.pyplot(fig)

col1,col2 = st.beta_columns(2) #create 2 columns
with col1: #isolate colum 1
    one = st.radio('1. Which condition was the most stable?', ['Condition 3: Eyes Open on Foam', 'Condition 1: Eyes Open', 'Condition 2: Eyes Closed', 'Condition 4: Eyes Closed on Foam']) #mulitple choice question
    if one == 'Condition 1: Eyes Open': #identify correct option
        st.write('Correct!')
    else:
        st.write('Try Again')
with col2: #isolate column 2
    two = st.radio('2. Which condition was the least stable?', ['Condition 1: Eyes Open', 'Condition 3: Eyes Open on Foam', 'Condition 2: Eyes Closed', 'Condition 4: Eyes Closed on Foam']) #mulitple choice question
    if two == 'Condition 4: Eyes Closed on Foam': #identify correct option
        st.write('Correct!')
    else:
        st.write('Try Again')

#create a dataframe for summary of findings
st.header('Summary of Findings')
summary_df = pd.DataFrame(x_min, index=['Condition 1','Condition 2', 'Condition 3', 'Condition 4'], columns = ['x min (cm)']) #create df and set the index as condition names
summary_df['x max (cm)'] = x_max #create column for x max
summary_df['y min (cm)'] = y_min #create column for y min
summary_df['y_max (cm)'] = y_max #create column for y max
summary_df['a (cm)'] = a_list #create column for a values
summary_df['b (cm)'] = b_list #create column for b values
summary_df['A (cm^2)'] = A_list #create column for A values

if st.button('Click for Summary'): #create a button
    st.table(summary_df) #display the summary table when button is clicked
    st.success('Congratulations, your analysis is complete!') #completion message :)


















