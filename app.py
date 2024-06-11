from flask import Flask, request, make_response,jsonify
import pandas as pd
import io
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)
# Store the data in memory
data = None

@app.route('/', methods=['GET'])
def index():
    return "Hi from server"

@app.route("/upload", methods=['POST'])
def upload_route():
    global data

    # Check if a file was uploaded
    if 'file' not in request.files:
        return {"msg":'No file uploaded'}

    # Get the uploaded file
    file = request.files['file']

    # Read the file as a DataFrame
    data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    print(request.form.get("start_date"))
    # Check if start_date and end_date were provided
    if 'start_date' in request.form and 'end_date' in request.form:
        # Get the start and end dates from the request
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Filter the data based on the selected dates
        data = data[(data['DisplayDtTm'] >= start_date) & (data['DisplayDtTm'] <= end_date)]

    return {"msg": 'File uploaded successfully'}



@app.route('/mean')
def calculate_mean():
    # Check if data is loaded
    if data is None:
        return {"msg":'No data loaded'}
    
    # Perform your calculations on the stored data
    # For this example, let's calculate the standard deviation of the "Glucose Value" column
    meanVal = data["Glucose Value"].mean()
    
    dataMean = str(meanVal)
    return {"mean":dataMean}

# Define the route to perform calculations and download the result
@app.route('/sd')
def calculate_route():
    # Check if data is loaded
    if data is None:
        return {"msg":'No data loaded'}
    
    # Perform your calculations on the stored data
    # For this example, let's calculate the standard deviation of the "Glucose Value" column
    std_dev = data["Glucose Value"].std()
    
    dataSD = str(std_dev)
    return {"sd":dataSD}


@app.route('/sdr') #d
def calculate_sdr():
    # Check if data is loaded
    if data is None:
        return {"msg":'No data loaded'}
    
    # Read the CSV file or perform any necessary data retrieval

    # Caluclate thr SDR values
    stdr_dev = data['Glucose Value'].diff() / 2
    stdr = stdr_dev.std()
    dataSDR = str(stdr)


    # Calculate the BG Rate of Change
    data['BG Rate of Change'] = data['Glucose Value'].diff() / 2

    # Calculate standard deviation and mean
    bg_roc_std = data['BG Rate of Change'].std()
    bg_roc_mean = data['BG Rate of Change'].mean()

    # Prepare the histogram data
    histogram_data = data['BG Rate of Change'].tolist()
    histogram_data = [None if np.isnan(x) else x for x in histogram_data]


    # Return the calculated data as JSON
    response = {
        'dataSDR' : dataSDR,
        'bg_roc_std': bg_roc_std,
        'bg_roc_mean': bg_roc_mean,
        'histogram_data': histogram_data
    }
    return jsonify(response)


# @app.route('/iqr', methods=['GET'])
# def calculate_iqr():
#     # Load the data and calculate the IQR
#     if data is None:
#         return {"msg":'No data loaded'}
    
#     iqr_data = data['Glucose Value'].tolist()
#     print(iqr_data)
#     # Calculate the statistics for the IQR graph
#     iqr_stats = {
#         'data': iqr_data,
#     }

#     return iqr_stats


@app.route('/iqr', methods=['GET']) #d
def calculate_iqr():
    # Load the data and calculate the IQR
    global data
    if data is None:
        return {"msg": 'No data loaded'}
    
    iqr_data = data['Glucose Value'].tolist()
    # Calculate the quartiles and median
    
    dataValues = {
       "iqrdata":iqr_data
    }
   

    return jsonify(dataValues)


@app.route('/sdr_table', methods=['GET'])
def calculate_sdr_table():
    # Load the data and calculate the IQR
    if data is None:
        return {"msg":'No data loaded'}
    
    # Calculate the BG Rate of Change
    data['BG Rate of Change'] = data['Glucose Value'].diff() / 2
    data2 = data['BG Rate of Change'] = data['BG Rate of Change'].replace(np.nan, None)
    print(data2)

    # Select the required columns for the table
    table_data = data[['DisplayDtTm', 'Glucose Value', 'BG Rate of Change']].head().to_dict("records")
    # print(jsonify(table_data))
    
    return table_data


