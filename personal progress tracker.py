# Importing required packages
from tkinter import *
import tkinter.messagebox as tmsg
import datetime, os, json, requests

# function for checking yesterday's goals completed or not
def checkYesterdaysGoals():
    yesterday = datetime.date.today() - datetime.timedelta(1) # will get yesterday's date in format - "YYYY-MM-DD"

    # If yesterday's goals' file is present and its entry is also present in 'tracking_file.txt' that means it is not yet been checked so the program will ask user to check that.
    if f"{yesterday}.txt" in os.listdir() and f"{yesterday}" in open('tracking_file.txt').readlines():
        # |------------------------------------------|Nested Functions start|-----------------------------------------|
        
        # func will run when 'Completed' btn is clicked
        def checkCompleted():
            '''
            This function will make the ACTIVE item in yesterdaysGoals as Completed and will append the item in completedGoals simultaneously removing it from yesterdaysGoals
            '''
            if checkerLbox.get(ACTIVE) != "":
                completedGoals.append(checkerLbox.get(ACTIVE))
                completedGoals_var.set(value=completedGoals)
                yesterdaysGoals.remove(checkerLbox.get(ACTIVE))
                yesterdaysGoals_var.set(value=yesterdaysGoals)
                completedGoalsLbox.activate(END)
                noOfGoalsUpdater() # updating the no. of goals(Remaining to check, Completed and Not Completed) on the GUI


        # func will run when 'Not Completed' btn is clicked
        def checkNotcompleted():
            '''
            This function will make the ACTIVE item in yesterdaysGoals as Not Completed and will append the item in notcompletedGoals simultaneously removing it from yesterdaysGoals
            '''
            if checkerLbox.get(ACTIVE) != "":
                notcompletedGoals.append(checkerLbox.get(ACTIVE))
                notcompletedGoals_var.set(value=notcompletedGoals)
                yesterdaysGoals.remove(checkerLbox.get(ACTIVE))
                yesterdaysGoals_var.set(value=yesterdaysGoals)
                notcompletedGoalsLbox.activate(END)
                noOfGoalsUpdater() # updating the no. of goals(Remaining to check, Completed and Not Completed) on the GUI
        
        # func will run when 'Not Completed' btn in completedGoalsFrame is clicked
        def complete_notcomplete():
            '''
            This function will move the ACTIVE item in completedGoals to notcompletedGoals
            '''
            if completedGoalsLbox.get(ACTIVE) != "":
                notcompletedGoals.append(completedGoalsLbox.get(ACTIVE))
                notcompletedGoals_var.set(value=notcompletedGoals)
                completedGoals.remove(completedGoalsLbox.get(ACTIVE))
                completedGoals_var.set(value=completedGoals)
                completedGoalsLbox.activate(END)
                notcompletedGoalsLbox.activate(END)
                noOfGoalsUpdater() # updating the no. of goals(Remaining to check, Completed and Not Completed) on the GUI

        # func will run when 'Completed' btn in notcompletedGoals Frame is clicked
        def notcomplete_complete():
            '''
            This function will move the ACTIVE item in completedGoals to notcompletedGoals
            '''
            if notcompletedGoalsLbox.get(ACTIVE) != "":
                completedGoals.append(notcompletedGoalsLbox.get(ACTIVE))
                completedGoals_var.set(completedGoals)
                notcompletedGoals.remove(notcompletedGoalsLbox.get(ACTIVE))
                notcompletedGoals_var.set(notcompletedGoals)
                completedGoalsLbox.activate(END)
                notcompletedGoalsLbox.activate(END)
                noOfGoalsUpdater() # updating the no. of goals(Remaining to check, Completed and Not Completed) on the GUI
        
        # func will run when 'Done' btn is clicked
        def done():
            # to check if all yesterday's goals are checked
            if yesterdaysGoals==[]:
                
                # if notcompletedGoals is not empty that means user didn't completed all yesterday's goals, so confirming user about it
                if notcompletedGoals != []:
                    ans = tmsg.askyesno("Done", f"You have {len(notcompletedGoals)} Goals Not Completed of Yesterday. Those will be added in your Today\'s Goals List\nAre you sure you want to confirm them?", default="no")
                
                    if ans == True:
                        checkerComplete()
                else:
                    tmsg.showinfo("Info", "Congratulations!\nYou have successfully completed all your Yesterday\'s Goals")
                    checkerComplete()


            else:
                tmsg.showwarning("Note", f"You have not checked all your Yesterday's Goals!\n{remainingGoalsCount_var.get()}")
        
        def checkerComplete():
            '''
            func will store the contents of completedGoals & notcompletedGoals in respective files and clear the entry of yesterday in 'tracked file.txt'
            '''
            # adding completed goals to yesterday's goals file 
            with open(f"{yesterday}.txt", "w") as f:
                f.writelines(completedGoals)
            
            # adding notcompleted goals to today's goals file 
            with open(f"{datetime.date.today()}.txt", 'a') as f:
                f.writelines(notcompletedGoals)
            
            # Clearing the entry of Yesterday's Goals file as it has now been checked
            # but as the file is hidden we can't open it in write mode, so first we'll unhide it and then will clear its content and then again we'll hide it 
            os.system('attrib -h \"tracking_file.txt\"')
            with open('tracking_file.txt', 'w') as f:
                f.write("")
            os.system('attrib +h \"tracking_file.txt\"')
            window.destroy()

        
        def noOfGoalsUpdater():
            '''
            func will update the no. of goals(Remaining to check, Completed and Not Completed) on the GUI
            ''' 
            remainingGoalsCount_var.set(f"Remaining: {len(yesterdaysGoals)}")
            remainingGoalsCount.update()
            completedGoalsCount_var.set(f"Completed Goals: {len(completedGoals)}")
            completedGoalsCount.update()
            notcompletedGoalsCount_var.set(f"Not Completed Goals: {len(notcompletedGoals)}")
            notcompletedGoalsCount.update()

        # |------------------------------------------|Nested Functions end|-------------------------------------------|

        # |---------------------------------------|Logic & GUI Packing Start|------------------------------------------|
    
        # New window
        window = Tk()
        window.geometry(resolution)
        window.resizable(False, False)
        window.title("Check Yesterday's Goals - by Atharva Varule")
        try:
            window.wm_iconbitmap("..\progress.ico")
        except:
            pass
        window.protocol("WM_DELETE_WINDOW", exit) # will exit from program when 'Close' icon is clicked
        
        # lists for storing: 1-yesterday's goals 2-yesterday's completed goals 3-yesterday's incomplete goals
        yesterdaysGoals = []
        completedGoals = []
        notcompletedGoals = []
        
        # fetching yesterday's goals and appending them to the yesterdaysGoals list
        with open(f"{yesterday}.txt") as f:
            for line in f.readlines():
                if line != "\n": # will ignore empty lines
                    yesterdaysGoals.append(line)
        
        # creating StringVars which will store the list of all goals, completed goals & not completed goals and these vars we will use as value to the option 'listvariable' of Listbox
        yesterdaysGoals_var = StringVar(value=yesterdaysGoals)
        completedGoals_var = StringVar(value=completedGoals)
        notcompletedGoals_var = StringVar(value=notcompletedGoals)


        # ---------------Creating Frame for listbox of all goals--------------------------

        # Outer Frame for coloring border
        checkerFrameBorder = Frame(window, background="#074167")
        checkerFrameBorder.pack(side=TOP, fill=X, padx=0, pady=0)
        
        checkerFrame = Frame(checkerFrameBorder)
        checkerFrame.pack(side=TOP, fill=X, padx=4, pady=4)
        
        # Heading of Frame of all goals
        Label(checkerFrame, text="Check your Yesterday's Goals", font=("Gill Sans MT", 16, "bold")).pack(side=TOP, fill=Y, anchor="w", padx=5)
    
        # Will display no of remaining goals to check 
        remainingGoalsCount_var = StringVar(value=f"Remaining: {len(yesterdaysGoals)}")
        remainingGoalsCount = Label(checkerFrame, textvariable=remainingGoalsCount_var, font=("Gill Sans MT", 12))
        remainingGoalsCount.pack(anchor="e", padx=3)

        # Creating Frame for Listbox and its scrollbar
        in_checkerFrame = Frame(checkerFrame, background="#074167", pady=2)
        in_checkerFrame.pack(side=TOP, fill=X)

        # Listbox containing list of all goals
        checkerLbox = Listbox(in_checkerFrame, listvariable=yesterdaysGoals_var, exportselection=FALSE, width=121, height=9, font=("Trebuchet MS", 14), relief=FLAT, borderwidth=6, activestyle=NONE, highlightthickness=0, selectbackground="#032438", selectforeground="white", selectborderwidth=0, background="#8fc9ef")
        checkerLbox.select_set(ACTIVE)

        # X-Scrollbar for checkerLbox
        checkerLboxScrollX = Scrollbar(in_checkerFrame, command=checkerLbox.xview,orient=HORIZONTAL)
        checkerLbox.config(xscrollcommand=checkerLboxScrollX.set)

        # Y-Scrollbar for checkerLbox
        checkerLboxScrollY = Scrollbar(in_checkerFrame, command=checkerLbox.yview)
        checkerLbox.config(yscrollcommand=checkerLboxScrollY.set)

        # Packing X-Scrollbar , Y-Scrollbar & Listbox in a sequence for adjustment
        checkerLboxScrollX.pack(side=BOTTOM, fill=X, padx=0, pady=0)
        checkerLboxScrollY.pack(side=RIGHT, fill=Y, padx=0, pady=0)
        checkerLbox.pack(fill=BOTH, expand=True)
   

        # 'Not Completed' button
        Button(checkerFrame, text="Not Completed", command=checkNotcompleted, font=("Segoe UI Black", 12), width=20, relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424").pack(side=LEFT, padx=10, pady=5)

        # 'Completed' button
        Button(checkerFrame, text="Completed", command=checkCompleted, font=("Segoe UI Black", 12), width=20, relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424").pack(side=LEFT, padx=10, pady=5)
        
        # 'Done' Button
        Button(checkerFrame, text="Done", command=done, font=("Segoe UI Black", 12), width=20, relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424").pack(side=RIGHT, padx=10, pady=5)


        # --------------Creating Frame for listbox of completed goals---------------------

        # Outer Frame for coloring border
        completedGoalsFrameBorder = Frame(window, background="#074167")
        completedGoalsFrameBorder.pack(side=RIGHT, fill=Y, padx=0, pady=0)
        
        completedGoalsFrame = Frame(completedGoalsFrameBorder)
        completedGoalsFrame.pack(padx=4, pady=4)
        
        # Heading of Frame of completed goals
        completedGoalsCount_var = StringVar(value=f"Completed Goals: {len(completedGoals)}")
        completedGoalsCount = Label(completedGoalsFrame, textvariable=completedGoalsCount_var, font=("Gill Sans MT", 15, "bold"))
        completedGoalsCount.pack(side=TOP, fill=Y, anchor="w", padx=5, pady=10)

        # Button for moving item from completedGoals to notcompletedGoals
        Button(completedGoalsFrame, text="Not Completed", command=complete_notcomplete, font=("Segoe UI Black", 12), width=20, height=1,relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424").pack(side=BOTTOM ,pady=14)

        # Creating Frame for listbox and scrollbar
        in_completedGoalsFrame = Frame(completedGoalsFrame, background="#074167", pady=1)
        in_completedGoalsFrame.pack(fill=BOTH, expand=True)

        # Listbox containing list of completed goals
        completedGoalsLbox = Listbox(in_completedGoalsFrame, listvariable=completedGoals_var, width=66, height=8, font=("Trebuchet MS", 13), relief=FLAT, borderwidth=3, activestyle=NONE, highlightthickness=0, selectbackground="#032438", selectforeground="white", selectborderwidth=0, background="#8fc9ef")

        # X-Scrollbar for completedGoalsLbox
        completedGoalsLboxScrollX = Scrollbar(in_completedGoalsFrame, command=completedGoalsLbox.xview, orient=HORIZONTAL)
        completedGoalsLbox['xscrollcommand'] = completedGoalsLboxScrollX.set

        # Y-Scrollbar for completedGoalsLbox
        completedGoalsLboxScrollY = Scrollbar(in_completedGoalsFrame, command=completedGoalsLbox.yview)
        completedGoalsLbox['yscrollcommand'] = completedGoalsLboxScrollY.set

        # Packing X-Scrollbar , Y-Scrollbar & Listbox in a sequence for adjustment
        completedGoalsLboxScrollX.pack(side=BOTTOM, fill=X, pady=0)
        completedGoalsLboxScrollY.pack(side=RIGHT, fill=Y, padx=0, pady=0)
        completedGoalsLbox.pack(fill=BOTH, expand=True)

        # --------------Creating Frame for listbox of not completed goals-----------------

        # Outer Frame for coloring border
        notcompletedGoalsFrameBorder = Frame(window, background="#074167")
        notcompletedGoalsFrameBorder.pack(side=LEFT, fill=Y, padx=0, pady=0)
        
        notcompletedGoalsFrame = Frame(notcompletedGoalsFrameBorder)
        notcompletedGoalsFrame.pack(padx=4, pady=4)
        
        # Heading of Frame of notcompleted goals
        notcompletedGoalsCount_var = StringVar(value=f"Incomplete Goals: {len(notcompletedGoals)}")
        notcompletedGoalsCount = Label(notcompletedGoalsFrame, textvariable=notcompletedGoalsCount_var, font=("Gill Sans MT", 15, "bold"))
        notcompletedGoalsCount.pack(side=TOP, anchor="w", padx=5, pady=10)

        # Button for moving item from notcompletedGoals to completedGoals
        Button(notcompletedGoalsFrame, text="Completed", command=notcomplete_complete, font=("Segoe UI Black", 12), width=20, relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424").pack(side=BOTTOM, pady=14)

        # Creating Frame for listbox and scrollbar
        in_notcompletedGoalsFrame = Frame(notcompletedGoalsFrame, background="#074167", pady=1)
        in_notcompletedGoalsFrame.pack(fill=BOTH, expand=True)

        # Listbox containing list of not_completed goals
        notcompletedGoalsLbox = Listbox(in_notcompletedGoalsFrame, listvariable=notcompletedGoals_var, width=66, height=8, font=("Trebuchet MS", 13), relief=FLAT, borderwidth=3, activestyle=NONE, highlightthickness=0, selectbackground="#032438", selectforeground="white", selectborderwidth=0, background="#8fc9ef")

        # X-Scrollbar for notcompletedGoalsLbox
        notcompletedGoalsLboxScrollX = Scrollbar(in_notcompletedGoalsFrame, command=notcompletedGoalsLbox.xview, orient=HORIZONTAL)
        notcompletedGoalsLbox['xscrollcommand'] = notcompletedGoalsLboxScrollX.set
        
        # Y-Scrollbar for notcompletedGoalsLbox
        notcompletedGoalsLboxScrollY = Scrollbar(in_notcompletedGoalsFrame, command=notcompletedGoalsLbox.yview)
        notcompletedGoalsLbox['yscrollcommand'] = notcompletedGoalsLboxScrollY.set
        
        # Packing X-Scrollbar , Y-Scrollbar & Listbox in a sequence for adjustment
        notcompletedGoalsLboxScrollX.pack(side=BOTTOM, fill=X, pady=0)
        notcompletedGoalsLboxScrollY.pack(side=RIGHT, fill=Y, padx=0, pady=0)
        notcompletedGoalsLbox.pack(fill=BOTH, expand=True)


        window.mainloop()
        

        # |---------------------------------------|Logic & GUI Packing End|------------------------------------------|


# function for setting today's goals
def setTodaysGoals():
    today = datetime.date.today() # getting today's date in the format - YYYY-MM-DD
    
    # If today's entry is present in 'tracking_file.txt', and if 'update.txt' is present and its content is "False" that means updates are not yet sent on Slack, so the program will ask user about it
    # Else if today's entry is present in 'tracking_file.txt' that means todays goals are already set so the program will inform user about it
    # Else the program will ask user to set todays goals
    if (f"{today}" in open('tracking_file.txt').readlines()) and "update.txt" in os.listdir() and open('update.txt').read()=="False":
        ans = tmsg.askyesno("Info", "You have already checked in Today!\nBut updates are yet to be sent on Slack\nDo you want to send them now?")
        if ans == True:
            sendUpdate()
    
    elif f"{today}" in open('tracking_file.txt').readlines():
        tmsg.showinfo("Info", "You have already checked in Today! (confirming yesterday\'s goals and/or setting goals for today)")

    else:
        # |------------------------------------------|Nested Functions start|-----------------------------------------|

        # func will run when 'Add' btn is clicked
        def addGoal(event):
            '''
            This function will add the goal entered in Entry widget by user in todaysGoals list
            '''
            goal = goalEntry_var.get().title()
            goalEntry_var.set("") # clearing the entry widget
            if goal != "": # check if entry widget is empty?
                todaysGoals.append(goal)
                todaysGoals_var.set(todaysGoals)
                todaysGoalsCount_var.set(f"Your Today\'s Goals: {len(todaysGoals)}")
                todaysGoalsLbox.select_set(ACTIVE)
        
        # func will run when 'Edit' btn is clicked
        def edit():
            '''
            This function will move the ACTIVE list item from todaysGoalsLbox to goalEntry widget so as to allow user to edit it
            '''
            goal = todaysGoalsLbox.get(ACTIVE)
            goalEntry_var.set(goal)
            remove()
            todaysGoalsLbox.select_set(ACTIVE)

        # func will run when 'Remove' btn is clicked
        def remove():
            '''
            This function will remove the ACTIVE item in todaysGoalsLbox
            '''
            todaysGoals.remove(todaysGoalsLbox.get(ACTIVE))
            todaysGoals_var.set(todaysGoals)
            todaysGoalsCount_var.set(f"Your Today\'s Goals: {len(todaysGoals)}")
            todaysGoalsLbox.select_set(ACTIVE)
        
        # func will run when 'Done' btn is clicked
        def done():
            '''
            This function will append the todaysGoals in respective file and will also add entry of today in 'tracking_file.txt' after performing some necessary checks
            '''
            
            # check if user has set any goals or not?
            if todaysGoals==[]: 
                tmsg.showwarning('Warning', "You haven\'t set any goals for today !")
            
            else:
                ans = tmsg.askyesno('Info', f"You have set {len(todaysGoals)} Goals for Today\nAre you sure you want to confirm them?", default="no")

                if ans == True:
                    # Appending todaysGoals in respective file
                    with open(f"{today}.txt", 'a') as f:
                        for goal in todaysGoals:
                            f.write(f"{goal}\n")

                    # Adding entry of Today's Goals file
                    # but as the file is hidden we can't open it in write mode, so first we'll unhide it and then will add the entry and then again we'll hide it 
                    os.system('attrib -h \"tracking_file.txt\"')
                    with open('tracking_file.txt', 'w') as f:
                        f.write(f"{today}")
                    os.system('attrib +h \"tracking_file.txt\"')

                    tmsg.showinfo('Info', "Goals Set Successfully\nNow Go & Grind Yourself To Complete Them\nAll The Best!")
                    
                    # Sending updates on Slack if "update.txt" is present in os.listdir() (User has registered for Slack Updates)
                    if "update.txt" in os.listdir():
                        sendUpdate()

                    window.destroy()
        # |------------------------------------------|Nested Functions end|-----------------------------------------|

        # |------------------------------------------|Logic & GUI Packing start|-----------------------------------------|

        window = Tk()
        window.geometry(resolution)
        window.resizable(False, False)
        window.title("Set Today's Goals - by Atharva Varule")
        try:
            window.wm_iconbitmap("..\progress.ico")
        except:
            pass

        # list for storing today's goals
        todaysGoals = []
        # creating StringVar which will store the list of today's goals and this var we will use as value to the option 'listvariable' of Listbox
        todaysGoals_var = StringVar(value=todaysGoals)
        # creating StringVar which we will use as value to the option 'textvariable' of Entry widget
        goalEntry_var = StringVar(value="")

        # --------------------------------Goal Entry Frame--------------------------------
        
        # Outer Frame for coloring border
        goalEntryFrameBorder = Frame(window, background="#074167")
        goalEntryFrameBorder.pack(side=TOP, fill=X)
        
        # Frame for Goal Entry
        goalEntryFrame = Frame(goalEntryFrameBorder)
        goalEntryFrame.pack(fill=X, padx=4, pady=4)
        
        # Heading for Goal Entry Frame
        Label(goalEntryFrame, text="Set Your Goal:", font=("Gill Sans MT", 16, "bold")).pack(side=TOP, anchor="w", padx=8, pady=10)
        
        # Frame for Entry Widget for giving Border color
        goalEntryFrameBorder = Frame(goalEntryFrame, background="#074167")
        goalEntryFrameBorder.pack(side=TOP, fill=X, padx=10)

        # Entry widget for Goal Entry
        goalEntry = Entry(goalEntryFrameBorder, textvariable=goalEntry_var, font=("Trebuchet MS", 14), relief=FLAT, borderwidth=4)
        goalEntry.pack(fill=X, padx=2, pady=2)
        goalEntry.bind('<Return>', addGoal)
        
        # 'Add' button
        addBtn = Button(goalEntryFrame, text="Add", font=("Segoe UI Black", 12), width=16, relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424") 
        addBtn.pack(anchor="e", padx=10, pady=20)
        addBtn.bind('<Button-1>', addGoal)
    
        # --------------------------------Goal Edit Frame--------------------------------

        # Outer Frame for coloring border
        goalEditFrameBorder = Frame(window, background="#074167")
        goalEditFrameBorder.pack(fill=BOTH, expand=True)

        # Frame for goal editing
        goalEditFrame = Frame(goalEditFrameBorder)
        goalEditFrame.pack(fill=BOTH, expand=TRUE, padx=4, pady=4)

        # Heading of Frame of today's goals
        todaysGoalsCount_var = StringVar(value=f"Your Today\'s Goals: {len(todaysGoals)}")
        todaysGoalsCount = Label(goalEditFrame, textvariable=todaysGoalsCount_var, font=("Gill Sans MT", 16, "bold"))
        todaysGoalsCount.pack(side=TOP, anchor="w", padx=8, pady=10)
        
        # Creating Frame for listbox and scrollbar
        in_goalEditFrame = Frame(goalEditFrame, background="#074167", pady=2)
        in_goalEditFrame.pack(side=TOP, fill=X)

        # Listbox containing list of today's goals
        todaysGoalsLbox = Listbox(in_goalEditFrame, listvariable=todaysGoals_var, selectmode="single", height=15, font=("Trebuchet MS", 13), relief=FLAT, borderwidth=3, activestyle=NONE, highlightthickness=0, selectbackground="#032438", selectforeground="white", selectborderwidth=0, background="#8fc9ef")
        todaysGoalsLbox.select_set(ACTIVE)

        # X & Y Scrollbars for todaysGoalsLbox
        todaysGoalsLboxScrollX = Scrollbar(in_goalEditFrame, command=todaysGoalsLbox.xview, orient=HORIZONTAL)
        todaysGoalsLboxScrollY = Scrollbar(in_goalEditFrame, command=todaysGoalsLbox.yview)

        todaysGoalsLbox.config(xscrollcommand=todaysGoalsLboxScrollX.set, yscrollcommand=todaysGoalsLboxScrollY.set)
        
        # Packing X-Scrollbar, Y-Scrollbar & Listbox in a sequence for adjustment
        todaysGoalsLboxScrollX.pack(side=BOTTOM, fill=X)
        todaysGoalsLboxScrollY.pack(side=RIGHT, fill=Y)
        todaysGoalsLbox.pack(fill=BOTH, expand=True)

        # 'Edit' button
        Button(goalEditFrame, text="Edit", command=edit, font=("Segoe UI Black", 12), width=16, relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424").pack(side=LEFT, padx=10)

        # 'Remove' button
        Button(goalEditFrame, text="Remove", command=remove, font=("Segoe UI Black", 12), width=16, relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424").pack(side=LEFT, padx=10)

        # 'Done' button
        Button(goalEditFrame, text="Done", command=done, font=("Segoe UI Black", 12), width=16, relief=RIDGE, borderwidth=1, background="#e82535", foreground="#021326", activebackground="#d71424").pack(side=RIGHT, padx=10)

        
        window.mainloop()

        # |------------------------------------------|Logic & GUI Packing end|-----------------------------------------|


# function for getting User Information
def getUserInfo():
    splashWin.destroy() # Destroying the Welcome Screen

    # |------------------------------------------|Nested Functions start|-----------------------------------------|
    
    # func will run when 'Save' btn is clicked
    def save():
        '''
        This function will save the user info provided by the user after performing some necessary checks
        '''
        
        # check if any entry field is empty?
        if username_var.get()=="" or age_var.get()=="" or gender_var.get()=="" or webhook_var.get()=="":
            tmsg.showerror("Error", "Fields cannot be empty")
            return
        
        # check if input Age is integer?
        try:
            int(age_var.get())
        except:
            tmsg.showinfo("Info", f"Age cannot be \'{age_var.get()}\'")
            return
        
        # check if input Age is valid?
        if int(age_var.get())<=0 or int(age_var.get())>=120:
            tmsg.showinfo("Info", "You are not alive buddy!")
            return
        
        # checking URL input
        try:
            requests.get(webhook_var.get())
        
        # check if the URL is valid?
        except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema) :
            tmsg.showinfo("Info", "Invalid URL\nPlease enter the exact URL that you got from your \"Slack Application\'s Incoming Webhook URL\"\nIf you are confused here, please click on the \'Help\' button")
            return
    
        # check if the URL exists or if there is internet connection?
        except requests.exceptions.ConnectionError:
            tmsg.showinfo("Info", "Connection Failed\nPlease check your internet connection or the URL provided by you doesn't exists!")
            return

        # Registration successful message
        data = {"text":f"Hey {username_var.get().title()}!\nYou have successfully registered in Personal Progress Tracker software.\nNow you'll receive all your updates here.\nThanks for using our software. We hope you'll have great experience. Your feedbacks are always welcomed!"}
        
        webhook = webhook_var.get()
        response = requests.post(webhook, json.dumps(data)) # sending the message through user provided 'incoming webhook URL'

        # checking the 'response', if it is 'ok' then message sent successfully and that means the provided URL is valid 'Slack Application's Incoming Webhook URL'. And if the 'response' is something else, that means provided URL is not valid 'Slack App's Incoming Webhook URL'
        if response.text != "ok":
            tmsg.showinfo("Info", "Provided URL is not a \'Slack Application\'s Incoming Webhook URL\'")
            return
        
        tmsg.showinfo("Info", "Registration Successful!\n\nCheck you Slack Channel")

        # dict for storing user info
        userInfo = {
            "username":username_var.get().title(),
            "age":age_var.get(),
            "gender":gender_var.get(),
            "webhook":webhook_var.get()
        }
        
        # storing user info in 'user_info.json' file 
        os.system('attrib -h "user_info.json"')
        with open('user_info.json', 'w') as f:
            json.dump(userInfo, f)
        os.system('attrib +h "user_info.json"')
        
        # creating a file for storing boolean value representing if updates of todays goals are sent to slack or not
        with open('update.txt', 'w') as f:
            f.write("False")
        os.system('attrib +h "update.txt"') # hiding file "update.txt"

        window.destroy()

    # func will run when 'Help' btn is clicked
    def _help():
        '''
        This function will show a pop-up displaying Help info for the user
        '''

        import webbrowser
        ans = tmsg.askyesnocancel("Help", f"This software is developed by Atharva Varule\n\nYou can proceed further with or without creating User Account. Account creation can improve user experience. It comes with a feature which uses Slack channel to post your daily goals on it and it'll be very handy for you to review your goals as you can use Slack Mobile Application.\nFor that you\'ll need a Slack Application\' Incoming Webhook URL. If you want to get your own Incoming Webhook URL, click on \'Yes\'")
        # if user clicks 'Yes' then he/she will be redirected to the below link on a web browser
        if ans==True:
            url = "https://api.slack.com/messaging/webhooks"
            webbrowser.open(url)
    
    
    # |------------------------------------------|Nested Functions end|-----------------------------------------|

    # |------------------------------------------|Logic & GUI Packing start|-----------------------------------------|


    # fetching user info from 'user_info.json' file
    os.system('attrib -h \"user_info.json\"')
    with open('user_info.json', 'r') as f:
        userInfo = json.load(f)
    os.system('attrib +h \"user_info.json\"')
    
    # checking if user details are already filled or not?
    # if yes, then program will return to the main function. else it will ask user for it
    if userInfo["username"]!="" or userInfo["age"]!="" or userInfo["gender"]!="" or userInfo["webhook"]!="":
        return
   
    
    # creating the window
    window = Tk()
    window.geometry(centerWindow(540, 600, ws, hs))
    window.resizable(False, False)
    window.title("User Account")
    window.config(background="#074167")
    try:
        window.wm_iconbitmap("../progress.ico")
    except:
        pass

    # StringVars for storing values from userInfo
    username_var = StringVar(value=userInfo["username"])
    age_var = StringVar(value=userInfo["age"])
    gender_var = StringVar(value=userInfo["gender"])
    webhook_var = StringVar(value=userInfo["webhook"])

    # Frame for packing all widgets 
    frame = Frame(window)
    frame.pack(fill=BOTH, expand=True, padx=3, pady=3)
    
    # headFrame for packing Heading of the window
    headFrame = Frame(frame)
    headFrame.pack(side=TOP, fill=X)
    Label(headFrame, text="Account Details", font=("Gill Sans MT", 18, "bold"), pady=12).pack(fill=X, pady=2)
    
    # Label just for spacing adjustment (its text's color is white i.e. invisible)
    Label(frame, text="separator", foreground="white").pack(side=TOP, fill=X)
    
    # For positioning widgets in a neat way, separate frames are created for every entry field & its label

    # username label & its entry widget
    usernameFrame = Frame(frame)
    usernameFrame.pack(side=TOP, fill=X, pady=10)
    Label(usernameFrame, text="Full Name:", font=("Trebuchet MS", 13)).pack(anchor="w", padx=8)

    usernameEntryBorder = Frame(usernameFrame, background="#074167")
    usernameEntryBorder.pack(side=TOP, fill=X, padx=10)

    username_entry = Entry(usernameEntryBorder, textvariable=username_var, state="normal", font=("bahnschrift semicondensed", 14), borderwidth=5, relief=FLAT) 
    username_entry.pack(anchor="w", fill=X, padx=2, pady=2)

    # age label & its entry widget
    ageFrame = Frame(frame)
    ageFrame.pack(side=TOP, fill=X, pady=10)
    Label(ageFrame, text="Age:", font=("Trebuchet MS", 13)).pack(anchor="w", padx=8)

    ageEntryBorder = Frame(ageFrame, background="#074167")
    ageEntryBorder.pack(anchor="w", fill=X, padx=10)

    age_entry = Entry(ageEntryBorder, textvariable=age_var, state="normal", font=("bahnschrift semicondensed", 14), borderwidth=5, relief=FLAT) 
    age_entry.pack(anchor="w", fill=X, padx=2, pady=2)

    # gender label & its radiobutton widgets
    genderFrame = Frame(frame)
    genderFrame.pack(side=TOP, fill=X, pady=10)
    Label(genderFrame, text="Gender:", font=("Trebuchet MS", 13)).pack(side=LEFT, anchor="n", padx=8)

    gender_entry_M = Radiobutton(genderFrame, value="M", variable=gender_var, text="Male", state="normal", tristatevalue=0, font=("bahnschrift semicondensed", 13)) 
    gender_entry_M.pack(anchor="w")
    gender_entry_F = Radiobutton(genderFrame, value="F", variable=gender_var, text="Female", state="normal", tristatevalue=0, font=("bahnschrift semicondensed", 13)) 
    gender_entry_F.pack(anchor="w")

    # webhook label & its entry widget
    webhookFrame = Frame(frame)
    webhookFrame.pack(side=TOP, fill=X, pady=10)
    Label(webhookFrame, text="Slack Application\'s Incoming Webhook URL:", font=("Trebuchet MS", 13)).pack(anchor="w", padx=8)

    webhookEntryBorder = Frame(webhookFrame, background="#074167")
    webhookEntryBorder.pack(anchor="w", fill=X, padx=10)
    
    webhook_entry = Entry(webhookEntryBorder, textvariable=webhook_var, state="normal", font=("bahnschrift semicondensed", 14), borderwidth=5, relief=FLAT) 
    webhook_entry.pack(anchor="w", fill=X, padx=2, pady=2)

    print(username_var.get(), age_var.get(), gender_var.get(), webhook_var.get())
    print(username_entry.get(), age_entry.get(), webhook_entry.get())


    # 'Skip' button
    Button(frame, text="Skip", command=window.destroy, font=("Segoe UI Black", 12), width=10, relief=RIDGE, borderwidth=1, background="#f93646", foreground="#021326", activebackground="#d71424").pack(side=LEFT, padx=10)
    
    # 'Save' button
    Button(frame, text="Save", command=save, font=("Segoe UI Black", 12), width=10, relief=RIDGE, borderwidth=1, background="#f93646", foreground="#021326", activebackground="#d71424").pack(side=RIGHT, padx=10)
    
    # 'Help' button
    Button(frame, text="Help", command=_help, font=("Segoe UI Black", 12), width=10, relief=RIDGE, borderwidth=1, background="#f93646", foreground="#021326", activebackground="#d71424").pack(side=LEFT, padx=10)
    
    
    window.mainloop()

    # |------------------------------------------|Logic & GUI Packing end|-----------------------------------------|


# function for placing window at the center of screen (copied from 'https://www.daniweb.com/programming/software-development/threads/66181/center-a-tkinter-window' and edited it to fit in my software)
def centerWindow(_w, _h, _ws, _hs):

    # calculate position x, y
    x = (_ws/2) - (_w/2)    
    y = (_hs/2) - (_h/2)

    return '%dx%d+%d+%d' % (_w, _h, x, y)


# function for sending Slack Update
def sendUpdate():
    today = datetime.date.today() # getting today's date in format: YYYY-MM-DD

    # getting user details
    with open('user_info.json', 'r') as f:
        userInfo = json.load(f)
    
    # storing required user details in separate variables
    username = userInfo.get("username")
    webhook = userInfo.get("webhook")
        
    srNo = 1 # counter for goals

    # message to send on Slack
    message = f"Date: {today}\n\nHey {username}!\nHere\'s your today\'s list of goals:\n\n"

    with open(f'{today}.txt', 'r') as f:
        for goal in f.readlines():
            if goal!="\n" and goal!="":
                message = f"{message}{str(srNo)} - {goal}"
                srNo += 1
    
    message = f"{message}\nNow get yourself ready to achieve these goals\nAll The Best!"
    
    '''
    At this point the message will be:
        Date: <today's date>

        Hey <username>!
        Here's your today's list of goals:

        1 - ......
        2 - ......
        .
        .
        .
        n - ......

        Now get yourself ready to achieve these goals
        All The Best!
    '''
    
    # creating payload for posting on Slack
    data = {
        "text":message
    }
    
    try:
        # sending the update message
        response = requests.post(webhook, json.dumps(data))

        # updating the file "update.txt" to "True"
        os.system('attrib -h "update.txt"')
        with open('update.txt', 'w') as f:
            f.write("True")
        os.system('attrib +h "update.txt"')

    # if Internet connection failed
    except requests.exceptions.ConnectionError:
        ans = tmsg.askretrycancel("Error", "Unable to send updates on Slack\nPlease check your internet connection and try again")
        if ans == True:
            sendUpdate()
        else:
            # updating the file "update.txt" to "False"
            os.system('attrib -h "update.txt"')
            with open('update.txt', 'w') as f:
                f.write("False")
            os.system('attrib +h "update.txt"')


if __name__=="__main__":
    if "files" not in os.listdir():
        os.makedirs("files")
    
    os.chdir("files") # changing the working directory to where all the required files exists or will be existing

    # if "progress_tracker" directory is not present (program is executing for the first time)
    if "progress_tracker" not in os.listdir():
        os.makedirs("progress_tracker")
    
    os.chdir("progress_tracker")
    
    if "tracking_file.txt" not in os.listdir():
        # creating file to store list of tracked dates
        with open('tracking_file.txt', 'a') as f:
            pass
        # hiding the file 'tracking_file.txt'
        os.system('attrib +h \"tracking_file.txt\"')
        
    if "user_info.json" not in os.listdir():
        # creating file to store user information
        with open('user_info.json', 'w') as f:
            # initializing user info to dump into the file
            emptyUserInfo = {
                "username":"", "age":"", "gender":"", "webhook":""
            }
            json.dump(emptyUserInfo, f)
        # hiding the file 'user_info.json'
        os.system('attrib +h \"user_info.json\"')

    
    # Creating Splash Screen for Welcoming User (copied from 'https://www.tutorialspoint.com/how-to-create-a-splash-screen-using-tkinter' and edited it to fit in my software)
    splashWin= Tk()

    # Get screen width and height
    ws = splashWin.winfo_screenwidth()
    hs = splashWin.winfo_screenheight()

    # Define the size of the window or frame
    splashWin.geometry(centerWindow(640, 320, ws, hs))

    # Remove border of the splash Window
    splashWin.overrideredirect(True)
    
    splashFrame = Frame(splashWin, background="#074167")
    splashFrame.pack(fill=BOTH, expand=True)
    
    # Define the label of the window
    Label(splashFrame, text= "Welcome\nto\nProgress Tracker", fg= "#f93646",
    font=('segoe ui black', 35), padx=10, pady=10).pack(pady=50)
   

    # Splash Window Timer
    splashWin.after(3000, getUserInfo)

    splashWin.mainloop()
    

    resolution = centerWindow(1250, 720, ws, hs) # geometry value for all windows
    checkYesterdaysGoals()    
    setTodaysGoals()
    