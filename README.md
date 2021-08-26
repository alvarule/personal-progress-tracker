# Personal Progress Tracker

### This program helps you set and track your daily goals. It asks you to set your goals everyday and reminds you on the next day to review/confirm if you completed previous day's goals and again set new goals for the present day. It also comes with a feature called as Slack Updates. By using this feature, you will get your daily goals handy on your mobile phone. But to use this feature, you'll need to have a Personal Slack Application's Incoming Webhook URL. To know how to get this [click here](https://api.slack.com/messaging/webhooks).
### The idea behind this project came to my mind when I attended a workshop organised by my college on the topic 'Industry Readiness'. In that workshop, the trainer told everyone to track their own progress by writing it down somewhere. And that hit my mind to developing a program which will help people to set small goals daily. So this is just a small program which will do the thing which I planned. This program will help those lazy people like me to set and track their daily goals. I'm hoping to further develop it in such a way that it will programmatically calculate the progress of a particular period of time (possibly 1 month) of an individual and congratulate him/her for achieving it, so that normal people who are not aware about how important it is to track their progress would be able to easily do it. But I'm not sure how will I do that. So if you have any idea, feel free to contact me on Social Media (social media links are given at the end)
### I hope my project will help you in one or the other way. I'm open for your feedbacks :)

## Table of Contents:
- [Usage](#usage)
- [Logic of Program](#logic-of-program)
- [Tip from the developer](#tip-from-developer)
- [Contact Me](#contact-me)
- [Thanks to](#thanks-to)


## Usage:

### It's very simple. You just need to clone this repository to your local computer and then run the file 'personal progress tracker.py'. 
### First of all, you'll be greeted with "Welcome" screen. Then it'll ask you for User Details like your Name, Age, Gender and your personal webhook URL which you can get by following the steps given [here](https://api.slack.com/messaging/webhooks). These details are just for user interactiveness but if you filled those and clicked 'Save' then the 'Slack Updates' feature will get activated for you. You can also skip this step but the program will keep asking for it everytime you run it. But once you filled those details and saved them, it'll never ask you for it again (My recommendation on this would be get those details filled so that you can get your daily goal updates handy on your mobile phone on 'Slack' Mobile Application). One more thing, once you saved your details and if you want to edit them, you cannot do it using the program. (For this purpose, I was designing a user-friendly dashboard (after developing all other functions) which will include all major options for user convenience and I also successfully developed it. But, a problem arised which was, from that dashboard when new windows opens, they were not accepting any user inputs and the reason behind this was - I was using Procedural Approach which is not suitable for developing multi-window programs. I researched for it and got that it can be done using Object Oriented Approach. But at that stage of development, it was very complicated to switch to Object Oriented Approach. So I left that idea (Planning to develop it in near future)). So for editing user details, the only thing you need to do is delete a hidden file named 'user_info.json' under "files/progress_tracker/" and then execute the program.
### After that, a window will open asking you to set your today's goals. Once you set them and clicked 'Done' if you have filled User Details, you'll get the list of those goals on your Slack Channel with which your provided Incoming Webhook URL is linked with. (If you don't know anything about Slack, I highly recommend you to get your hands dirty with it. It's very similar to Discord or any other communication platform)
### Next Day when you execute this program, as I mentioned if you haven't filled User Details it will ask for it, Else it'll ask you to confirm if you have completed your previous day's goals. And after that, you can set goals for present day.


## Logic of Program:

### Modules used - tkinter, datetime, os, json, requests
### Main functions - checkYesterdaysGoals() for confirming previous day's goals, setTodaysGoals() for setting present day's goals, getUserInfo() for getting User Details, centerWindow() which returns geometry value for all windows to appear at the center, sendUpdates() for sending updates i.e. list of present day's goals on Slack
### Files created/used/required - "user_info.json" for storing User details, "tracking_file.txt" for storing present day's date which will be used (explained later), "updates.txt" for storing a Boolean value for whether updates of present day has been sent or not and "YYYY-MM-DD.txt" (replace with Date) for storing everyday's goals. ("progress.ico" file is used for Icon of Windows. I'm unable to remember where I got that but I've downloaded it from Internet)

### Execution starts at "main". First of all existence of required files and folders will be checked and if anything is missing it will get created and initialised with default values(for files). Then a splash screen displaying "Welcome to Progress Tracker" is designed which will be displayed for 3 seconds using the after() function of tkinter. 
### Now the actual functions starts executing. (Here I've included the logic briefly. For detailed working of the program, you can review the source code where I've included the purpose of each block of code using comments.)

### centerWindow(): This function just calculates and returns a value, based on the provided arguments, which is directly passed as an argument to the geometry() function of tkinter window. This value will place the window at the center of the screen.

### getUserInfo(): This function accepts user details including Full Name, Age, Gender & Webhook URL. All these inputs will be validated through some checks so that any wrong input is not stored which can create errors further. And at last, stores those details in a JSON file using json module.

### checkYesterdaysGoals(): This function asks user to confirm his/her previous day's goals completed or not. At first it checks for existence of previous day's goals file which is named in the format - YYYY-MM-DD.txt (Ex: Goals of 15th August 2021 will be named as "2021-08-15.txt"). It also checks for an entry of Date in the file "tracked_file.txt" which will be entered by the function setTodaysGoals() while setting present day's goals. If both checks result to "True" then only it will perform its operation i.e. confirming previous day's goals from user. ### During confirming, it will separately store completed & incompleted goals of previous day and then it will write the completed goals in previous day's goals file and incomplete goals in present day's file means the user has to complete them on present day in addition to new goals. After successful completion of its task, it will update the 'tracking_file.txt' by removing previous day's entry in it which is added by setTodaysGoals() function on the previous day. 

### setTodaysGoals(): This function asks user to set goals for present day. But before that, it checks for the existence of the entry of present day and also checks the boolean value in 'update.txt' file. 
### If the entry is present and the boolean value is "False", it informs user that present day's goals are already set but the updates are not yet sent on Slack and asks user if he/she wants to send them at that moment? If user says "Yes" the function will call sendUpdate() function.
### Else if the entry is not present in 'tracking_file.txt', the program will ask user to set goals for present day.
### After successful completion of its task, it will append all the goals to the present day's goals' file. And then it will update the 'tracking_file.txt' file by entering present date in the format YYYY-MM-DD. It will also try to send Slack Updates and based on if it succeeds or fails, it will write a boolean value representing the result in the 'update.txt' file ("True" if succeeds else "False")

### sendUpdates(): This function generates a well structured message including date, username, list of present day's goals & at the end a greet for the user and sends it using requests module POST method on the Incoming Webhook URL provided in the user details.


## Tip from Developer:

### One more thing you can do for your convenience and that is, set this program to run once everyday using "Task Scheduler" for Windows users (If you are running on Linux you can use "Cron Daemon" and for Mac users "Automator" is a utility) so that even if you forgot to run the program, the OS will remember it for you.


## Contact Me:

### For any queries or issues you can contact me on:
- Telegram - @Athrv_7249 
- Instagram - [@_athrva_7249](https://www.instagram.com/_athrv_7249/) 
- Twitter - [@AtharvaVarule](https://twitter.com/AtharvaVarule)


## Thanks to:
- [CodeWithHarry for Python](https://youtube.com/playlist?list=PLu0W_9lII9agICnT8t4iYVSZ3eykIAOME)
- [CodeWithHarry for Tkinter](https://youtube.com/playlist?list=PLu0W_9lII9ajLcqRcj4PoEihkukF_OTzA)
- My Trainer of workshop for Idea
- [Tutorials Point for Tkinter Splash Screen](https://www.tutorialspoint.com/how-to-create-a-splash-screen-using-tkinter)
- [Ene Uran for Tkinter Centering Window Code](https://www.daniweb.com/programming/software-development/threads/66181/center-a-tkinter-window)
