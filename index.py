from math import floor, ceil
import subprocess as sp
from time import sleep
# pylint: disable=unused-wildcard-import
from tkinter import *
import configparser

def test():
  print('teste')

class App:
  def __init__(self, master=None):
    self.frame = Frame(master)
    self.frame.pack()
    Label(master, textvariable=txt_ping, font=('Consolas','15'), fg='white', bg='darkgray').pack()
    Label(master, textvariable=txt_variance, font=('Consolas','15'), fg='white', bg='darkgray').pack()


def get_ping():
  global process, ping, root
  try:
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
      exit(0)
    if output:
      data = output.strip().decode('utf-8')
      if 'ms' in data:
        data = data.split(':')[1]
        ping = int(data.split(' ')[2:3:][0].split('=')[1].replace('ms', ''))
        pingdata(ping)
        txt_ping.set('{:<11}{:>10}'.format('ping: {}'.format(ping)[:11], ping_quality))
        txt_variance.set('{:<11}{:>10}'.format('vari: {:.3f}'.format(variance)[:11], variance_quality))
  except:
    txt_ping.set('{:<11}{:>10}'.format('ping: {}'.format(-1)[:11], 'offline'))
    txt_variance.set('{:<11}{:>10}'.format('vari: {:.3f}'.format(-1)[:11], 'offline'))

  root.after(500, get_ping)

def pingdata(ping):
  global lastTen, variance, ping_quality, variance_quality
  if(len(lastTen) > 9):
    lastTen.pop(0)
  lastTen.append(ping)

  sample = lastTen[-ceil(len(lastTen)*0.3):]
  avg = sum(sample)/len(sample)-1
  vsum = 0
  for p in sample:
    vsum += (p - avg)**2
  
  variance = (vsum / len(sample)-1)**(1/2)

  if ping <= 58:
    ping_quality = 'very good'
  elif 58 < ping <= 60:
    ping_quality = 'good'
  elif 60 < ping <= 100:
    ping_quality = 'bad'
  else:
    ping_quality = 'very bad'

  if floor(variance*100) <= 30:
    variance_quality = 'good'
  elif 30 < floor(variance*100) <= 100:
    variance_quality = 'bad'
  else:
    variance_quality = 'very bad'
  
  return (lastTen, variance, ping_quality, variance_quality, ping)

def change_server(event):
  print('test')

if __name__ == "__main__":
  config = configparser.ConfigParser()
  config.read('config.ini')
  server = config['DEFAULT']['server']
  process = sp.Popen('ping pingtest-{}.brawlhalla.com -t'.format(server), shell=True, stdout=sp.PIPE)
  ping = 0
  lastTen = []
  variance = 0
  variance_quality = 'good'
  ping_quality = 'good'

  root = Tk()
  root.title = ''

  # root.overrideredirect(True)
  root.geometry("+0+0")
  # root.lift()
  root.wm_attributes("-topmost", True)
  # root.wm_attributes("-disabled", True)
  root.wm_attributes('-alpha', 0.7)

  txt_ping = StringVar()
  txt_ping.set('0')
  txt_variance = StringVar()
  txt_variance.set('0')
  txt_server = StringVar()
  txt_server.set('brs')
  App(root)
  root.after(0, get_ping)
  root.mainloop()