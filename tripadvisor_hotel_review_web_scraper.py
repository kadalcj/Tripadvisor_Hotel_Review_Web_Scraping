# Some package that I use to make this web scrapper specificly for TripAdvisor Hotel Review
# Use pip to install the package
import requests
import pandas
from bs4 import BeautifulSoup

# Just for fun
import sys

# Simple GUI
print('Which hotel shall we scrape today? (url please)')
uri = input('>>> ')
print()

print('Enter the name of extracted csv:')
csvName = input('>>> ')
print()

print('Okay, let\'s go')
print()

# Just for fun
if(('https://www.tripadvisor.' in uri) == False):
    print('Are you sure about that?')
    print('Run me again.')
    sys.exit()

elif(uri == ''):
    print('Okay, maybe later.')
    sys.exit()

elif(csvName == ''):
    print('Please be serious.')
    sys.exit()

# Temp Var
reviewHotelNameList = []
reviewNameList = []
reviewDateList = []
reviewTitleList = []
reviewCommentList = []

# Just for fun
print()
print(uri)
print()

#-------------------
# Request
req = requests.get(uri)
soup = BeautifulSoup(req.text, 'html.parser')

# Check if there was an review or not
if(soup.find('div', {'class': 'hotels-hotel-review-about-noreviews-NoReviewsCTA__noReviewsYet--1OL25'}) != None):

    res = soup.find('div', {'class': 'hotels-hotel-review-about-noreviews-NoReviewsCTA__noReviewsYet--1OL25'})

    if(res.text == 'There are no reviews for this property yet.'):
        print('No Review, not interest')
        print('Bye')
        sys.exit()