@app.route('/rolling_stats', methods=['GET'])
def calculate_rolling_stats():
    
    if data is None:
        return {"msg":'No data loaded'}
    
    # Calculate rolling mean and standard deviation
    window = 7
    rolling_mean = data['Glucose Value'].rolling(window=window).mean().replace(np.nan, None)
    rolling_std = data['Glucose Value'].rolling(window=window).std().replace(np.nan, None)
    
    # Prepare the data for the chart
    dataRes = {
        'original': data['Glucose Value'].tolist(),
        'rolling_mean': rolling_mean.tolist(),
        'rolling_std': rolling_std.tolist()
    }
    

    return jsonify(dataRes)


@app.route('/tir_tar_tbr', methods=['GET'])
def calculate_tir_tar_tbr():
    
    if data is None:
        return {"msg":'No data loaded'}
    # Calculate the TIR, TAR, and TBR metrics
    total_points = len(data)
    tir_points = len(data[(data['Glucose Value'] >= 70) & (data['Glucose Value'] <= 180)])
    tar_points = len(data[(data['Glucose Value'] > 180)])

    tar_points1 = len(data[(data['Glucose Value'] > 180) & (data['Glucose Value'] <= 250)])
    tar_points2 = len(data[(data['Glucose Value'] > 250)])

    tbr_points = len(data[(data['Glucose Value'] < 70)])

    tbr_points1 = len(data[(data['Glucose Value'] > 54) & (data['Glucose Value'] <= 70)])
    tbr_points2 = len(data[(data['Glucose Value'] < 54)])

    # Calculate the percentages
    tir_percentage = tir_points / total_points * 100
    tar_percentage = tar_points / total_points * 100
    tbr_percentage = tbr_points / total_points * 100

    tar1_percentage = tar_points1 / total_points * 100
    tar2_percentage = tar_points2 / total_points * 100
    tbr1_percentage = tbr_points1 / total_points * 100
    tbr2_percentage = tbr_points2 / total_points * 100

    # Prepare the data for the frontend
    dataA = {
        'tir_percentage': tir_percentage,
        'tar_percentage': tar_percentage,
        'tbr_percentage': tbr_percentage,
        'tar1_percentage': tar1_percentage,
        'tar2_percentage': tar2_percentage,
        'tbr1_percentage': tbr1_percentage,
        'tbr2_percentage': tbr2_percentage
    }

    return jsonify(dataA)


