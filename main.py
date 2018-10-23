import amazon_service
import datetime
import time
import json

if __name__ == "__main__":
    extracted_data = []

    # Get input from key down
    keyword = raw_input("Enter your idea? ")
    key = keyword
    type(keyword)

    # replace <space> with a +
    keyword = keyword.replace(" ", "+")

    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    suggestions = amazon_service.getAllKeywords(key)
    # suggestions = getSuggestedKeywords(keyword)
    print (suggestions)


    for suggestion in suggestions:
        extracted_data.append(amazon_service.getBookBasicDetails(suggestion))

    f = open(key+'.json', 'w')
    json.dump(extracted_data, f, indent=4)

    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
