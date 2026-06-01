from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import sqlite3
import numpy as np 
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Conv1D, Dense, Flatten, MaxPooling1D, Dropout, BatchNormalization
from keras.models import Sequential


def suggest_roles(skills):
    skill_mapping = {
        'python': 'Python Developer ,Machine Learning Engineer,Game Developer',
        'sql': 'SQL Developer,Database Administrator (DBA),Database Developer,Business Intelligence (BI) Developer',
        'javascript': 'JavaScript Developer,Mobile App Developer,Game Developer ',
        'php': 'PHP Developer,System Administrator,Web Designer',
        'java': 'Java Developer,Java Software Architect,Android Developer',
        'ruby': 'Ruby Developer,Test Automation Engineer,Technical Support Engineer',
        'html and css': 'FrontEnd Developer,Digital Marketing Specialist,Content Manager',
        'mobile applications developer': 'Mobile Applications Developer, Mobile Applications Developer,Mobile Applications Developer',
         'web developer': 'Web Developer, Web Developer, Web Developer',
         'network security engineer': 'Network Security Engineer, Network Security Engineer, Network Security Engineer',
        'technical support engineer': 'Technical Support Engineer, Technical Support Engineer, Technical Support Engineer',
         'ui/ux developer': 'UI/UX Developer, UI/UX Developer, UI/UX Developer',
        'software tester/Quality Assurance Engineer': 'Software Tester/Quality Assurance Engineer, Software Tester/Quality Assurance Engineer, Software Tester/Quality Assurance Engineer',
         'database developer': 'Database Developer, Database Developer,Database Developer',
         'mobile applications Developer' : 'Mobile Applications Developer, Mobile Applications Developer, Mobile Applications Developer',
         'software engineer' : 'Software Engineer, Software Engineer, Software Engineer'

    }
    suggested_roles = [skill_mapping.get(skill, 'Unknown Role') for skill in skills.split(',')]
    return ', '.join(suggested_roles)





def predict(mark,skill):
    class_names = {
        0: 'Birlasoft', 1: 'Cognizant', 2: 'Hexaware Technologies',
        3: 'Infosys', 4: 'KPIT Technologies', 5: 'L&T Infotech',
        6: 'Tech Mahindra', 7: 'Wipro Technologies', 8: 'css corp',9:'TCS'
    }
    train_data=pd.read_csv("Book2.csv", encoding='latin-1')
    le_Skill = LabelEncoder()
    le_depart= LabelEncoder()
    le_Company  = LabelEncoder()
    train_data['skill'] = le_Skill.fit_transform(train_data['Skills Known'])
    train_data['dept'] = le_depart.fit_transform(train_data['department'])
    train_data['target'] = le_Company.fit_transform(train_data['Company Placed'])
    x = train_data.drop(['Full Name', "12th Mark","10th Mark","dept",'Company Placed', "Skills Known","Projects Done",'target','department',"Certifications/Internships"], axis = 1)
    y = train_data['target']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    num_classes = 10
    y_train_processed = np.clip(y_train, 0, num_classes - 1)
    y_test_processed = np.clip(y_test, 0, num_classes - 1)

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(x_train)
    X_test_scaled = scaler.transform(x_test)
    X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], X_train_scaled.shape[1], 1))
    X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], X_test_scaled.shape[1], 1))
    cnn_model = Sequential()
    cnn_model.add(Conv1D(filters=64, kernel_size=5, activation='relu', input_shape=(X_train_reshaped.shape[1], X_train_reshaped.shape[2]), padding='same'))
    cnn_model.add(BatchNormalization())
    cnn_model.add(MaxPooling1D(pool_size=1))
    cnn_model.add(Dropout(0.5))
    cnn_model.add(Conv1D(filters=128, kernel_size=5, activation='relu', padding='same'))
    cnn_model.add(BatchNormalization())
    cnn_model.add(MaxPooling1D(pool_size=2))
    cnn_model.add(Dropout(0.5))
    cnn_model.add(Flatten())
    cnn_model.add(Dense(256, activation='relu'))    
    cnn_model.add(Dropout(0.5))
    cnn_model.add(Dense(num_classes, activation='softmax'))
    cnn_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    history_cnn = cnn_model.fit(X_train_reshaped, y_train_processed, epochs=5, batch_size=64, validation_data=(X_test_reshaped, y_test_processed),verbose=0)
    predicted_probs = cnn_model.predict([[mark,0,skill]])
    top_indices = np.argsort(predicted_probs[0])[::-1][:3]
    top_companies = [(class_names[i]) for i in top_indices]
    return(top_companies)