@app.route('/mage', methods=['GET'])
def MAGE(std=1):
        if data is None:
            return {"msg":'No data loaded'} 

        #extracting glucose values and incdices
        glucose = data['Glucose Value'].tolist()
        ix = [1*i for i in range(len(glucose))]
        stdev = std
        
        # local minima & maxima
        a = np.diff(np.sign(np.diff(glucose))).nonzero()[0] + 1      
        # local min
        valleys = (np.diff(np.sign(np.diff(glucose))) > 0).nonzero()[0] + 1 
        # local max
        peaks = (np.diff(np.sign(np.diff(glucose))) < 0).nonzero()[0] + 1         
        # +1 -- diff reduces original index number

        #store local minima and maxima -> identify + remove turning points
        excursion_points = pd.DataFrame(columns=['Index', 'Time', 'Glucose', 'Type'])
        k=0
        for i in range(len(peaks)):
            excursion_points.loc[k] = [peaks[i]] + [data['DisplayDtTm'][k]] + [data['Glucose Value'][k]] + ["P"]
            k+=1

        for i in range(len(valleys)):
            excursion_points.loc[k] = [valleys[i]] + [data['DisplayDtTm'][k]] + [data['Glucose Value'][k]] + ["V"]
            k+=1

        excursion_points = excursion_points.sort_values(by=['Index'])
        excursion_points = excursion_points.reset_index(drop=True)


        # selecting turning points
        turning_points = pd.DataFrame(columns=['Index', 'Time', 'Glucose', 'Type'])
        k=0
        for i in range(stdev,len(excursion_points.Index)-stdev):
            positions = [i-stdev,i,i+stdev]
            for j in range(0,len(positions)-1):
                if(excursion_points.Type[positions[j]] == excursion_points.Type[positions[j+1]]):
                    if(excursion_points.Type[positions[j]]=='P'):
                        if excursion_points.Glucose[positions[j]]>=excursion_points.Glucose[positions[j+1]]:
                            turning_points.loc[k] = excursion_points.loc[positions[j+1]]
                            k+=1
                        else:
                            turning_points.loc[k] = excursion_points.loc[positions[j+1]]
                            k+=1
                    else:
                        if excursion_points.Glucose[positions[j]]<=excursion_points.Glucose[positions[j+1]]:
                            turning_points.loc[k] = excursion_points.loc[positions[j]]
                            k+=1
                        else:
                            turning_points.loc[k] = excursion_points.loc[positions[j+1]]
                            k+=1

        if len(turning_points.index)<10:
            turning_points = excursion_points.copy()
            excursion_count = len(excursion_points.index)
        else:
            excursion_count = len(excursion_points.index)/2


        turning_points = turning_points.drop_duplicates(subset= "Index", keep= "first")
        turning_points=turning_points.reset_index(drop=True)
        excursion_points = excursion_points[excursion_points.Index.isin(turning_points.Index) == False]
        excursion_points = excursion_points.reset_index(drop=True)

        # calculating MAGE
        mage = turning_points.Glucose.sum()/excursion_count
        
        megaround = round(mage,3)
        return jsonify({"mage":megaround})
    




@app.route('/modd', methods=['GET'])
def MODD():
    global data
    if data is None:
            return {"msg":'No data loaded'} 
        
    a = data[data.columns[0]]                                               #added
    raje = pd.to_datetime(a)                                            #added
    data['Timefrommidnight'] =  raje.dt.time                              #added
    lists=[]
    for i in range(0, len(data['Timefrommidnight'])):
        lists.append(int(data['Timefrommidnight'][i].strftime('%H:%M:%S')[0:2])*60 + int(data['Timefrommidnight'][i].strftime('%H:%M:%S')[3:5]) + round(int(data['Timefrommidnight'][i].strftime('%H:%M:%S')[6:9])/60))
    data['Minfrommid'] = lists
    data = data.drop(columns=['Timefrommidnight'])
    
    #Calculation of MODD and CONGA:
    MODD_n = []
    uniquetimes = data['Minfrommid'].unique()

    for i in uniquetimes:
        MODD_n.append(uniquevalfilter(data, i))
    
    #Remove zeros from dataframe for calculation (in case there are random unique values that result in a mean of 0)
    MODD_n[MODD_n == 0] = np.nan
    
    MODD = np.nanmean(MODD_n)
    return jsonify({"modd":MODD})

#MODD
def uniquevalfilter(dtA, value):
        
    xdf = dtA[data['Minfrommid'] == value]
    n = len(xdf)
    a = dtA[dtA.columns[1]]      ##added
    diff = abs(a.diff())
    MODD_n = np.nanmean(diff)
    return MODD_n



# def CONGA24(df):
    
#     data = pd.read_csv('D:\Life 2020\Rajeswari Files\Data\BolusinsulinNN\CGM analyzation\PatientID_23.csv')
#     df = pd.DataFrame(data)                                             #added
#     a = df[df.columns[0]]                                               #added
#     raje = pd.to_datetime(a)                                            #added
#     df['Timefrommidnight'] =  raje.dt.time                              #added
   
