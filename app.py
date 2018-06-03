import gdax, time, json, time
import numpy as np
import gnuplotlib as gp
from dateutil import parser

import warnings
warnings.simplefilter('ignore', np.RankWarning)


product = "ETH-USD"


class myWebsocketClient(gdax.WebsocketClient):
  def on_open(self):
    self.url = "wss://ws-feed.gdax.com/"
    self.products = [product]
    self.start_time = time.time()
    self.sales = []
  def on_message(self, msg):
    if msg["type"] == "match":
      #print (json.dumps(msg, indent=2, sort_keys=True))
      t = parser.parse(msg["time"])
      x = time.mktime(t.timetuple()) + t.microsecond / 1E6
      #x = time.time()
      y = float(msg["price"])
      self.sales.append((x,y))
  def on_close(self):
    print("-- Goodbye! --")

def derivitive(coefs):
  new_coefs = []
  max_power = len(coefs) - 1
  for i in range(0, (len(coefs) - 1)):
    new_coefs.append(coefs[i]*(max_power - i))
  return new_coefs

def solve_for(coefs, x):
  result = 0
  max_power = len(coefs) - 1
  for i in range(0, len(coefs)):
    result = result + (coefs[i]*(x**(max_power - i)))
  return result


wsClient = myWebsocketClient()
wsClient.start()
while True:
  time.sleep(3)
  if len(wsClient.sales) > 2:
    min_time = time.time() - 18000
    recent = [x for x in wsClient.sales if x[0] >= min_time]
    times, prices = zip(*recent)
    measured_x = np.array([abs(t - wsClient.start_time) for t in times])
    measured_y = np.array(prices)

    fitted_coefs = np.polyfit(measured_x, measured_y, 10)
    total_range = range(int(measured_x[0]), int(measured_x[-1]))

    fitted_y = [solve_for(fitted_coefs, v) for v in total_range]

    # d1 = derivitive(coefs)
    # d1y = [solve_for(d1, v) for v in total_range]

    gp.plot(
    (np.array(measured_x), np.array(measured_y), {"legend": "Actual"}),
    (np.array(total_range), np.array(fitted_y), {"legend": "Fit"}),
    #(np.array(x), np.array(d1y), {"legend": "D1"}),
      terminal = 'dumb 400 100',
      unset    = 'grid',
      ascii    = 1)
wsClient.close()
