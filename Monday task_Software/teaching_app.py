import pandas as pd

# Load datasets
instructors_df = pd.read_csv('archive/instructors.csv')
courses_df = pd.read_csv('archive/courses.csv')
course_instructors_df = pd.read_csv('archive/course_instructors.csv')

# Preview datasets
print(instructors_df.head())
print(courses_df.head())
print(course_instructors_df.head())

# Simple GUI using Tkinter

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import requests
from io import BytesIO
from textblob import TextBlob
import numpy as np
from sklearn.linear_model import LinearRegression

# Load datasets
instructors_df = pd.read_csv('archive/instructors.csv')
courses_df = pd.read_csv('archive/courses.csv')
course_instructors_df = pd.read_csv('archive/course_instructors.csv')

# Dummy data for course ratings
X = np.array([[10], [20], [30], [40], [50]])  # Number of students
y = np.array([3, 4, 2, 5, 4])  # Ratings (1 to 5)

# Train a simple linear regression model
model = LinearRegression()
model.fit(X, y)

# Function to predict course rating
def predict_rating(num_students):
    prediction = model.predict(np.array([[num_students]]))
    return round(prediction[0], 2)

# Function to analyze feedback
def analyze_feedback():
    feedback = feedback_text.get("1.0", tk.END)
    analysis = TextBlob(feedback)
    sentiment = analysis.sentiment.polarity
    
    if sentiment > 0:
        feedback_result.config(text="Positive feedback", foreground="green")
    elif sentiment < 0:
        feedback_result.config(text="Negative feedback", foreground="red")
    else:
        feedback_result.config(text="Neutral feedback", foreground="blue")

# Function to display instructor information
def show_instructor_info(event):
    instructor_id = instructor_combobox.get().split(" - ")[0]
    instructor_data = instructors_df[instructors_df['instructor_id'] == int(instructor_id)].iloc[0]
    courses_taught = course_instructors_df[course_instructors_df['instructor_id'] == int(instructor_id)]['course_id']
    
    # Show instructor's bio
    bio_label.config(text=instructor_data['bio'])
    
    # Show instructor's image
    response = requests.get(instructor_data['img'])
    img_data = Image.open(BytesIO(response.content))
    img_data = img_data.resize((150, 150), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img_data)
    instructor_img_label.config(image=img)
    instructor_img_label.image = img

    # Show courses taught
    course_listbox.delete(0, tk.END)
    for course_id in courses_taught:
        course_info = courses_df[courses_df['course_id'] == course_id].iloc[0]
        course_listbox.insert(tk.END, f"{course_info['title']} (Price: {course_info['price']})")
        
        # Predict course rating based on dummy student enrollment data
        predicted_rating = predict_rating(course_info['total_enrolled_students'])  # Assume there's a column for this
        print(f"Predicted rating for {course_info['title']}: {predicted_rating}")

# Create main window
root = tk.Tk()
root.title("AI-Enhanced Application to Evaluate Teaching Practices")
root.config(bg="#e0e0e0")  # Background color

# Set stylish fonts with smaller sizes
header_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
label_font = tkFont.Font(family="Arial", size=10, weight="bold")
listbox_font = tkFont.Font(family="Verdana", size=9)

# Dropdown for selecting instructor
instructor_label = ttk.Label(root, text="Select Instructor:", font=header_font)
instructor_label.pack(pady=5)  # Reduced padding
instructor_label.config(background="#a0d3e8")  # Background color

instructor_combobox = ttk.Combobox(root, font=label_font, values=[f"{row['instructor_id']} - {row['name']}" for _, row in instructors_df.iterrows()])
instructor_combobox.pack(pady=5)  # Reduced padding

# Bio and image display
bio_label = ttk.Label(root, text="Instructor Bio", font=label_font, wraplength=300)
bio_label.pack(pady=5)  # Reduced padding
bio_label.config(background="#f9f9f9")  # Background color

instructor_img_label = ttk.Label(root)
instructor_img_label.pack(pady=5)  # Reduced padding

# Course list display
course_label = ttk.Label(root, text="Courses Taught:", font=header_font)
course_label.pack(pady=5)  # Reduced padding
course_label.config(background="#f0f8ff")  # Background color

course_listbox = tk.Listbox(root, height=8, width=50, font=listbox_font)
course_listbox.pack(pady=5)  # Reduced padding
course_listbox.config(background="#c8e6c9", fg="black")  # Listbox colors

# Feedback section
feedback_label = ttk.Label(root, text="Provide Feedback:", font=label_font)
feedback_label.pack(pady=5)  # Reduced padding
feedback_label.config(background="#f0f8ff")  # Background color

feedback_text = tk.Text(root, height=5, width=50)
feedback_text.pack(pady=5)  # Reduced padding

analyze_button = ttk.Button(root, text="Analyze Feedback", command=analyze_feedback)
analyze_button.pack(pady=5)  # Reduced padding

feedback_result = ttk.Label(root, text="", font=label_font)
feedback_result.pack(pady=5)  # Reduced padding

# Bind selection event
instructor_combobox.bind("<<ComboboxSelected>>", show_instructor_info)

# Start the GUI loop
root.mainloop()





