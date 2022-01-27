import os
import csv


def write(x, name):
    with open(name+'.csv', 'r') as read_obj, \
            open('ActiveLearning_update.csv', 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = csv.reader(read_obj, delimiter=',')
        # Create a csv.writer object from the output file object
        csv_writer = csv.writer(write_obj, delimiter=',')
        # Read each row of the input csv file as list
        j = 0
        for row in csv_reader:
            i = len(row)
            if j == 0:
                row.append("eval_"+str(i-3))
                j += 1
            elif j == 1:
                # Append the default text in the row / list
                row.append(x[0])
                j += 1
            elif j == 2 or j == 3:
                # Append the default text in the row / list
                row.append(x[1])
                j += 1
            elif j == 4 or 11.5 < j < 16.5:
                # Append the default text in the row / list
                row.append(0)
                j += 1
            elif 4.5 < j < 7.5:
                # Append the default text in the row / list
                row.append(x[2])
                j += 1
            elif 7.5 < j < 11.5:
                # Append the default text in the row / list
                row.append(x[3])
                j += 1
            else:
                # Append the default text in the row / list
                row.append(x[j-13])
                j += 1
            # Add the updated row / list to the output file
            csv_writer.writerow(row)
    os.remove(name+".csv")
    os.rename("ActiveLearning_update.csv", name+".csv")
    return i


def write_results(x):
    # [density, paraffins, naphtenes, aromatics, Tdist, TRO1, TRO2, Hprot1, Hprot2, PRO1, PRO2]
    with open('ActiveLearning.csv', 'r') as read_obj, \
            open('ActiveLearning_update.csv', 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = csv.reader(read_obj, delimiter=',')
        # Create a csv.writer object from the output file object
        csv_writer = csv.writer(write_obj, delimiter=',')
        # Read each row of the input csv file as list
        j = 0
        for row in csv_reader:
            i = len(row)
            if j == 0:
                row.append("eval_"+str(i))
                j += 1
            elif j == 1:
                # Append the default text in the row / list
                row.append(x[0])
                j += 1
            elif j == 2 or j == 3:
                # Append the default text in the row / list
                row.append(x[1])
                j += 1
            elif j == 4 or 11.5 < j < 16.5:
                # Append the default text in the row / list
                row.append(0)
                j += 1
            elif 4.5 < j < 7.5:
                # Append the default text in the row / list
                row.append(x[2])
                j += 1
            elif 7.5 < j < 11.5:
                # Append the default text in the row / list
                row.append(x[3])
                j += 1
            else:
                # Append the default text in the row / list
                row.append(x[j-13])
                j += 1
            # Add the updated row / list to the output file
            csv_writer.writerow(row)
    os.remove("ActiveLearning.csv")
    os.rename("ActiveLearning_update.csv", "ActiveLearning.csv")
    return i