#  #   df['Timefrommidnight'] =  df['Time'].dt.time
#     lists=[]
#     for i in range(0, len(df['Timefrommidnight'])):
#         lists.append(int(df['Timefrommidnight'][i].strftime('%H:%M:%S')[0:2])*60 + int(df['Timefrommidnight'][i].strftime('%H:%M:%S')[3:5]) + round(int(df['Timefrommidnight'][i].strftime('%H:%M:%S')[6:9])/60))
#     df['Minfrommid'] = lists
#     df = df.drop(columns=['Timefrommidnight'])
    
#     #Calculation of MODD and CONGA:
#     MODD_n = []
#     uniquetimes = df['Minfrommid'].unique()

#     for i in uniquetimes:
#         MODD_n.append(uniquevalfilter(df, i))
    
#     #Remove zeros from dataframe for calculation (in case there are random unique values that result in a mean of 0)
#     MODD_n[MODD_n == 0] = np.nan
    
#     CONGA24 = np.nanstd(MODD_n)
#     return CONGA24


# print('CONGA24 is: ' + str(CONGA24(data))) 
@app.route('/conga', methods=['GET'])
def CONGA24():
    global data
    if data is None:
            return {"msg":'No data loaded'} 
    
    a = data[data.columns[0]]                                               #added
    raje = pd.to_datetime(a)                                            #added
    data['Timefrommidnight'] =  raje.dt.time                              #added
   
 #   df['Timefrommidnight'] =  df['Time'].dt.time
    lists=[]
    for i in range(0, len(data['Timefrommidnight'])):
        lists.append(int(data['Timefrommidnight'][i].strftime('%H:%M:%S')[0:2])*60 + int(data['Timefrommidnight'][i].strftime('%H:%M:%S')[3:5]) + round(int(data['Timefrommidnight'][i].strftime('%H:%M:%S')[6:9])/60))
    data['Minfrommid'] = lists
    data = data.drop(columns=['Timefrommidnight'])
    
    #Calculation of MODD and CONGA:
    MODD_n = []
    uniquetimes = data['Minfrommid'].unique()

    for i in uniquetimes:
        MODD_n.append(uniquevalfilter(data, i))
    
    #Remove zeros from dataframe for calculation (in case there are random unique values that result in a mean of 0)
    MODD_n[MODD_n == 0] = np.nan
    
    CONGA24 = np.nanstd(MODD_n)
    return jsonify({"conga":CONGA24})


@app.route('/gv', methods=['GET'])
def gv():
    global data
    if data is None:
            return {"msg":'No data loaded'} 
        
    data['Time'] = pd.to_datetime(data['DisplayDtTm'])
    data['Glucose'] = pd.to_numeric(data['Glucose Value'])
    data = data.iloc[12:]  # Skip the first 12 rows
    data.reset_index(drop=True, inplace=True)
    data['Day'] = data['Time'].dt.date
    cvx = (np.std(data['Glucose']) / np.mean(data['Glucose'])) * 100
    
    return jsonify({"gv":cvx})


@app.route('/hyperglycemic_trends', methods=['GET']) #d
def hyperglycemic_trends():
    # Read the data and set the upper and lower bounds
    if data is None:
            return {"msg":'No data loaded'} 
    upper_bound = 500
    lower_bound = 180

    # Filter the data based on the upper and lower bounds
    filtered_data = data[(data['Glucose Value'] <= upper_bound) | (data['Glucose Value'] >= lower_bound)]
    print(filtered_data,"FILTERRRRR")
    # date_string = "Sun, 14 Jun 2009 08:31:00 GMT"
    date_format = "%a, %d %b %Y %H:%M:%S %Z"
    date = pd.to_datetime(data['DisplayDtTm'],dayfirst=True)
    testlen = len(filtered_data['Glucose Value'].tolist())
    # Prepare the data for scatterplot
    if testlen == 0:
        scatter_data = {
            'time': date.tolist(),
            'glucose': filtered_data['Glucose Value'].tolist(),
            'upper_bound': [upper_bound] * len(filtered_data),
            'lower_bound': [lower_bound] * len(filtered_data),
            "msg":"patent is not experiencing hyperglycemic condition"
        }
        # Prepare the data for scatterplot
        return jsonify(scatter_data)
    scatter_data = {
            'time': date.tolist(),
            'glucose': filtered_data['Glucose Value'].tolist(),
            'upper_bound': [upper_bound] * len(filtered_data),
            'lower_bound': [lower_bound] * len(filtered_data)
        }

    # Return the scatterplot data as JSON
    return jsonify(scatter_data)



