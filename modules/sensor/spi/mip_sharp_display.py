import time
#import datetime

import numpy as np


_SENSOR_DISPLAY = False
try:
  import pigpio
  _SENSOR_DISPLAY = True
except:
  pass
print('  MIP SHARP DISPLAY : ',_SENSOR_DISPLAY)

# https://qiita.com/hishi/items/669ce474fcd76bdce1f1

#GPIO.BCM
GPIO_DISP = 27 #13 in GPIO.BOARD
GPIO_SCS = 22 #15 in GPIO.BOARD
GPIO_VCOMSEL = 17 #11 in GPIO.BOARD

#update mode
UPDATE_MODE = 0x80


class MipSharpDisplay():

  config = None
  pi = None
  spi = None
  interval = 0.25

  def __init__(self, config):
    
    self.config = config

    if not _SENSOR_DISPLAY:
      return

    self.pi = pigpio.pi()
    #self.spi = self.pi.spi_open(0, 2000000, 0)
    self.spi = self.pi.spi_open(0, 8000000, 0) #overclocking
    time.sleep(0.1)     #Wait
    
    self.pi.set_mode(GPIO_DISP, pigpio.OUTPUT)
    self.pi.set_mode(GPIO_SCS, pigpio.OUTPUT)
    self.pi.set_mode(GPIO_VCOMSEL, pigpio.OUTPUT)

    self.pi.write(GPIO_SCS, 0)
    self.pi.write(GPIO_DISP, 1)
    self.pi.write(GPIO_VCOMSEL, 1)
    time.sleep(0.1)

    self.buff_width = int(self.config.G_WIDTH/8)+2
    self.img_buff_rgb8 = np.empty((self.config.G_HEIGHT,int(self.config.G_WIDTH/8)+2), dtype='uint8')
    self.pre_img = np.zeros((self.config.G_HEIGHT,int(self.config.G_WIDTH/8)+2), dtype='uint8')
    self.img_buff_rgb8[:,0] = UPDATE_MODE
    #address is set in reversed bits
    self.img_buff_rgb8[:,1] = [int('{:08b}'.format(a)[::-1], 2) for a in range(self.config.G_HEIGHT)]
    if self.config.G_HEIGHT > 255: 
      #self.img_buff_rgb8[:,0] = self.img_buff_rgb8[:,0] + (img_buff_rgb8[:,1] >> 8)
      self.img_buff_rgb8[:,0] = self.img_buff_rgb8[:,0] + (np.arange(self.config.G_HEIGHT) >> 8)
    
    #self.clear()
  
  def clear(self):
    self.pi.write(GPIO_SCS, 1)
    time.sleep(0.000006)
    self.pi.spi_write(self.spi, [0b00100000,0]) # ALL CLEAR MODE
    self.pi.write(GPIO_SCS, 0)
    time.sleep(0.000006)
  
  def no_update(self):
    self.pi.write(GPIO_SCS, 1)
    time.sleep(0.000006)
    self.pi.spi_write(self.spi, [0b00000000,0]) # NO UPDATE MODE
    self.pi.write(GPIO_SCS, 0)
    time.sleep(0.000006)

  def blink(self, sec):
    if not _SENSOR_DISPLAY:
      return
    s = sec
    state = True
    while s > 0:
      self.pi.write(GPIO_SCS, 1)
      time.sleep(0.000006)
      if state:
        self.pi.spi_write(self.spi, [0b00010000,0]) # BLINK(BLACK) MODE
      else:
        self.pi.spi_write(self.spi, [0b00011000,0]) # BLINK(WHITE) MODE
      self.pi.write(GPIO_SCS, 0)
      time.sleep(self.interval)
      s -= self.interval
      state = not state
    self.no_update()

  def inversion(self, sec):
    if not _SENSOR_DISPLAY:
      return
    s = sec
    state = True
    while s > 0:
      self.pi.write(GPIO_SCS, 1)
      time.sleep(0.000006)
      if state:
        self.pi.spi_write(self.spi, [0b00010100,0]) # INVERSION MODE
      else:
        self.no_update()
      self.pi.write(GPIO_SCS, 0)
      time.sleep(self.interval)
      s -= self.interval
      state = not state
    self.no_update()

  def update(self, image):

    im_array = np.array(image.convert("1"))

    #t = datetime.datetime.now()
    
    #update
    self.img_buff_rgb8[:,2:] = np.packbits(
      im_array.astype('uint8').reshape(self.config.G_HEIGHT, self.config.G_WIDTH),
      axis=1
      )
    img_bytes = bytearray()

    #differential update
    rewrite_flag = True
    diff_lines = np.where(np.sum((self.img_buff_rgb8 == self.pre_img), axis=1) != self.buff_width)[0] 
    #print("diff ", int(len(diff_lines)/self.config.G_HEIGHT*100), "%")
    #print(" ")
    img_bytes = self.img_buff_rgb8[diff_lines].tobytes()
    if len(diff_lines) == 0:
      rewrite_flag = False
    self.pre_img[diff_lines] = self.img_buff_rgb8[diff_lines]

    #print("Loading images... :", (datetime.datetime.now()-t).total_seconds(),"sec")
    #t = datetime.datetime.now()
    
    if _SENSOR_DISPLAY and rewrite_flag and not self.config.G_QUIT:
      self.pi.write(GPIO_SCS, 1)
      time.sleep(0.000006)
      if len(img_bytes) > 0:
        self.pi.spi_write(self.spi, img_bytes)
      #dummy output for ghost line
      self.pi.spi_write(self.spi, [0x00000000,0])
      self.pi.write(GPIO_SCS, 0)

    #print("Drawing images... :", (datetime.datetime.now()-t).total_seconds(),"sec")
  
  def quit(self):
    if not _SENSOR_DISPLAY:
      return
    self.clear()
    self.pi.write(GPIO_DISP, 1)
    time.sleep(0.1)

    self.pi.spi_close(self.spi)
    self.pi.stop()

