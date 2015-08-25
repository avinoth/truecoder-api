import webapp2
from google.appengine.api import urlfetch
import json
from collections import Counter

class MainPage(webapp2.RequestHandler):
  def get(self):
    user_id = 'avinoth'
    url = "https://api.github.com/users/" + user_id + "/repos"
    data = fetch_count(url)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(data)

  def fetch_count(url):
    loc_dict = Counter({})
    result = urlfetch.fetch(url)
    if result.status_code != 200:
      data = {'status': 'Error from Github - ' + str(result.status_code)}
      return data
    payload = json.loads(result.content)

    for repo in payload:
      language_url = repo['language_url']
      loc = Counter(get_loc(language_url))
      loc_dict += loc
    return loc_dict

  def get_loc(url):
    result = urlfetch.fetch(url)
    if result.status_code != 200:
      return {}
    else:
      return json.loads(result.content)


app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