# Get the max page number
if(soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'}) != []):
    res = soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'})

    maxPage = int(res[-1].text)

elif(soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'}) == []):
    if(soup.find('a', {'class': 'pageNum cx_brand_refresh_phase2'}) != None):
        res = soup.find('a', {'class': 'pageNum cx_brand_refresh_phase2'})

        maxPage = int(res.text)
    else:
        maxPage = 1

# This is the function
def scrape_data(uri, soup, maxPage):
    # Pagination Page
    currentPage = 0
    # Loop
    while currentPage in range(0, maxPage):

        getHotelName = soup.find('h1', {'class': 'hotels-hotel-review-atf-info-parts-Heading__heading--2ZOcD'})
        print('Hotel: ' + getHotelName.text)

        # Get Max Review List
        maxReview = soup.find_all('a', {'class': 'ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC'})

        # Pagination Review
        currentReviewPage = 0
        while currentReviewPage in range(0, len(maxReview)):
            # Devider
            print('------------- Review ' + str(currentReviewPage + 1) + ' -------------')

            getReviewName = soup.find_all('a', {'class': 'ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC'})[currentReviewPage]
            print('Name: ' + getReviewName.text)

            getReviewDate = soup.find_all('div', {'class': 'social-member-event-MemberEventOnObjectBlock__event_type--3njyv'})[currentReviewPage].find()
            if('.com' in uri):
                getReviewDateUpdate = getReviewDate.text.replace(getReviewName.text + ' wrote a review ', '')
            elif('.co.id' in uri):
                getReviewDateUpdate = getReviewDate.text.replace(getReviewName.text + ' menulis ulasan ', '')
            print('Date: ' + getReviewDateUpdate)

            getReviewTitle = soup.find_all('div', {'class': 'location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z'})[currentReviewPage].find('span')
            print('Title: ' + getReviewTitle.text)

            getReviewComment = soup.find_all('q', {'class': 'location-review-review-list-parts-ExpandableReview__reviewText--gOmRC'})[currentReviewPage].find('span')
            print('Comment: ' + getReviewComment.text)

            # Devider
            print('----------------------------')

            # Push to csv in every iteration
            # It will help you if there was a problem in the midle of scraping
            # But the downside is maybe it will take more resource
            reviewHotelNameList.append(getHotelName.text)
            reviewNameList.append(getReviewName.text)
            reviewDateList.append(getReviewDateUpdate)
            reviewTitleList.append(getReviewTitle.text)
            reviewCommentList.append(getReviewComment.text)

            createTable = {
                'Hotel Name': reviewHotelNameList,
                'Reviewer Name': reviewNameList,
                'Review Date': reviewDateList,
                'Review Title': reviewTitleList,
                'Review Comment': reviewCommentList
            }

            dataFrame = pandas.DataFrame(createTable, columns=['Hotel Name', 'Reviewer Name', 'Review Date', 'Review Title', 'Review Comment'])
            dataFrame.to_csv(r'./' + csvName + '.csv')
            # Move to the next review
            currentReviewPage += 1

        # Move to the next page
        currentPage += 1

        # Request to next page
        uriMove = uri.replace('Reviews-', 'Reviews-or' + str(currentPage*5) + '-')
        print(uriMove)
        # Devider
        print('------------- Page ' + str(currentPage) + '-------------')
        print()
        # Request to next page
        req = requests.get(uriMove)
        soup = BeautifulSoup(req.text, 'html.parser')

# Fetch the data
scrape_data(uri, soup, maxPage)
#END of the Loop

# Change the uri so we can get English(.com) and Bahasa(.co.id) reviews
if('.com' in uri):
    # Replace the domain to .co.id and fetch
    uri = uri.replace('.com', '.co.id')

    # Space
    print()
    print('Change url to .co.id *Review in Bahasa')
    print(uri)
    print()

    # New Request
    req = requests.get(uri)
    soup = BeautifulSoup(req.text, 'html.parser')

    # Check if there was an review or not
    if(soup.find('div', {'class': 'hotels-hotel-review-about-noreviews-NoReviewsCTA__noReviewsYet--1OL25'}) != None):

        res = soup.find('div', {'class': 'hotels-hotel-review-about-noreviews-NoReviewsCTA__noReviewsYet--1OL25'})

        if(res.text == 'There are no reviews for this property yet.'):
            print('No Review, not interest')
            print('Bye')
            sys.exit()

    # Get the max page number
    if(soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'}) != []):
        res = soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'})
        print(res)

        maxPage = int(res[-1].text)

    elif(soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'}) == []):
        if(soup.find('a', {'class': 'pageNum cx_brand_refresh_phase2'}) != None):
            res = soup.find('a', {'class': 'pageNum cx_brand_refresh_phase2'})
            print(res)

            maxPage = int(res.text)
        else:
            maxPage = 1

    scrape_data(uri, soup, maxPage)

elif('.co.id' in uri):
    # Replace the domain to .com and fetch
    uri = uri.replace('.co.id', '.com')
    
    # Space
    print()
    print('Changing to .com *Review in Enlish')
    print(uri)
    print()

    # New Request
    req = requests.get(uri)
    soup = BeautifulSoup(req.text, 'html.parser')

    # Check if there was an review or not
    if(soup.find('div', {'class': 'hotels-hotel-review-about-noreviews-NoReviewsCTA__noReviewsYet--1OL25'}) != None):

        res = soup.find('div', {'class': 'hotels-hotel-review-about-noreviews-NoReviewsCTA__noReviewsYet--1OL25'})

        if(res.text == 'There are no reviews for this property yet.'):
            print('No Review, not interest')
            print('Bye')
            sys.exit()

    # Get the max page number
    if(soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'}) != []):
        res = soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'})

        maxPage = int(res[-1].text)

    elif(soup.find_all('a', {'class': 'pageNum cx_brand_refresh_phase2'}) == []):
        if(soup.find('a', {'class': 'pageNum cx_brand_refresh_phase2'}) != None):
            res = soup.find('a', {'class': 'pageNum cx_brand_refresh_phase2'})

            maxPage = int(res.text)
        else:
            maxPage = 1

    scrape_data(uri, soup, maxPage)

# Push to the csv for final product
# If the program manage to scrape all the data without problem
createTable = {
    'Hotel Name': reviewHotelNameList,
    'Reviewer Name': reviewNameList,
    'Review Date': reviewDateList,
    'Review Title': reviewTitleList,
    'Review Comment': reviewCommentList
}

dataFrame = pandas.DataFrame(createTable, columns=['Hotel Name', 'Reviewer Name', 'Review Date', 'Review Title', 'Review Comment'])
# Set the Index from 0 to 1
dataFrame.index += 1
dataFrame.to_csv(r'./' + csvName + '.csv')

# Break. I mean 'Complete'
print()
print('Mission Complete')
#-------------------#
