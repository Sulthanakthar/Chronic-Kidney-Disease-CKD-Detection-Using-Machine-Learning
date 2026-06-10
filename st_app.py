import streamlit as st
import os
import base64
import warnings

# Suppress unpickling and feature name warnings globally
try:
    from sklearn.exceptions import InconsistentVersionWarning
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
except ImportError:
    pass
warnings.filterwarnings("ignore", category=UserWarning)

# Convert local logo to base64 and cache the result for performance
@st.cache_data
def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def login_page():
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    if os.path.exists(logo_path):
        logo_base64 = get_image_base64(logo_path)
        logo_html = f'<div class="logo-container"><img src="data:image/png;base64,{logo_base64}" alt="Logo"></div>'
    else:
        logo_html = ""

    st.markdown(
        f"""
        <style>
            /* Logo positioning */
            .logo-container {{
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 1000;
            }}
            .logo-container img {{
                width: 65px; /* Adjust logo size */
            }}

            /* Login container styling */
            .login-container {{
                max-width: 400px;
                margin: 0 auto;
                padding: 6px;
                text-align: center;
                border-radius: 15px;
                background-color: #f5f5f5;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            .login-container h1 {{
                color: #333;
                font-size: 24px;
                margin-bottom: 10px;
            }}
            .stButton>button {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
                font-size: 16px;
            }}
            .stButton>button:hover {{
                background-color: #45a049;
            }}
            .stTextInput>div>div>input {{
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #ccc;
                width: 100%;
                font-size: 16px;
            }}
        </style>
        {logo_html}
        <div class="login-container">
            <h1>CKD DETECTION LOGIN PAGE</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Username and password inputs
    username = st.text_input("Username")
    password = st.text_input("password", type="password")

    # Login button
    login_button = st.button("Login")

    if login_button:
        if username == "admin" and password == "Sulthan":
            st.success("Logged in successfully!")
            st.session_state['logged_in'] = True
        else:
            st.error("Invalid username or password")
            st.stop()

def logout():
    if 'logged_in' in st.session_state:
        del st.session_state['logged_in']
    st.success("You have been logged out successfully!")

# Check login state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Display login page or main app
if not st.session_state['logged_in']:
    login_page()
else:
    st.sidebar.button("Logout", on_click=logout)
    import pandas as pd
      # Replace with your main app content

    # Load the trained model
    @st.cache_resource
    def load_model():
        import joblib
        model_path = 'RFmodel.pkl'
        if os.path.exists(model_path):
         return joblib.load(model_path)
        else:
         return None

    model = load_model()

# Function to preprocess user input
    def preprocess_input(data):
       from sklearn.preprocessing import StandardScaler
       df = pd.DataFrame(data, index=[0])
       scaler = StandardScaler()
       df_scaled = scaler.fit_transform(df)
       return df_scaled


    

# Check if image exists before loading it
    

    menu = st.sidebar.selectbox("Choose an option", ["Predict CKD", "Data Visualization","Nearby Hospitals","Dietary Recommendations"])

    if menu == "Predict CKD":
        st.title("Chronic Kidney Disease Detection App")
        st.markdown("---")
        st.markdown("""
        This app predicts the likelihood of Chronic Kidney Disease (CKD) based on various medical features.
        Enter the details below and click 'Predict' to get the result.
        """)

    # Input fields for features
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=50, max_value=200, value=70)
        specific_gravity = st.selectbox("Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025], index=4)
        albumin = st.selectbox("Albumin Level", [0, 1, 2, 3, 4, 5], index=0)
        sugar = st.selectbox("Sugar Level", [0, 1, 2, 3, 4, 5], index=0)
        red_blood_cells = st.selectbox("Red Blood Cells", ["normal", "abnormal"], index=0)
        pus_cell = st.selectbox("Pus Cell", ["normal", "abnormal"], index=0)
        pus_cell_clumps = st.selectbox("Pus Cell Clumps", ["present", "not present"], index=1)
        bacteria = st.selectbox("Bacteria", ["present", "not present"], index=1)
        blood_glucose_random = st.number_input("Blood Glucose Random (mg/dL)", min_value=50, max_value=500, value=107)
        blood_urea = st.number_input("Blood Urea (mg/dL)", min_value=1, max_value=500, value=33)
        serum_creatinine = st.number_input("Serum Creatinine (mg/dL)", min_value=0.1, max_value=20.0, value=0.86)
        sodium = st.number_input("Sodium (mEq/L)", min_value=100, max_value=200, value=142)
        potassium = st.number_input("Potassium (mEq/L)", min_value=1.0, max_value=10.0, value=4.3)
        haemoglobin = st.number_input("Haemoglobin (g/dL)", min_value=3.0, max_value=20.0, value=15.2)
        packed_cell_volume = st.number_input("Packed Cell Volume", min_value=20, max_value=60, value=46)
        white_blood_cell_count = st.number_input("White Blood Cell Count (cells/cmm)", min_value=1000, max_value=20000, value=7700)
        red_blood_cell_count = st.number_input("Red Blood Cell Count (millions/cmm)", min_value=1.0, max_value=10.0, value=5.4)
        hypertension = st.selectbox("Hypertension", ["yes", "no"], index=1)
        diabetes_mellitus = st.selectbox("Diabetes Mellitus", ["yes", "no"], index=1)
        coronary_artery_disease = st.selectbox("Coronary Artery Disease", ["yes", "no"], index=1)
        appetite = st.selectbox("Appetite", ["good", "poor"], index=0)
        peda_edema = st.selectbox("Pedal Edema", ["yes", "no"], index=1)
        aanemia = st.selectbox("Anemia", ["yes", "no"], index=1)

    # Map categorical variables to numeric values as per the training dataset
        mapping = {
            "normal": 1,
            "abnormal": 0,
            "present": 1,
            "not present": 0,
            "yes": 1,
            "no": 0,
            "good": 0,
            "poor": 1
        }

    # Prepare the input data as a DataFrame with feature names to match the model training phase
        input_data = pd.DataFrame([[
            age, blood_pressure, specific_gravity, albumin, sugar,
            mapping[red_blood_cells], mapping[pus_cell], mapping[pus_cell_clumps],
            mapping[bacteria], blood_glucose_random, blood_urea, serum_creatinine,
            sodium, potassium, haemoglobin, packed_cell_volume, white_blood_cell_count,
            red_blood_cell_count, mapping[hypertension], mapping[diabetes_mellitus],
            mapping[coronary_artery_disease], mapping[appetite], mapping[peda_edema],
            mapping[aanemia]
        ]], columns=[
            'age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
            'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
            'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
            'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema', 'aanemia'
        ])

        if st.button("Predict"):
            prediction = model.predict(input_data)
            if prediction[0] == 0:  # Assuming 0 indicates CKD
                st.error("The patient is likely to have Chronic Kidney Disease (CKD).")
                st.markdown("### Recommended Treatment:")
                st.write("- Consult a nephrologist for further evaluation.")
                st.write("- Follow a low-sodium, kidney-friendly diet.")
                st.write("- Maintain good hydration and monitor fluid intake.")
                st.write("- Regular monitoring of kidney function and blood pressure.")
            else:
                st.success("The patient is not likely to have Chronic Kidney Disease (CKD).")
        # Display normal values for key features
        st.markdown("### Normal Values for Key Features:")
        st.write("""
        - **Age**: N/A (No specific normal range, but CKD risk increases with age.)
        - **Blood Pressure**: 90/60 mmHg to 120/80 mmHg.
        - **Specific Gravity**: 1.005 to 1.030.
        - **Albumin Level**: 0 (Normal urine albumin is < 30 mg/day).
        - **Sugar Level**: 0 (Normal urine sugar is 0).
        - **Red Blood Cells**: Normal (No RBCs in urine).
        - **Pus Cell**: Normal (No pus cells in urine).
        - **Pus Cell Clumps**: Not present.
        - **Bacteria**: Not present.
        - **Blood Glucose Random**: 70–140 mg/dL.
        - **Blood Urea**: 7–20 mg/dL.
        - **Serum Creatinine**: 0.6–1.2 mg/dL.
        - **Sodium**: 135–145 mEq/L.
        - **Potassium**: 3.5–5.0 mEq/L.
        - **Haemoglobin**: 12–16 g/dL (females), 13.5–17.5 g/dL (males).
        - **Packed Cell Volume**: 36–46% (females), 40–52% (males).
        - **White Blood Cell Count**: 4,000–11,000 cells/cmm.
        - **Red Blood Cell Count**: 4.7–6.1 million/cmm (males), 4.2–5.4 million/cmm (females).
        - **Hypertension**: No.
        - **Diabetes Mellitus**: No.
        - **Coronary Artery Disease**: No.
        - **Appetite**: Good.
        - **Pedal Edema**: No.
        - **Anemia**: No.
        """)

    
    elif menu == "Nearby Hospitals":
        import difflib
        st.title("🏥 Nearby Hospital Recommendations")
        st.markdown("---")

        location = st.text_input("Enter your city to find nearby Nephrology Hospitals:", key="search_location")
        if st.button("Find Hospitals") and location:
            st.write(f"🔍 Searching for nephrology hospitals in: {location}")

            query = f"nephrology hospital near {location}".replace(' ', '+')
            maps_url = f"https://www.google.com/maps/search/{query}"


            recommended_hospitals = {
            'chennai': [
                ('Stanley Medical Center', 'Chennai', '+91 44 25281336', '24/7', 'https://stanleymedicalcollege.ac.in/'),
                ('Apollo Hospital', 'Chennai', '+91 44 28290200', '24/7', 'https://www.apollohospitals.com/'),
                ('Kauvery Hospital', 'Chennai', '+91 44 40006000', '24/7', 'https://www.kauveryhospital.com/'),
                ('M.R Hospital', 'Chennai', '+91 44 25272022', 'Mon-Sat 9 AM - 8 PM', 'https://www.mrhospital.com/')
            ],
            'bangalore': [
                ('Manipal Hospital', 'Bangalore', '+91 80 40116666', '24/7', 'https://www.manipalhospitals.com/'),
                ('Fortis Hospital', 'Bangalore', '+91 80 66214444', '24/7', 'https://www.fortishealthcare.com/'),
                ('Aster CMI Hospital', 'Bangalore', '+91 80 43420100', '24/7', 'https://www.asterhospitals.in/')
            ],
            'vellore': [
                ('CMC Hospital', 'Vellore', '+91 416 2281000', '24/7', 'https://www.cmch-vellore.edu/')
            ],
            'coimbatore': [
                ('Ganga Hospital', 'Coimbatore', '+91 422 2485000', '24/7', 'https://www.gangahospital.com/'),
                ('KMCH', 'Coimbatore', '+91 422 4323800', '24/7', 'https://www.kmchhospitals.com/')
            ],
            'salem': [
                ('Gokulam Hospital', 'Salem', '+91 427 2448171', '24/7', 'https://www.gokulamhospitals.com/')
            ]
            }

            city_key = difflib.get_close_matches(location.lower(), recommended_hospitals.keys(), n=1, cutoff=0.6)
            city_key = city_key[0] if city_key else None

            if city_key:
                st.subheader("🏥 Recommended Nephrology Hospitals")
                for hospital in recommended_hospitals[city_key]:
                    st.write(f"**{hospital[0]}** - {hospital[1]}")
                    st.write(f"🌐 [Visit Website]({hospital[4]})")
                    st.write(f"📞 [Call]({hospital[2]})")
                    st.write(f"🕑 {hospital[3]}")
                    st.markdown(f"[📍 View on Google Maps](https://www.google.com/maps/search/?api=1&query={hospital[0].replace(' ', '+')},+{city_key})")
                    st.markdown("---")

            st.markdown(f"[View More Hospitals on Google Maps]({maps_url})")
        else:
            st.info("Enter a city name to find nearby hospitals.")

    elif menu == "Dietary Recommendations":
        st.title("Dietary Recommendations")
        st.markdown("---")
        
        st.write("#### Dietary Recommendations:")
        st.write("**Protein Management:**")
        st.write("- Limit red meat and processed protein sources.")
        st.write("- Choose plant-based proteins such as lentils, tofu, and chickpeas.")
        st.write("- Consume protein in moderation as per doctor's advice.")

        st.write("**Sodium Intake:**")
        st.write("- Avoid canned and processed foods high in sodium.")
        st.write("- Use herbs and spices instead of salt for flavor.")
        st.write("- Read food labels and choose low-sodium options.")

        st.write("**Potassium Control:**")
        st.write("- Limit potassium-rich foods such as bananas, oranges, potatoes, and spinach.")
        st.write("- Opt for low-potassium alternatives like apples, berries, and cabbage.")

        st.write("**Phosphorus Management:**")
        st.write("- Avoid processed foods, dairy products, and cola drinks.")
        st.write("- Choose phosphorus binders if prescribed by a healthcare provider.")

        st.write("**Fluid Intake:**")
        st.write("- Stay hydrated but avoid excessive fluid intake.")
        st.write("- Monitor fluid intake based on medical advice.")

        st.write("#### Meal Planning Tips:")
        st.write("- Plan meals with a balance of carbohydrates, proteins, and healthy fats.")
        st.write("- Use fresh ingredients and avoid ready-to-eat meals.")
        st.write("- Consult a dietitian for a personalized meal plan.")

        st.write("#### Foods to Avoid:")
        st.write("- High-sodium foods like chips, pickles, and processed meats.")
        st.write("- High-phosphorus foods such as nuts, seeds, and fast food.")
        st.write("- High-potassium foods including bananas, tomatoes, and avocados.")
        st.write("- Sugary drinks and alcohol.")
        st.write("- Limit potassium-rich foods such as bananas, oranges, potatoes, and spinach.")
        st.write("- Choose low-potassium alternatives like apples, berries, and green beans.")
        st.write("- Monitor phosphorus intake by avoiding processed foods, dairy products, and carbonated drinks.")
        st.write("- Select phosphorus binders if prescribed by a healthcare provider.")
        st.write("- Follow a low-sodium, kidney-friendly diet.")
        st.write("- Increase intake of fresh fruits and vegetables, avoiding high-potassium foods.")
        st.write("- Limit protein intake to reduce kidney workload.")
        st.write("- Stay hydrated by drinking sufficient water as per doctor's advice.")
        st.write("- Reduce salt intake and eat a balanced diet.")
        st.write("- Quit smoking and limit alcohol consumption.")
        st.write("- Manage stress through relaxation techniques.")

        
        #if st.button("Back to Prediction"):
            #st.session_state["menu"] = "Predict CKD"


    elif menu == "Data Visualization":
        import seaborn as sns
        import matplotlib.pyplot as plt
        import plotly.express as px
        st.header("CKD Dataset Visualization")
        st.markdown("---")
        uploaded_file = st.file_uploader("Upload CKD dataset (CSV format)", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if 'id' in df.columns:
                df.drop('id', axis=1, inplace=True)
            df.columns = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
                      'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                      'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
                      'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema', 'aanemia', 'class']
        
        # Convert categorical data to numerical if needed
            categorical_cols = df.select_dtypes(include=['object', 'string']).columns
            for col in categorical_cols:
                df[col] = df[col].astype('category').cat.codes  # Convert strings to integers
            # Filter numerical data
            numerical_df = df.select_dtypes(include=['int64', 'float64'])

            st.write("### Data Preview")
            st.dataframe(numerical_df.head())

            st.write("#### Correlation Heatmap")
            fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
            sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax_corr)
            st.pyplot(fig_corr)
            plt.close(fig_corr)

            st.write("#### Custom Bar Chart with Colors")
            selected_column = st.selectbox("Select column for bar chart", df.select_dtypes(include=['int64', 'float64']).columns)
            fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
            ax_bar.bar(df[selected_column].index, df[selected_column], color='#FF5733')
            ax_bar.set_xlabel(selected_column)
            ax_bar.set_ylabel("Value")
            ax_bar.set_title(f"{selected_column} Distribution")
            st.pyplot(fig_bar)
            plt.close(fig_bar)

            st.write("#### Feature Relationships")
            feature_x = st.selectbox("Select X-axis feature", numerical_df.columns)
            feature_y = st.selectbox("Select Y-axis feature", numerical_df.columns)
            fig_scat, ax_scat = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x=numerical_df[feature_x], y=numerical_df[feature_y], hue=df['class'], ax=ax_scat)
            st.pyplot(fig_scat)
            plt.close(fig_scat)

            def kde(col):
                grid = sns.FacetGrid(df, hue="class", height=6, aspect=2)
                grid.map(sns.kdeplot, col)
                grid.add_legend()
                st.pyplot(grid.fig)
                plt.close(grid.fig)
            
            def scatter(col1, col2):
                fig = px.scatter(df, x=col1, y=col2, color="class", template='plotly_dark')
                st.plotly_chart(fig)

            st.write("#### Kernel Density Estimation (KDE) Plots")
            selected_kde_feature = st.selectbox(
                "Select feature for KDE plot",
                ['red_blood_cell_count', 'white_blood_cell_count', 'packed_cell_volume', 'haemoglobin', 'albumin', 'blood_glucose_random', 'sodium', 'blood_urea', 'specific_gravity']
            )
            kde(selected_kde_feature)

            st.write("#### Scatter Plots")
            scatter_preset = st.selectbox(
                "Select preset scatter plot",
                [
                    "haemoglobin vs packed_cell_volume",
                    "blood_urea vs serum_creatinine",
                    "sodium vs potassium"
                ]
            )
            if scatter_preset == "haemoglobin vs packed_cell_volume":
                scatter('haemoglobin', 'packed_cell_volume')
            elif scatter_preset == "blood_urea vs serum_creatinine":
                scatter('blood_urea', 'serum_creatinine')
            elif scatter_preset == "sodium vs potassium":
                scatter('sodium', 'potassium')

    