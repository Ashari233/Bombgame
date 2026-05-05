#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################

# import the configs
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from PIL import Image, ImageTk, ImageSequence
from threading import Thread
from time import sleep, time
import os
import sys

#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="#0077D6")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # setup the initial "boot" GUI
        self.setupBoot()
        # store the strike popup object
        self._strikePopup = None

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
        # Centering Frame for phase statuses
        self.centerFrame = Frame(
            self,
            relief="groove",
            bg="#0077D6",
            bd=1
        )
        self.centerFrame.place(x=20, y=90, width=760, height=190)

        # Strikes Indicator
        self.STRIKES = Label(
            self,
            text="STRIKES: 3",
            fg="#000000",
            bg="#0077D6",
            font=("Courier New", 16),
            anchor="center"
        )
        self.STRIKES.place(x=620, y=10, width=160, height=40)

        # Time Machine Title Text
        self.timeMachineTitle = Label(
            self,
            text="TIME MACHINE",
            fg="#000000",
            bg="#0077D6",
            font=("Courier New", 27),
            anchor="center"
        )
        self.timeMachineTitle.place(x=190, y=10, width=420, height=50)

        # Time Machine Maintenance Mode Subtitle Text
        self.timeMachineSubtitle = Label(
            self,
            text="MAINTENANCE MODE",
            fg="#000000",
            bg="#0077D6",
            font=("Courier New", 28),
            anchor="center"
        )
        self.timeMachineSubtitle.place(x=190, y=50, width=420, height=50)

        # Title text for wires phase
        self.wiresTitleText = Label(
            self,
            text="WIRING",
            fg="#000000",
            bg="#0077D6",
            font=("Courier New", 23),
            anchor="center"
        )
        self.wiresTitleText.place(x=40, y=120, width=220, height=60)

        # Status text for wires phase
        self.wiresStatusText = Label(
            self,
            text="OPERATIONAL",
            fg="red",
            bg="#0077D6",
            font=("Courier New", 23),
            anchor="center"
        )
        self.wiresStatusText.place(x=50, y=200, width=200, height=60)

        # Title text for button phase
        self.buttonTitleText = Label(
            self,
            text="ACCESS CODE",
            fg="#000000",
            bg="#0077D6",
            font=("Courier New", 23),
            anchor="center"
        )
        self.buttonTitleText.place(x=260, y=120, width=270, height=60)

        # Status text for button phase
        self.buttonStatusText = Label(
            self,
            text="DENIED",
            fg="red",
            bg="#0077D6",
            font=("Courier New", 23),
            anchor="center"
        )
        self.buttonStatusText.place(x=300, y=200, width=200, height=60)

        # Title text for code pad phase
        self.codePadTitleText = Label(
            self,
            text="TIME CALIBR.",
            fg="#000000",
            bg="#0077D6",
            font=("Courier New", 23),
            anchor="center"
        )
        self.codePadTitleText.place(x=540, y=120, width=220, height=60)

        # Status text for code pad phase
        self.codePadStatusText = Label(
            self,
            text="COMPLETED",
            fg="red",
            bg="#0077D6",
            font=("Courier New", 23),
            anchor="center"
        )
        self.codePadStatusText.place(x=540, y=200, width=220, height=60)

        # Title text for toggles phase
        self.togglesTitleText = Label(
            self,
            text="DESTINATION YEAR:",
            fg="#000000",
            bg="#0077D6",
            font=("Courier New", 24),
            anchor="center"
        )
        self.togglesTitleText.place(relx=0.5, y=300, width=520, height=45, anchor="n")

        # Status text for toggles phase
        self.togglesStatusText = Label(
            self,
            text="0 CE",
            fg="#000000",
            bg="#0077D6",
            font=("Courier New", 24),
            anchor="center"
        )
        self.togglesStatusText.place(relx=0.5, y=345, width=520, height=45, anchor="n")
        
        # # the timer
        # self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        # self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # # the keypad passphrase
        # self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        # self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # # the jumper wires status
        # self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        # self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # # the pushbutton status
        # self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        # self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # # the toggle switches status
        # self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        # self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        # # the strikes left
        # self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        # self._lstrikes.grid(row=5, column=2, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # TODO place a gui element briefly on the screen that tells the user that they have received a strike
    def strike_display(self):
        if self._strikePopup:
            self._strikePopup.destroy()
        
        self._strikePopup = Frame(
            self,
            relief="ridge",
            bg="#0077D6",
            bd=3
        )
        self._strikePopup.place(relx=0.5, rely=0.5, anchor="center")
        
        strikeLabel = Label(
            self._strikePopup,
            text="You have received a strike!",
            fg="red",
            bg="#0077D6",
            font=("Courier New", 40, "bold"),
            padx=40,
            pady=20
        )
        strikeLabel.pack()
        
        self.after(2000, lambda: strikeLabel.destroy())
        self.after(2000, lambda: self._strikePopup.destroy())
    
    # Assistance was received from ChatGPT 5.1 Codex for gif logic
    def _load_gif_frames(self, path):
        try:
            gif = Image.open(path)
        except (OSError, FileNotFoundError):
            return []

        frames = []
        for frame in ImageSequence.Iterator(gif):
            frames.append(ImageTk.PhotoImage(frame.copy()))
        gif.close()
        return frames
    # END Assistance was received from ChatGPT 5.1 Codex for gif logic

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self.centerFrame.destroy()
        self.STRIKES.destroy()
        self.timeMachineTitle.destroy()
        self.timeMachineSubtitle.destroy()
        self.wiresTitleText.destroy()
        self.wiresStatusText.destroy()
        self.buttonTitleText.destroy()
        self.buttonStatusText.destroy()
        self.codePadTitleText.destroy()
        self.codePadStatusText.destroy()
        self.buttonStatusText.destroy()
        self.togglesTitleText.destroy()
        self.togglesStatusText.destroy()
        # self._ltimer.destroy()
        # self._lkeypad.destroy()
        # self._lwires.destroy()
        # self._lbutton.destroy()
        # self._ltoggles.destroy()
        # self._lstrikes.destroy()
        sleep(.5)
        if success:
            # Assistance was received from ChatGPT 5.1 Codex for gif logic
            warp_frames = self._load_gif_frames("warptravel.gif")
            warp_label = Label(self, bg="#000000")
            warp_label.place(relx=0.5, rely=0.5, anchor="center")

            def animate(frame_idx=0):
                if not warp_frames:
                    return
                frame = warp_frames[frame_idx % len(warp_frames)]
                warp_label.configure(image=frame)
                warp_label.image = frame
                self.after(90, animate, frame_idx + 1)

            animate()

            def finalSuccessScreen():
                warp_label.destroy()
                Label(
                    self,
                    text="You Succeeded!",
                    fg="green",
                    bg="#0077D6",
                    font=("Courier New", 48, "bold")
                ).place(relx=0.5, rely=0.5, anchor="center")

            self.after(3000, finalSuccessScreen)
            # END Assistance was received from ChatGPT 5.1 Codex for gif logic
        elif success == False: # explosion gif & failure screen
            # Assistance was received from ChatGPT 5.1 Codex for gif logic
            warp_frames = self._load_gif_frames("explosion.gif")
            warp_label = Label(self, bg="#000000")
            warp_label.place(relx=0.5, rely=0.5, anchor="center")

            def animate(frame_idx=0):
                if not warp_frames:
                    return
                frame = warp_frames[frame_idx % len(warp_frames)]
                warp_label.configure(image=frame)
                warp_label.image = frame
                self.after(90, animate, frame_idx + 1)

            animate()

            def finalSuccessScreen():
                warp_label.destroy()
                Label(
                    self,
                    text="You Failed!",
                    fg="red",
                    bg="#0077D6",
                    font=("Courier New", 48, "bold")
                ).place(relx=0.5, rely=0.5, anchor="center")

            self.after(3000, finalSuccessScreen)
            # END Assistance was received from ChatGPT 5.1 Codex for gif logic
        
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()

        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER, command=self.retry)
        self._bretry.place(relx=0.3, rely=0.7, anchor="center")
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
        self._bquit.place(relx=0.7, rely=0.7, anchor="center")

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False

# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""
        
        # Assistance for debounce related items received from ChatGPT 5.1 Codex
        self._debounce_interval = 0.15  # 100 ms
        self._last_sample = []
        self._last_time = 0
        
        # target is an array of different steps, so we need to increment through it for each step
        self._currentTarget = self._target[0]
        self._currentTargetIndex = 0

    # Assistance for debounce related items received from ChatGPT 5.1 Codex
    def _stable_keys(self):
        current = list(self._component.pressed_keys)
        now = time()

        if current == self._last_sample:
            if (now - self._last_time) >= self._debounce_interval:
                return current
        else:
            self._last_sample = current
            self._last_time = now
        return []

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # debounce
            print(self._value, self._currentTarget, list(self._component.pressed_keys))
            # Assistance for debounce related items received from ChatGPT 5.1 Codex
            stable = self._stable_keys()
            if stable:
                key = stable[0]
                self._value += str(key)
                if self._value == self._currentTarget:
                    self.checkIfDefused()
                elif self._value != self._currentTarget[:len(self._value)]:
                    self._failed = True
                    self.resetTargetIndex()
                # consume the key so it isn’t re-read on release
                self._last_sample = []
            
#             # process keys when keypad key(s) are pressed
#             if (self._component.pressed_keys):
#                 while (self._component.pressed_keys):
#                     try:
#                         # just grab the first key pressed if more than one were pressed
#                         key = self._component.pressed_keys[0]
#                     except:
#                         key = ""
#                     sleep(0.1)
#                 # log the key
#                 self._value += str(key)
#                 # the combination is correct -> phase defused
#                 if (self._value == self._currentTarget):
#                     self.checkIfDefused()
#                 # the combination is incorrect -> phase failed (strike) 
#                 elif (self._value != self._currentTarget[0:len(self._value)]):
#                     self._failed = True
#                     self.resetTargetIndex()
            sleep(0.01)
    
    def checkIfDefused(self):
        if self._currentTargetIndex == len(self._target) - 1: # final code has been entered properly
            self._defused = True
        else:
            self.incrementTargetIndex()
            
    def incrementTargetIndex(self):
        self._currentTargetIndex += 1
        self._currentTarget = self._target[self._currentTargetIndex]
        self._value = ""
    
    def resetTargetIndex(self):
        self._currentTargetIndex = 0
        self._currentTarget = self._target[self._currentTargetIndex]
        self._value = ""
    
    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)
        self._value = "11111"