@app.route('/hypoloycemic_trends', methods=['GET']) #d
def hypoloycemic_trends():
    # Read the data and set the upper and lower bounds
    if data is None:
            return {"msg":'No data loaded'} 
    upper_bound = 70
    lower_bound = 20

    # Filter the data based on the upper and lower bounds
    filtered_data = data[(data['Glucose Value'] <= upper_bound) | (data['Glucose Value'] <= lower_bound)]
    # date_string = "Sun, 14 Jun 2009 08:31:00 GMT"
    # date_format = "%a, %d %b %Y %H:%M:%S %Z"
    date = pd.to_datetime(data['DisplayDtTm'],dayfirst=True)
    print(filtered_data['Glucose Value'])
    testlen = len(filtered_data['Glucose Value'].tolist())
    if testlen == 0:
        scatter_data = {
            'time': date.tolist(),
            'glucose': filtered_data['Glucose Value'].tolist(),
            'upper_bound': [upper_bound] * len(filtered_data),
            'lower_bound': [lower_bound] * len(filtered_data),
            "msg":"patent is not experiencing hypoloycemic condition"
        }
        # Prepare the data for scatterplot
        return jsonify(scatter_data)
    scatter_data = {
            'time': date.tolist(),
            'glucose': filtered_data['Glucose Value'].tolist(),
            'upper_bound': [upper_bound] * len(filtered_data),
            'lower_bound': [lower_bound] * len(filtered_data)
        }

    # Return the scatterplot data as JSON
    return jsonify(scatter_data)

@app.route('/morning_trends', methods=['GET']) #d
def generate_morning_trends():
    global data
    if data is None:
            return {"msg":'No data loaded'} 
    # Filter the 'Morning' data
    morning_data = data.iloc[0:136]

    # Prepare the data for the chart
    chart_data = {
        'labels': morning_data['DisplayDtTm'].tolist(),
        'values': morning_data['Glucose Value'].tolist()
    }

    return jsonify(chart_data)

@app.route('/afternoon_trends', methods=['GET']) #d
def generate_afternoon_trends():
    
    if data is None:
            return {"msg":'No data loaded'} 
    # Filter the 'Morning' data
    morning_data = data.iloc[137:194]

    # Prepare the data for the chart
    chart_data = {
        'labels': morning_data['DisplayDtTm'].tolist(),
        'values': morning_data['Glucose Value'].tolist()
    }

    return jsonify(chart_data)


@app.route('/night_trends', methods=['GET']) #d
def generate_night_trends():
    
    if data is None:
            return {"msg":'No data loaded'} 
    # Filter the 'Morning' data
    morning_data = data.iloc[195:274,:]

    # Prepare the data for the chart
    chart_data = {
        'labels': morning_data['DisplayDtTm'].tolist(),
        'values': morning_data['Glucose Value'].tolist()
    }

    return jsonify(chart_data)


@app.route('/glucose_trend', methods=['GET']) #d
def glucose_trend():
    # Calculate the aggregate values
    global data
    if data is None:
            return {"msg":'No data loaded'} 
        
    data['Aggregate'] = [180 if glucose_val >= 180 else 70 if glucose_val <= 70 else 110 for glucose_val in data['Glucose Value']]
    
    # Prepare the data for frontend
    data2 = {
        'labels': data['DisplayDtTm'].tolist(),
        'glucose_values': data['Glucose Value'].tolist(),
        'aggregate_values': data['Aggregate'].tolist()
    }
    
    return jsonify(data2)


if __name__ == '__main__':
    app.run()
