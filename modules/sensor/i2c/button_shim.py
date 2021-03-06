import buttonshim


#button functions
def FUNC_A():
  pass
def FUNC_B():
  pass
def FUNC_C():
  pass
def FUNC_D():
  pass
def FUNC_E():
  pass
def FUNC_A_LONG():
  pass
def FUNC_B_LONG():
  pass
def FUNC_C_LONG():
  pass
def FUNC_D_LONG():
  pass
def FUNC_E_LONG():
  pass
def DUMMY():
  pass

#access from decorator
_HOLD_STATUS = {
  'A': False,
  'B': False,
  'C': False,
  'D': False,
  'E': False,
}


class ButtonShim():

  config = None
  pre_index = -1

  def __init__(self, config):
    self.config = config
    buttonshim.set_pixel(0x00, 0x00, 0x00)

  def set_func(self):
    global FUNC_A, FUNC_B, FUNC_C, FUNC_D, FUNC_E, FUNC_A_LONG, FUNC_B_LONG, FUNC_C_LONG, FUNC_D_LONG, FUNC_E_LONG
    if self.config.gui == None:
      return
    if self.config.gui.stack_widget == None:
      return
    s = self.config.gui.stack_widget
    i = s.currentIndex()
    b = self.config.G_GPIO_BUTTON_DEF['Button_Shim']
    
    m = 'MAIN'
    if i == 1:
      m = 'MAIN'
    elif i >= 0:
      m = 'MENU'
    
    if i != self.pre_index:
      FUNC_A = eval('self.config.gui.'+b[m]['A'][0])
      FUNC_B = eval('self.config.gui.'+b[m]['B'][0])
      FUNC_C = eval('self.config.gui.'+b[m]['C'][0])
      FUNC_D = eval('self.config.gui.'+b[m]['D'][0])
      FUNC_E = eval('self.config.gui.'+b[m]['E'][0])
      
      FUNC_A_LONG = eval('self.config.gui.'+b[m]['A'][1])
      FUNC_B_LONG = eval('self.config.gui.'+b[m]['B'][1])
      FUNC_C_LONG = eval('self.config.gui.'+b[m]['C'][1])
      FUNC_D_LONG = eval('self.config.gui.'+b[m]['D'][1])
      FUNC_E_LONG = eval('self.config.gui.'+b[m]['E'][1])

    self.pre_index = i

  # Button A
  @buttonshim.on_press(buttonshim.BUTTON_A)
  def press_handler_a(button, pressed):
    global _HOLD_STATUS
    _HOLD_STATUS['A'] = False

  @buttonshim.on_release(buttonshim.BUTTON_A)
  def release_handler_a(button, pressed):
    global FUNC_A
    if not _HOLD_STATUS['A']:
      FUNC_A()

  @buttonshim.on_hold(buttonshim.BUTTON_A, hold_time=2)
  def hold_handler_a(button):
    global _HOLD_STATUS, FUNC_A_LONG
    _HOLD_STATUS['A'] = True
    FUNC_A_LONG()

  # Button B
  @buttonshim.on_press(buttonshim.BUTTON_B)
  def press_handler_b(button, pressed):
    global _HOLD_STATUS
    _HOLD_STATUS['B'] = False

  @buttonshim.on_release(buttonshim.BUTTON_B)
  def release_handler_b(button, pressed):
    global FUNC_B
    if not _HOLD_STATUS['B']:
      FUNC_B()

  @buttonshim.on_hold(buttonshim.BUTTON_B, hold_time=2)
  def hold_handler_b(button):
    global _HOLD_STATUS, FUNC_B_LONG
    _HOLD_STATUS['B'] = True
    FUNC_B_LONG()

  # Button C
  @buttonshim.on_press(buttonshim.BUTTON_C)
  def press_handler_c(button, pressed):
    global _HOLD_STATUS
    _HOLD_STATUS['C'] = False

  @buttonshim.on_release(buttonshim.BUTTON_C)
  def release_handler_c(button, pressed):
    global FUNC_C
    if not _HOLD_STATUS['C']:
      FUNC_C()

  @buttonshim.on_hold(buttonshim.BUTTON_C, hold_time=2)
  def hold_handler_c(button):
    global _HOLD_STATUS, FUNC_C_LONG
    _HOLD_STATUS['C'] = True
    FUNC_C_LONG()

  # Button D
  @buttonshim.on_press(buttonshim.BUTTON_D)
  def press_handler_d(button, pressed):
    global _HOLD_STATUS
    _HOLD_STATUS['D'] = False

  @buttonshim.on_release(buttonshim.BUTTON_D)
  def release_handler_d(button, pressed):
    global FUNC_D
    if not _HOLD_STATUS['D']:
      FUNC_D()

  @buttonshim.on_hold(buttonshim.BUTTON_D, hold_time=2)
  def hold_handler_d(button):
    global _HOLD_STATUS, FUNC_D_LONG
    _HOLD_STATUS['D'] = True
    FUNC_D_LONG()

  # Button E
  @buttonshim.on_press(buttonshim.BUTTON_E)
  def press_handler_e(button, pressed):
    global _HOLD_STATUS
    _HOLD_STATUS['E'] = False

  @buttonshim.on_release(buttonshim.BUTTON_E)
  def release_handler_e(button, pressed):
    global FUNC_E
    if not _HOLD_STATUS['E']:
      FUNC_E()

  @buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=2)
  def hold_handler_e(button):
    global _HOLD_STATUS, FUNC_E_LONG
    _HOLD_STATUS['E'] = True
    FUNC_E_LONG()

