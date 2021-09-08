#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 2 11:10:36 2021

@author: emilymartins
"""
import pandas as pd
import numpy as np
import streamlit as st
from scipy import integrate
import matplotlib.pyplot as plt 

sampleData = "https://raw.githubusercontent.com/DrewCommandeur/EPHE201/866d4bef6d883fdd719b53851259ef6accb28d48/LinKin/25m_SprintData.csv"

st.title('Lab 3: Linear Kinematics- Sprint Analysis') #Title for Streamlit
st.write("*In this lab, you will learn how to calculate kinematic values from raw IMU sprinting data.*")

#Import Data:
st.header("""Upload the IMU data you would like to analyze:""")
st.subheader("Choose Data Source")
example = st.selectbox('Choose data source', ['Sample Data', 'Data from file'])
st.subheader("a: Select the file type you are uploading (Note: only .csv and .xlsx files are accepted)")
f_type=st.selectbox('Select the file type', [".csv", ".xlsx"]) #Give option to upload file as .csv or .xlsx
st.subheader("b: Upload your file")




if example == "Sample Data":
    file = pd.read_csv(sampleData)

else:    
    file = st.file_uploader("Upload file", type=['csv', 'xlsx'])
    
    
if st.checkbox("Confirm file upload"): 
    if f_type== ".csv": #if file is .csv upload as .csv, else upload as excel
        df_og = pd.read_csv(file)
    else:
        df_og = pd.read_excel(file)
else:
    st.error("You must confirm your file upload to proceed.")
    st.stop()

#Visualize the axis of Translation:
st.header("""Select the column containing the axis the translation:""")
columns=st.multiselect("Select x, y, and z acceleration columns:", list(df_og.columns)) #slect x, y, and z accel axes to remove the time column if present
if st.checkbox("Confirm x, y, and z acceleration axes are selected"): #if 3 axes are confirmed, then users can select an axis to visualize to determine the axis of translation
    axis= st.selectbox("Select the axis of translation:", columns)
    fig, ax= plt.subplots()
    ax.plot(df_og[axis].index, df_og[axis], color="#8856a7")
    ax.set_xlabel("Samples (#)")
    ax.set_ylabel("Acceleration (m/s^2)")
    st.pyplot(fig)
else:
    st.error("Confirm axes to continue.")
    st.stop()


#Remove offset:
st.header("""Remove the offset & Find onset of movement""")
st.write("Quiet stance corresponds to a flat section of the signal (either before or after the sprint). Once the window is selected, the average acceleration of that window will be calculated; this average is the offset.")
st.write("The onset of movement can be estimated by the first peak in either the vertical axis or the axis of tranlation. In this analysis, we will use the axis of translation. If the data needs to be negated, the first peak would correspond to the first valley.")
min_ind, max_ind = st.slider('Move the black sliders to create a window of quiet stance:',df_og[axis].index.min(), df_og[axis].index.max(), (df_og[axis].index.min(), df_og[axis].index.max())) #create slider for creating window of quiet stance using vertical lines
start= df_og[axis].index.min()+100 
onset= st.slider("Move the green slider to the first peak (i.e. your onset of movement):", df_og[axis].index.min(), df_og[axis].index.max(), start,1) #create slider for users to select the index corresponding to the onset
offset= df_og[axis].iloc[min_ind:max_ind+1].mean() #calculate offset (average of window of quiet stance based on indices from slider)
offset_view=st.write("Offset= " + str(offset))
df=pd.DataFrame()
df[axis+ " Offset"]= df_og[axis]- offset #subtract offset from data

fig2, ax= plt.subplots() #create plot with vertical lines that move as above slider values change
ax.plot(df_og[axis].index, df_og[axis], color="#8856a7", label="Raw Accel")
ax.set_xlabel("Samples (#)")
ax.set_ylabel("Acceleration (m/s^2)")
ax.axvline(min_ind, color='black', linestyle='dashed') #vert line corresponding to min_ind value
ax.axvline(max_ind, color='black', linestyle='dashed') # vert line corresponding to max_ind value
ax.axvline(onset, color='green', linestyle='dashed') #vert line corresponding to index of onset 
if st.checkbox("Display the Acceleration with the offset removed:"): #if checkbox is checked then overlay offsetted acceleration over raw acceleration
    ax.plot(df[axis+ " Offset"].index, df[axis+ " Offset"], color="yellow", label="Accel Offset", linestyle="dotted")
    ax.legend(loc="upper right")
    st.pyplot(fig2)
else:
    ax.legend(loc="upper right")
    st.pyplot(fig2)
    
#Display cropped data:
if st.checkbox("Check to display graph with cropped and offsetted acceleration"): #if checkbox checked then display of croppsed and offsetted acceleration else pass
    fig3, ax= plt.subplots()
    ax.plot(df[axis+ " Offset"].iloc[onset:].index,df[axis+ " Offset"].iloc[onset:], color= "#fc9272")
    ax.set_xlabel("Samples (#)")
    ax.set_ylabel("Acceleration (m/s^2)")
    ax.set_title("Cropped Acceleration Offset vs Samples of a Sprint")
    st.pyplot(fig3)
else:
    pass


#Integrate:
st.header("""Riemann Sums""") 
st.write("In order to calculate Velocity and Displacement, we need to perform Riemann Sums. This analysis will use the Trapezoidal Method, which is the average of the Left and Right Methods.")
q1= st.radio('What is the Area under the following graphs: A) Acceleration vs Time and B) Velocity vs Time', ["A)Displacement, B)Power","A)Velocity, B)Impulse", "A)Velocity, B)Displacement" ])
if st.checkbox('Check Answer', key="q1"):
    if q1== "A)Displacement, B)Power":
        st.error("Incorrect")
    elif q1== "A)Velocity, B)Impulse":
        st.error("Incorrect")
    else:
        st.success("Correct!")
sample_rate=st.number_input('Enter the sample rate (e.g. 208 Hz)', min_value=1) #enter sample rate in Hz
delta_time= 1/sample_rate
crop=df[axis+ " Offset"].iloc[onset:].reset_index(drop=True) 
real_t=np.arange(len(crop))*delta_time #create real time column using sample rate 
trap_velocity=integrate.cumtrapz(crop, x=None, dx=delta_time, initial=0) #calculate velocity
trap_velocity=pd.Series(trap_velocity)
trap_displ= integrate.cumtrapz(trap_velocity, x=None, dx=delta_time, initial=0) #calculate displacement
trap_displ=pd.Series(trap_displ)
def g_set(y_label, y_data, time, c, title): #create function for graphing
    ax.plot(time, y_data, color=c)
    ax.set_ylabel(y_label)
    ax.set_xlabel("Time (sec)")
    ax.set_title(title)
    return
#Crop to end time:
st.header("""Crop the end of the data""")
st.write("To crop the end of the sprint, we will use the sprint time.")
sprint_time=st.number_input('Enter sprint time in seconds', min_value=0.00) #enter sprint time to crop data
real_t_s= pd.Series(real_t)
crop_t_ind= real_t_s.where(real_t_s<=sprint_time).last_valid_index() #find index of sprint time in real time

#Final cropped dataframe: crop real time, accel, v, and d to sprint time 
final=pd.DataFrame()
final['Real Time (sec)']= real_t_s.iloc[:crop_t_ind+1]
final["Acceleration (m/s^2)"]= crop.iloc[:crop_t_ind+1]
final["Velocity (m/s)"]= trap_velocity.iloc[:crop_t_ind+1]
final["Displacement (m)"]= trap_displ.iloc[:crop_t_ind+1]

#Negate data option:
st.write("You may not be able to recognize that the data needs to be negated until you plot the velocity data. Use the graphs below to determine if the data should be negated.")
st.write("*Hint: If the velocity and displacement are increasing in the negative direction (i.e. the data is below the x-axis), then it needs to be negated.*")
kin_final=final.columns[1:]
if st.checkbox("Negate Data"): #if checkbox checked, then negate data, else pass
    for i in range(len(kin_final)):
        final[kin_final[i]]=final[kin_final[i]]*-1
else:
    pass

#Visualize Accel, v, and d using g_set function
c1,c2,c3= st.beta_columns(3) #create 3 columns on streamlit page- 1 col for each graph
fig4, ax=plt.subplots()
a_graph= g_set("Acceleration (m/s^2)",final["Acceleration (m/s^2)"], final['Real Time (sec)'], "red", "Acceleration vs Time of a Sprint" )
c1.pyplot(fig4)
fig5,ax=plt.subplots()
v_graph=g_set("Velocity (m/s)",final["Velocity (m/s)"], final['Real Time (sec)'], "blue", "Velocity vs Time of a Sprint" )
c2.pyplot(fig5)
fig6,ax=plt.subplots()
d_graph=g_set("Displacement (m)",final["Displacement (m)"], final['Real Time (sec)'], "green", "Displacement vs Time of a Sprint" )
c3.pyplot(fig6)


#Calculate kinematic variables:
st.header("""Calculate kinematic variables""")
with st.echo(): #insert code below into streamlit
    v_max= final["Velocity (m/s)"].max()
    v_avg=final["Velocity (m/s)"].mean()
    v_final=final["Velocity (m/s)"].iloc[-1] #.iloc[-1] corresponds to the final index
    a_avg=final["Acceleration (m/s^2)"].mean()
    d_final=final["Displacement (m)"].iloc[-1]
kin_vars= [v_max, v_avg, v_final, a_avg, d_final]
kin_vars_name= ("Max Velocity (m/s)", "Average Velocity (m/s)", "Final Velocity (m/s)", "Average Acceleration (m/s^2)", "Final Displacement (m)")
kin_vars_r=[]
for i in range(len(kin_vars)): #display all kinematic values in list kin_vars with corresponding variable names in kin_vars_name list
    kin_vars_r.append(round(kin_vars[i],2))
    st.write(kin_vars_name[i]+ "= " + str(kin_vars_r[i]))


st.header("Your analysis is complete!")
