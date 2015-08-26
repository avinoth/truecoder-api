import webapp2
from google.appengine.api import urlfetch
import json
from collections import Counter
import logging

class MainPage(webapp2.RequestHandler):
  def get(self):
    user_id = self.request.get('user_id')
    if user_id:
      client_id = self.request.get('client_id')
      client_secret = self.request.get('client_secret')
      url = "https://api.github.com/users/" + user_id + "/repos" + '?client_id=' + client_id + '&client_secret=' + client_secret
      data = json.dumps(fetch_count(url, client_id, client_secret))
    else:
      data = json.dumps({'error': 'Error - User ID Not Found'})
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(data)

def fetch_count(url, client_id, client_secret):
  loc_dict = Counter({})
  result = urlfetch.fetch(url)
  if result.status_code != 200:
    if client_id and client_secret:
      data = {'error': 'Error from Github - ' + str(result.status_code)}
    if result.status_code == 403:
      data = {'error': 'Reached github rate limit. Try providing client_id and client_secret'}
    return data
  payload = json.loads(result.content)

  for repo in payload:
    language_url = repo['languages_url'] + '?client_id=' + client_id + '&client_secret=' + client_secret
    loc = Counter(get_loc(language_url))
    loc_dict += loc
  if client_id and client_secret:
    return loc_dict
  else:
    return loc_dict + Counter({'notice': 'Client ID or Client Secret is not provided. Hence count is calculated as far as the github served because the rate limit.'})

def get_loc(url):
  result = urlfetch.fetch(url)
  if result.status_code != 200:
    return {}
  else:
    return json.loads(result.content)


app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
