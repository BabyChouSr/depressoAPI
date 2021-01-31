import snscrape.modules.twitter as sntwitter
import csv
csvFile = open('data.csv', 'a', newline='', encoding='utf8')
csvWriter = csv.writer(csvFile)
#csvWriter.writerow(['id','date','tweet','class']) 

depressed = 1
normal = 0

# @depressionnote
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:@depressionnote + since:2017-01-01 until:2021-01-29 -filter:links -filter:replies').get_items()):
#     csvWriter.writerow([tweet.id, tweet.date, tweet.content, depressed])

# #depressionquotes worthless
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('#depressionquotes + since:2014-01-01 until:2021-01-29 -filter:links -filter:replies').get_items()):
#     csvWriter.writerow([tweet.id, tweet.date, tweet.content, depressed])

# #suicidal
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('#suicidal + since:2014-01-01 until:2021-01-29 -filter:links -filter:replies').get_items()):
#     csvWriter.writerow([tweet.id, tweet.date, tweet.content, depressed])

# # happy (not done: inspirational, strength)
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('#happy + since:2014-01-01 until:2021-01-29 -filter:links -filter:replies').get_items()):
#     csvWriter.writerow([tweet.id, tweet.date, tweet.content, normal])

# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('#worthless + since:2014-01-01 until:2021-01-29 -filter:links -filter:replies').get_items()):
#     csvWriter.writerow([tweet.id, tweet.date, tweet.content, depressed])

for i,tweet in enumerate(sntwitter.TwitterSearchScraper('#positivity + since:2014-01-01 until:2021-01-29 -filter:links -filter:replies').get_items()):
    csvWriter.writerow([tweet.id, tweet.date, tweet.content, normal])
csvFile.close()