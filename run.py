from glassdoor import Glassdoor
import time

url = ''	#put link to company review first page here. e.g. http://www.glassdoor.com/Reviews/Amazon-com-Reviews-E6036.htm
output_filename = 'reviews.csv'

all_reviews = []

page_count = 1
page_total = 2	#put the total page you want to extract here

start = time.time()
print 'Starting Driver and logging in to Glassdoor...',
GD = Glassdoor()
print time.time()-start, 'seconds'

start = time.time()
print 'Getting reviews page 1...', 
GD.get_review_page_source(url)
print 'parsing...',
reviews = GD.parse_reviews_page()
print len(reviews), 'reviews found on this page.',
all_reviews.extend(reviews)
print time.time()-start, 'seconds'
page_count+=1

next = True
while next:
    start = time.time()
    next = GD.get_next_page()
    if next:
        print 'Getting reviews page %s...'%(page_count), 
        GD.get_review_page_source(next)
        print 'parsing...',
        reviews = GD.parse_reviews_page()
        print len(reviews), 'reviews found on this page.',
        all_reviews.extend(reviews)
        page_count +=1
	if page_count >= page_total:
		next = False;
    print time.time()-start, 'seconds'



start = time.time()
print 'Writing results to %s'%output_filename

#order_of_things = ["headline", "rating", "position", "status", 
#                    "location", "date", "misc", "cons",
#                    "pros", "management_advice", 
#                    "recommends", "outlook", 
#                    "approves_ceo"]
					
order_of_things = ["date","headline", "rating","status", "job_title",
                    "location","misc", "cons",
                    "pros", "management_advice", 
                    "recommends", "outlook", 
                    "approves_ceo"]

with open(output_filename, 'w') as f:
    headings = ','.join(order_of_things)
    f.write(headings+'\n')
    for review in all_reviews:
        line = ''
        for item in order_of_things:
            if review[item] == None:
                review[item] = str(review[item])
            review[item] = review[item].replace(',', ' ')
            review[item] = review[item].replace('-', '|')
            line+=review[item].encode('utf-8', errors='ignore')+','
        line.strip(',')
        f.write(line+'\n')
print time.time()-start, 'seconds'
print 'Completed Successfully, Exiting...'








