import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Function to parse the date string into a datetime object
def parse_date(date_str):
    date_object = datetime.strptime(date_str, "%m/%d/%Y").date()
    return date_object

# Function to get the most recent training for each unique training name
def get_recent_training(trainings):
    latest = {}
    for training in trainings:
        training_date = parse_date(training['timestamp'])
        # Check if the training is more recent than the existing one
        if training['name'] not in latest or training_date > parse_date(latest[training['name']]['timestamp']):
            # Handle missing expiration dates by setting expiration 1 year after completion
            if training["expires"] is None:
                expiration_date = training_date + timedelta(days=365)
                training["expires"] = expiration_date.strftime("%m/%d/%Y")
            latest[training['name']] = training
    return list(latest.values())


# Function to process the data and return the required outputs
def process_trainings(file_path, fiscal_year_start, fiscal_year_end, specified_trainings, specified_date):
    # Load data from the provided file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Get processed list with latest training completions for each person
    people = []
    for person in data:
        person_info ={
            "name": person["name"],
            "completions": get_recent_training(person["completions"])
        }
        people.append(person_info)

    # Task 1: Count how many people completed each training
    training_counts = {}
    for person in people:
        for completion in person["completions"]:
            training_name = completion["name"]
            training_counts[training_name] = training_counts.get(training_name, 0) + 1

    output1 = []
    for name, count in training_counts.items():
        training_info = {"training_name": name, "count": count}
        output1.append(training_info)

    # Task 2: List people who completed specified trainings within the fiscal year
    output2 = {}
    for person in people:
        for completion in person["completions"]:
            training_name = completion["name"]
            if training_name in specified_trainings:
                completion_date = parse_date(completion["timestamp"])
                if fiscal_year_start <= completion_date <= fiscal_year_end:
                    if training_name not in output2:
                        output2[training_name] = []
                    output2[training_name].append(person["name"])

    # Task 3: Find people with expired or soon-to-expire trainings
    one_month_later = specified_date + relativedelta(months=1)
    output3 = []
    for person in people:
        for completion in person["completions"]:
            expiration_date = parse_date(completion["expires"])
            if expiration_date:
                if expiration_date < specified_date:
                    status = "Expired"
                elif specified_date <= expiration_date <= one_month_later:
                    status = "Expires Soon"
                else:
                    continue
                output3.append({
                    "name": person["name"],
                    "training_name": completion["name"],
                    "expiration_date": expiration_date.strftime("%m/%d/%Y"),
                    "status": status
                })

    return output1, output2, output3

# Main function to run the app
def main():
    # Define file path and parameters
    file_path = 'trainings.txt'
    fiscal_year_start = datetime(2023, 7, 1).date()
    fiscal_year_end = datetime(2024, 6, 30).date()
    specified_trainings = {"Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"}
    specified_date = datetime(2023, 10, 1).date()

    # Process the training data and get outputs
    output1, output2, output3 = process_trainings(file_path, fiscal_year_start, fiscal_year_end, specified_trainings, specified_date)

    # Save the outputs to JSON files
    with open('output1.json', 'w') as f:
        json.dump(output1, f, indent=4)
    with open('output2.json', 'w') as f:
        json.dump(output2, f, indent=4)
    with open('output3.json', 'w') as f:
        json.dump(output3, f, indent=4)

    print("Outputs have been saved to 'output1.json', 'output2.json', and 'output3.json'.")

# Run the main function
if __name__ == "__main__":
    main()