#         self._lastValue = ""

    # runs the thread
    def run(self):
        self._running = True
        while (True):
            # get the jumper wire states (0->False, 1->True)
            self._value = "".join([str(int(pin.value)) for pin in self._component])
            self.checkIfDefused()
            sleep(0.1)
        self._running = False
        
    def checkIfDefused(self):
#         if self._lastValue == "" and self._value != "": # make sure lastValue is set to something
#             self._lastValue == self._value
        
        if self._value == self._target:
            self._defused = True
        elif self._value != self._target and self._value != "11111":
            print(self._value,self._target)
            self._failed = True # immediately fail, added in bomb.py logic
        
    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is number of times the button has been pressed
        self._value = 0
        # has the pushbutton been pressed before?
        self._pressed = False
        # when was the time since epoch that the pushbutton was last pressed?
        self._lastPressed = 0
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color list
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer
        # debounce variable
        # Assistance for debounce related items received from ChatGPT 5.1 Codex
        self._last_button_press_time = 0

    # runs the thread
    def run(self):
        Thread(target=self.updateButtonColor, daemon=True).start() # start flashing the Button LED based on the LED combo
        
        self._running = True
        while (self._running):
            # get the pushbutton's state
#             self._value = self
            
            # it is pressed
            if (self._component.value):
                # Assistance for debounce related items received from ChatGPT 5.1 Codex
                now = time()
                if (now - self._last_button_press_time) >= .3:
                    self._pressed = True
                    self._lastPressed = now
                    self._last_button_press_time = now
                    self._value += 1
                    print(self._value, self._target)
            else: # it is released
                # was it previously pressed?
                # has it also been two seconds since it was last pressed?
                if (self._pressed and (time() - self._lastPressed) >= 2):
                    # check the release parameters
                    # 
                    if (not self._target or self._target == self._value):
                        self._defused = True
                    else:
                        self._failed = True
                    # note that the pushbutton was released
                    self._pressed = False
            sleep(0.15)
    
    def updateButtonColor(self):
        while True:
            for pin in self._rgb: # turn back on button rgb
                pin.value = False
        
            for color in self._color:
                self._rgb[0].value = False if color == "R" else True
                self._rgb[1].value = False if color == "G" else True
                self._rgb[2].value = False if color == "B" else True
                sleep(.5)
            
            for pin in self._rgb: # turn off button rgb
                pin.value = True
                
            sleep(2)
        
    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")

# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)
        self._value = ""

    # runs the thread
    def run(self):
        self._running = True
        while (True):
            # get the toggle switch value(0->False, 1->True)
            self._value = "".join([str(int(pin.value)) for pin in self._component])
            self.checkIfDefused()
            sleep(0.1)
        self._running = False
        
    def convertToYear(self): # used in bomb.py to display final #
        operations = {"abs": False, "x2": False}
        finalValue = "0"
        if self._value[0] == "1" and self._target[0] == "1":
            finalValue = str(int(finalValue) - 1013)
        elif self._value[0] == "1":
            finalValue = str(int(finalValue) + 338)
        
        if self._value[1] == "1" and self._target[1] == "1":
            finalValue = str(int(finalValue) + 338)
        elif self._value[0] == "1" and self._target[0] == "0":
            finalValue = str(int(finalValue) - 1013)
        elif self._value[0] == "1" and self._target[2] == "0":
            operations["x2"] = True
        elif self._value[0] == "1" and self._target[3] == "0":
            operations["abs"] = True
        
        if self._value[2] == "1" and self._target[2] == "1":
            operations["x2"] = True
        elif self._value[2] == "1":
            finalValue = str(int(finalValue) + 338)
        
        if self._value[3] == "1" and self._target[3] == "1":
            operations["abs"] = True
        elif self._value[3] == "1":
            finalValue = str(int(finalValue) + 338)

        if operations["abs"] == True:
            finalValue = str(int(finalValue) * 2)

        if operations["x2"] == True:
            finalValue = str(int(finalValue) * 2)
        
        return finalValue
    
    def checkIfDefused(self):
        if self._value == self._target:
            self._defused = True

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return f"{self._value}/{int(self._value, 2)}"

