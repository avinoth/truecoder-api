import webapp2
from google.appengine.api import urlfetch
import json

class MainPage(webapp2.RequestHandler):
  def get(self):
    url = "https://api.github.com/users/avinoth/repos"
    result = urlfetch.fetch(url)
    if result.status_code != 200:
      data = {'status': 'Error from Github - ' + str(result.status_code)}
    else:
      payload = json.loads(result.content)
      data = payload[0]['name']
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(data)

app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
