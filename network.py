import tweepy
import pandas as pd
from queue import Queue
q = Queue()

# API Authentication

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# Output details
out_user = r'/path/user_details.csv'
out_followers = r'/path/followers.csv'
out_skip = r'/path/skip.csv'

# Setting up data frames with initial user
user = api.get_user('')
user_details = {'name':user.name,
     'screen_name':user.screen_name,
     'created_at':str(user.created_at),
     'id':user.id,
     'friends_count':user.friends_count,
     'followers_count':user.followers_count}
master_followers = pd.DataFrame({'id':user.id,'followers':user.followers_ids()})
master_user_details = pd.DataFrame([user_details])

# Setting up skip_listlist
skip_list = []
skip_list.append(user_details['id'])
skip_df = pd.DataFrame({'id':user.id},index=[0])

# Exporting initial master files
master_user_details.to_csv(out_user,index=False)
master_followers.to_csv(out_followers,index=False)
skip_df.to_csv(out_skip,index=False)

# Putting initial follower seed in queue
list(map(q.put,master_followers['followers']))
print (len(list(q.queue)))

while not q.empty():
    u = q.get()
    if u in skip_list:
        continue
    else:
            try:
                # API call to get user data
                user = api.get_user(u)
                user_details = {'name':user.name,
                                'screen_name':user.screen_name,
                                'created_at':str(user.created_at),
                                'id':user.id,
                                'friends_count':user.friends_count,
                                'followers_count':user.followers_count}
                
                # Adding to skip list
                skip_list.append(user_details['id'])
                skip_df = pd.DataFrame({'id':user.id},index=[0])
                
                # Appending user data to master list
                user_details = pd.DataFrame([user_details])
                master_user_details = master_user_details.append(user_details)
                
                # Getting followers and appending to master list
                followers = pd.DataFrame({'id':user.id,'followers':user.followers_ids()})
                if followers.shape[0] > 200:
                    followers = followers.sample(200)
                else:
                    pass
                master_followers = master_followers.append(followers)
                
                # Adding retrieved followers to queue
                list(map(q.put,followers['followers']))
                            
                # Exporting user and followers to CSV
                user_details.to_csv(out_user,index=False,mode='a',header=False)
                followers.to_csv(out_followers,index=False,mode='a',header=False)
                skip_df.to_csv(out_skip,index=False,mode='a',header=False)
                
                print (len(list(q.queue)))
                
            # Error handling
            except tweepy.TweepError as error:
                print (type(error))
        
                if str(error) == 'Not authorized.':
                    print ('Can''t access user data - not authorized.')
                    skip_list.append(u)
                    skip_df = pd.DataFrame({'id':u},index=[0])
                    skip_df.to_csv(out_skip,index=False,mode='a',header=False)
        
                if str(error) == 'User has been suspended.':
                    print ('User suspended.')
                    skip_list.append(u)
                    skip_df = pd.DataFrame({'id':u},index=[0])
                    skip_df.to_csv(out_skip,index=False,mode='a',header=False)    













