import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from tkcalendar import DateEntry
from dataclasses import dataclass
import pickle
from PIL import Image
import datetime

##########################
# CLASSES & DICTIONARIES #
##########################

# Client Class
@dataclass
class Client():
    clientID: str
    password: str
    firstName: str
    surname: str
    email: str
    phoneNumber: str
    dob: str

    # Used to add the object to the dictionary it will be stored in, to then put the dictionary into a pkl file
    def AddToDictionary(self):
        clientDictionary[self.clientID] = self

# Staff Class
@dataclass
class Staff():
    staffID: str
    password: str
    firstName: str
    surname: str
    email: str
    phoneNumber: str
    unavailableDates: list[str]    # format should be %d/%m/%Y %H.%M
    isHigherAdmin: bool

    # Used to add the object to the dictionary it will be stored in add the appropriate index
    def AddToDictionary(self):
        staffDictionary[self.staffID] = self

    # Used when booking to match the staff object to the combobox display
    def __str__(self):
        return f"{self.firstName} {self.surname}"

# Booking Class
@dataclass
class Booking():
    client: Client
    staff: Staff
    bookingID: str
    bookingTime: str
    isMentoring: bool   # True if it is a mentoring session, false if it is a reading

    # Used to add itself to the dictionary it will be stored in, the dictionary is then stored in a pkl file
    def AddToDictionary(self):
        bookingDictionary[self.bookingID] = self
    
# Review Class
@dataclass
class Review():
    staff: Staff
    reviewID: str
    review: str

    # Used to add itself to the dictionary it will be stored in
    def AddToDictionary(self):
        reviewDictionary[self.reviewID] = self

# Dictionaries the objects will be stored in
clientDictionary = {}
staffDictionary = {}
bookingDictionary = {}
reviewDictionary = {}


###################
# USER INTERFACES #
###################

# Login
def LoginScreen(screenToDestroy):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Login")
    screen.geometry("450x350+0+0")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lLogin = ctk.CTkLabel(screen, text="Log In", font=("Arial", 30))
    lLogin.place(relx=0.5, rely=0.2, anchor="center")
    lEmail = ctk.CTkLabel(screen, text="Email:")
    lEmail.place(relx=0.3, rely=0.4, anchor="e")
    lPassword = ctk.CTkLabel(screen, text="Password:")
    lPassword.place(relx=0.3, rely=0.55, anchor="e")

    # Entries
    eEmail = ctk.CTkEntry(screen, placeholder_text="Email", width=190)
    eEmail.place(relx=0.4, rely=0.4, anchor="w")
    ePassword = ctk.CTkEntry(screen, placeholder_text="Password", width=190, show="*")
    ePassword.place(relx=0.4, rely=0.55, anchor="w")

    # Buttons
    bLogin = ctk.CTkButton(screen, text="Login", command=lambda:Login(eEmail.get(), ePassword.get(), screen))
    bLogin.place(relx=0.3, rely=0.75, anchor="center")
    bSignUp = ctk.CTkButton(screen, text="Sign Up", command=lambda:RegisterCustomerScreen(screen))
    bSignUp.place(relx=0.7, rely=0.75, anchor="center")

    screen.mainloop()

# Register Customer
def RegisterCustomerScreen(screenToDestroy):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Sign Up")
    screen.geometry("450x350+0+0")

    # Frame
    frame = ctk.CTkScrollableFrame(screen, width=400, height=200, fg_color="#242424")
    frame.place(relx=0.5, rely=0.55, anchor="center")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="Sign Up", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.15, anchor="center")
    lFirstName = ctk.CTkLabel(frame, text="First Name:", font=("Arial", 15))
    lFirstName.grid(row=0, column=0, padx=50, pady=20)
    lSurname = ctk.CTkLabel(frame, text="Surname:", font=("Arial", 15))
    lSurname.grid(row=1, column=0)
    lEmail = ctk.CTkLabel(frame, text="Email:", font=("Arial", 15))
    lEmail.grid(row=2, column=0, pady=20)
    lPassword = ctk.CTkLabel(frame, text="Password:", font=("Arial", 15))
    lPassword.grid(row=3, column=0)
    lRepeat = ctk.CTkLabel(frame, text="Repeat Password:", font=("Arial", 15))
    lRepeat.grid(row=4, column=0, pady=20)
    lDOB = ctk.CTkLabel(frame, text="Date Of Birth:", font=("Arial", 15))
    lDOB.grid(row=5, column=0)
    lPhone = ctk.CTkLabel(frame, text="Phone Number:", font=("Arial", 15))
    lPhone.grid(row=6, column=0, pady=20)
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Entries
    eFirstName = ctk.CTkEntry(frame, placeholder_text="First Name", width=200)
    eFirstName.grid(row=0, column=1)
    eSurname = ctk.CTkEntry(frame, placeholder_text="Surname", width=200)
    eSurname.grid(row=1, column=1)
    eEmail = ctk.CTkEntry(frame, placeholder_text="Email", width=200)
    eEmail.grid(row=2, column=1)
    ePassword = ctk.CTkEntry(frame, placeholder_text="Password", width=200, show="*")
    ePassword.grid(row=3, column=1)
    eRepeat = ctk.CTkEntry(frame, placeholder_text="Repeat Password", width=200, show="*")
    eRepeat.grid(row=4, column=1)
    ePhone = ctk.CTkEntry(frame, placeholder_text="Phone Number", width=200)
    ePhone.grid(row=6, column=1)

    # Calendar Dropdown
    today = datetime.datetime.now()
    eighteenYearsAgo = today.replace(year=today.year - 18)
    calDOB = DateEntry(frame, width=25, height=200, date_pattern="DD/MM/yyyy", maxdate=eighteenYearsAgo)
    calDOB.grid(row=5, column=1, padx=5)

    # Buttons
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:LoginScreen(screen))
    bBack.place(relx=0.1, rely=0.9, anchor="e")
    bSignUp = ctk.CTkButton(screen, text="Sign Up", command=lambda:RegisterCustomer(screen, eEmail.get(), ePassword.get(), eRepeat.get(), eFirstName.get(), eSurname.get(), ePhone.get(), calDOB.get_date()))
    bSignUp.place(relx=0.5, rely=0.9, anchor="center")

    screen.mainloop()

# Register Staff
def RegisterStaffScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Register Staff")
    screen.geometry("450x350+0+0")

    # Variable for admin checkbox
    isAdminVar = ctk.BooleanVar()

    # Frame
    frame = ctk.CTkScrollableFrame(screen, width=400, height=200, fg_color="#242424")
    frame.place(relx=0.5, rely=0.55, anchor="center")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="Sign Up", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.15, anchor="center")
    lFirstName = ctk.CTkLabel(frame, text="First Name:", font=("Arial", 15))
    lFirstName.grid(row=0, column=0, padx=50, pady=20)
    lSurname = ctk.CTkLabel(frame, text="Surname:", font=("Arial", 15))
    lSurname.grid(row=1, column=0)
    lEmail = ctk.CTkLabel(frame, text="Email:", font=("Arial", 15))
    lEmail.grid(row=2, column=0, pady=20)
    lPassword = ctk.CTkLabel(frame, text="Password:", font=("Arial", 15))
    lPassword.grid(row=3, column=0)
    lRepeat = ctk.CTkLabel(frame, text="Repeat Password:", font=("Arial", 15))
    lRepeat.grid(row=4, column=0, pady=20)
    lPhone = ctk.CTkLabel(frame, text="Phone Number:", font=("Arial", 15))
    lPhone.grid(row=5, column=0)
    lIsAdmin = ctk.CTkLabel(frame, text="Admin?", font=("Arial", 15))
    lIsAdmin.grid(row=6, column=0, pady=20)
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Entries
    eFirstName = ctk.CTkEntry(frame, placeholder_text="First Name", width=200)
    eFirstName.grid(row=0, column=1)
    eSurname = ctk.CTkEntry(frame, placeholder_text="Surname", width=200)
    eSurname.grid(row=1, column=1)
    eEmail = ctk.CTkEntry(frame, placeholder_text="Email", width=200)
    eEmail.grid(row=2, column=1)
    ePassword = ctk.CTkEntry(frame, placeholder_text="Password", width=200, show="*")
    ePassword.grid(row=3, column=1)
    eRepeat = ctk.CTkEntry(frame, placeholder_text="Repeat Password", width=200, show="*")
    eRepeat.grid(row=4, column=1)
    ePhone = ctk.CTkEntry(frame, placeholder_text="Phone Number", width=200)
    ePhone.grid(row=5, column=1)

    # Tickbox
    tbIsAdmin = ctk.CTkCheckBox(frame, text="", variable=isAdminVar)
    tbIsAdmin.grid(row=6, column=1)

    # Buttons
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:AdminHomeScreen(screen, account))
    bBack.place(relx=0.1, rely=0.9, anchor="e")
    bSignUp = ctk.CTkButton(screen, text="Sign Up", command=lambda:RegisterStaff(screen, account, eEmail.get(), ePassword.get(), eRepeat.get(), eFirstName.get(), eSurname.get(), ePhone.get(), isAdminVar.get()))
    bSignUp.place(relx=0.5, rely=0.9, anchor="center")

    screen.mainloop()

# Customer Home
def CustomerHomeScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Customer Home")
    screen.geometry("450x350+0+0")

    # Get first name for "Welcome, [NAME]"
    firstName = account.firstName

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lHome = ctk.CTkLabel(screen, text="HOME", font=("Arial", 35))
    lHome.place(relx=0.5, rely=0.1, anchor="center")
    lWelcome = ctk.CTkLabel(screen, text="Welcome, " + firstName, font=("Arial", 25))
    lWelcome.place(relx=0.5, rely=0.25, anchor="center")
    lLogOut = ctk.CTkLabel(screen, text="Log Out")
    lLogOut.place(relx=0.11, rely=0.9, anchor="w")
    lManageAccount = ctk.CTkLabel(screen, text="Manage Account")
    lManageAccount.place(relx=0.89, rely=0.9, anchor="e")

    # Buttons
    bMakeBooking = ctk.CTkButton(screen, text="Make A Booking", command=lambda:MakeBookingScreen(screen, account))
    bMakeBooking.place(relx=0.5, rely=0.4, anchor="center")
    bViewBookings = ctk.CTkButton(screen, text="Manage Bookings", command=lambda:ClientViewBookingsScreen(screen, account))
    bViewBookings.place(relx=0.5, rely=0.53, anchor="center")
    bMakeReview = ctk.CTkButton(screen, text="Make A Review", command=lambda:MakeReviewScreen(screen, account))
    bMakeReview.place(relx=0.5, rely=0.66, anchor="center")
    bViewReviews = ctk.CTkButton(screen, text="View Reviews", command=lambda:ViewReviewsScreen(screen, account, None, "client"))
    bViewReviews.place(relx=0.5, rely=0.79, anchor="center")
    bLogOut = ctk.CTkButton(screen, text="[]", width=20, command=lambda:LoginScreen(screen))
    bLogOut.place(relx=0.1, rely=0.9, anchor="e")
    bManageAccount = ctk.CTkButton(screen, text="[]", width=20, command=lambda:LessDetailEditClientsScreen(screen, account))
    bManageAccount.place(relx=0.9, rely=0.9, anchor="w")

    screen.mainloop()

# Staff Home
def StaffHomeScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Staff Home")
    screen.geometry("450x350+0+0")

    # Get first name for "Welcome, [NAME]"
    firstName = account.firstName

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lHome = ctk.CTkLabel(screen, text="STAFF HUB", font=("Arial", 35))
    lHome.place(relx=0.5, rely=0.1, anchor="center")
    lWelcome = ctk.CTkLabel(screen, text="Welcome, " + firstName, font=("Arial", 25))
    lWelcome.place(relx=0.5, rely=0.25, anchor="center")
    lLogOut = ctk.CTkLabel(screen, text="Log Out")
    lLogOut.place(relx=0.11, rely=0.9, anchor="w")
    lManageAccount = ctk.CTkLabel(screen, text="Manage Account")
    lManageAccount.place(relx=0.89, rely=0.9, anchor="e")

    # Buttons
    bViewBookings = ctk.CTkButton(screen, text="View Bookings", command=lambda:StaffViewBookingsScreen(screen, account, False))
    bViewBookings.place(relx=0.5, rely=0.4, anchor="center")
    bViewReviews = ctk.CTkButton(screen, text="View Reviews", command=lambda:ViewReviewsScreen(screen, account, str(account), "staff"))
    bViewReviews.place(relx=0.5, rely=0.53, anchor="center")
    bLogOut = ctk.CTkButton(screen, text="[]", width=20, command=lambda:LoginScreen(screen))
    bLogOut.place(relx=0.1, rely=0.9, anchor="e")
    bManageAccount = ctk.CTkButton(screen, text="[]", width=20, command=lambda:EditStaffScreen(screen, account, False, False, None))
    bManageAccount.place(relx=0.9, rely=0.9, anchor="w")

    screen.mainloop()

# Admin Home
def AdminHomeScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Admin Home")
    screen.geometry("450x350+0+0")

    # Get first name for "Welcome, [NAME]"
    firstName = account.firstName

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lHome = ctk.CTkLabel(screen, text="ADMIN HUB", font=("Arial", 35))
    lHome.place(relx=0.5, rely=0.1, anchor="center")
    lWelcome = ctk.CTkLabel(screen, text="Welcome, " + firstName, font=("Arial", 25))
    lWelcome.place(relx=0.5, rely=0.25, anchor="center")
    lLogOut = ctk.CTkLabel(screen, text="Log Out")
    lLogOut.place(relx=0.11, rely=0.9, anchor="w")
    lManageAccount = ctk.CTkLabel(screen, text="Manage Account")
    lManageAccount.place(relx=0.89, rely=0.9, anchor="e")

    # Buttons
    bSearchAccounts = ctk.CTkButton(screen, text="Search Accounts", command=lambda:AccountSearchScreen(screen, account))
    bSearchAccounts.place(relx=0.5, rely=0.4, anchor="center")
    bMakeStaffAccount = ctk.CTkButton(screen, text="Make Staff Account", command=lambda:RegisterStaffScreen(screen, account))
    bMakeStaffAccount.place(relx=0.5, rely=0.53, anchor="center")
    bViewBooking = ctk.CTkButton(screen, text="Manage Bookings", command=lambda:StaffViewBookingsScreen(screen, account, True))
    bViewBooking.place(relx=0.5, rely=0.66, anchor="center")
    bViewReviews = ctk.CTkButton(screen, text="View Reviews", command=lambda:ViewReviewsScreen(screen, account, str(account), "admin"))
    bViewReviews.place(relx=0.5, rely=0.79, anchor="center")
    bLogOut = ctk.CTkButton(screen, text="[]", width=20, command=lambda:LoginScreen(screen))
    bLogOut.place(relx=0.1, rely=0.9, anchor="e")
    bManageAccount = ctk.CTkButton(screen, text="[]", width=20, command=lambda:EditStaffScreen(screen, account, False, True, account))
    bManageAccount.place(relx=0.9, rely=0.9, anchor="w")

    screen.mainloop()

# Making a Booking
def MakeBookingScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Make A Booking")
    screen.geometry("450x350+0+0")

    # List of all staff names for "Hosts" combobox
    with open("staffAccountsFile.pkl", "rb") as file:
        dictionary = pickle.load(file)
        listOfNames = []
        for user in dictionary.values():
            listOfNames.append(str(user))

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="Make A Booking", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lChooseDate = ctk.CTkLabel(screen, text="Pick A Date:")
    lChooseDate.place(relx=0.3, rely=0.27, anchor="center")
    lTime = ctk.CTkLabel(screen, text="Time:")
    lTime.place(relx=0.6, rely=0.36, anchor="w")
    lHost = ctk.CTkLabel(screen, text="Host:")
    lHost.place(relx=0.6, rely=0.5, anchor="w")
    lType = ctk.CTkLabel(screen, text="Type:")
    lType.place(relx=0.6, rely=0.64, anchor="w")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Dropdowns
    selectedStaff = StringVar()
    cbTime = ctk.CTkComboBox(screen, values=["09.00", "09.30", "10.00", "10.30", "11.00", "11.30", "12.00", "12.30", "13.00", "13.30", "14.00", "14.30", "15.00", "15.30", "16.00", "16.30"], width=120)
    cbTime.place(relx=0.7, rely=0.36, anchor="w")
    cbHosts = ctk.CTkComboBox(screen, values=listOfNames, width=120, variable=selectedStaff)
    cbHosts.place(relx=0.7, rely=0.5, anchor="w")
    cbHosts.set(listOfNames[0])

    # Radio Buttons
    typeVar = ctk.BooleanVar(value=False)     # For checking which type of session has been picked
    rbReading = ctk.CTkRadioButton(screen, text="Reading", variable=typeVar, value=False)
    rbReading.place(relx=0.7, rely=0.64, anchor="w")
    rbMentor = ctk.CTkRadioButton(screen, text="Mentoring", variable=typeVar, value=True)
    rbMentor.place(relx=0.7, rely=0.7)

    # Buttons
    bBook = ctk.CTkButton(screen, text="Book", command=lambda:MakeBooking(account, SelectStaff(selectedStaff.get()), cbTime.get(), calCalendar.get_date(), typeVar.get()))
    bBook.place(relx=0.5, rely=0.85, anchor="center")
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:CustomerHomeScreen(screen, account))
    bBack.place(relx=0.1, rely=0.9, anchor="e")

    # Calendar
    rightNow = datetime.datetime.now()
    calCalendar = Calendar(screen, selectmode="day", font=("Arial", 18), date_pattern="dd/mm/yyyy", mindate=rightNow)
    calCalendar.place(relx=0.3, rely=0.55, anchor="center")

    screen.mainloop()

# Make a Review
def MakeReviewScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Make A Review")
    screen.geometry("450x350+0+0")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="Submit A Review", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lWho = ctk.CTkLabel(screen, text="Who are you reviewing?:")
    lWho.place(relx=0.1, rely=0.25, anchor="w")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Combobox
    with open("staffAccountsFile.pkl", "rb") as file:
        dictionary = pickle.load(file)
        listOfNames = []
        for user in dictionary.values():
            listOfNames.append(str(user))
    
    selectedStaff = StringVar()
    cbStaff = ctk.CTkComboBox(screen, values=listOfNames, width=200, variable=selectedStaff)
    cbStaff.set(listOfNames[0])
    cbStaff.place(relx=0.5, rely=0.25, anchor="w")

    # Textbox
    txReview = ctk.CTkTextbox(screen, width=325, height=140)
    txReview.place(relx=0.5, rely=0.525, anchor="center")

    # Buttons
    bSubmit = ctk.CTkButton(screen, text="Submit", command=lambda:MakeReview(SelectStaff(selectedStaff.get()), txReview.get("0.0", "end-1c"), account, screen))
    bSubmit.place(relx=0.5, rely=0.8, anchor="center")
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:CustomerHomeScreen(screen, account))
    bBack.place(relx=0.1, rely=0.9, anchor="e")

    screen.mainloop()

# Edit client account details, accessible from the client home screen
def LessDetailEditClientsScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Edit Details")
    screen.geometry("450x350+0+0")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="Account Manager", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lFullName = ctk.CTkLabel(screen, text="Full Name:")
    lFullName.place(relx=0.3, rely=0.3, anchor="e")
    lEmail = ctk.CTkLabel(screen, text="Email:")
    lEmail.place(relx=0.3, rely=0.45, anchor="e")
    lPhone = ctk.CTkLabel(screen, text="Phone Number:")
    lPhone.place(relx=0.3, rely=0.6, anchor="e")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Entries
    eFirstName = ctk.CTkEntry(screen, width=100, placeholder_text="First Name")
    eFirstName.place(relx=0.4, rely=0.3, anchor="w")
    eFirstName.insert(0, account.firstName)
    eSurname = ctk.CTkEntry(screen, width=100, placeholder_text="Surname")
    eSurname.place(relx=0.67, rely=0.3, anchor="w")
    eSurname.insert(0, account.surname)
    eEmail = ctk.CTkEntry(screen, width=220, placeholder_text="Email")
    eEmail.place(relx=0.4, rely=0.45, anchor="w")
    eEmail.insert(0, account.email)
    ePhone = ctk.CTkEntry(screen, width=220, placeholder_text="Phone Number")
    ePhone.place(relx=0.4, rely=0.6, anchor="w")
    ePhone.insert(0, account.phoneNumber)

    # Buttons
    bSave = ctk.CTkButton(screen, text="Save", command=lambda:EditClientDetails(account, eFirstName.get(), eSurname.get(), eEmail.get(), ePhone.get(), None, screen, True, None))
    bSave.place(relx=0.3, rely=0.75, anchor="center")
    bDelete = ctk.CTkButton(screen, text="Delete Account", command=lambda:DeleteClient(account, screen))
    bDelete.place(relx=0.7, rely=0.75, anchor="center")
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:CustomerHomeScreen(screen, account))
    bBack.place(relx=0.1, rely=0.9, anchor="e")

    screen.mainloop()

# Edit client account details, accessible from searching for the account
def MoreDetailEditClientsScreen(screenToDestroy, account, adminsAccount):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Edit Details")
    screen.geometry("450x350+0+0")

    # Frame
    frame = ctk.CTkScrollableFrame(screen, width=400, height=160, fg_color="#242424")
    frame._scrollbar.configure(height=0)
    frame.place(relx=0.5, rely=0.45, anchor="center")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="Manage Account", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lFirstName = ctk.CTkLabel(frame, text="First Name:")
    lFirstName.grid(row=0, column=0, padx=15)
    lSurname = ctk.CTkLabel(frame, text="Surname:")
    lSurname.grid(row=1, column=0, padx=15)
    lEmail = ctk.CTkLabel(frame, text="Email:")
    lEmail.grid(row=2, column=0, padx=15)
    lPhone = ctk.CTkLabel(frame, text="Phone Number:")
    lPhone.grid(row=3, column=0, padx=15)
    lPassword = ctk.CTkLabel(frame, text="Password:")
    lPassword.grid(row=4, column=0, padx=15)
    lDOB = ctk.CTkLabel(frame, text="Date Of Birth:")
    lDOB.grid(row=5, column=0, padx=15)
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Entries
    eFirstName = ctk.CTkEntry(frame, width=220, placeholder_text="First Name")
    eFirstName.grid(row=0, column=1, pady=10)
    eFirstName.insert(0, account.firstName)
    eSurname = ctk.CTkEntry(frame, width=220, placeholder_text="Surname")
    eSurname.grid(row=1, column=1, pady=10)
    eSurname.insert(0, account.surname)
    eEmail = ctk.CTkEntry(frame, width=220, placeholder_text="Email")
    eEmail.grid(row=2, column=1, pady=10)
    eEmail.insert(0, account.email)
    ePhone = ctk.CTkEntry(frame, width=220, placeholder_text="Phone Number")
    ePhone.grid(row=3, column=1, pady=10)
    ePhone.insert(0, account.phoneNumber)
    ePassword = ctk.CTkEntry(frame, width=220, placeholder_text="Password")
    ePassword.grid(row=4, column=1, pady=10)
    ePassword.insert(0, account.password)

    # Calendar
    today = datetime.datetime.now()
    eighteenYearsAgo = today.replace(year=today.year - 18)
    try:
        calCalendar = Calendar(frame, selectmode="day", font=("Arial", 18), date_pattern="dd/mm/yyyy", year=int(str(account.dob)[-4:]), month=int(str(account.dob)[3:5]), day=int(str(account.dob)[:2]), maxdate=eighteenYearsAgo)
        calCalendar.grid(row=5, column=1, pady=10, padx=15)
    except:
        calCalendar = Calendar(frame, selectmode="day", font=("Arial", 18), date_pattern="dd/mm/yyyy", year=int(str(account.dob)[:4]), month=int(str(account.dob)[5:7]), day=int(str(account.dob)[-2:]), maxdate=eighteenYearsAgo)
        calCalendar.grid(row=5, column=1, pady=10, padx=15)

    # Bookings
    relevantBookings=[]

    with open("bookingsFile.pkl", "rb") as file:
        dictionary = pickle.load(file)
        relevantBookings = []
        for booking in dictionary.values():
            if booking.client.clientID == account.clientID:
                relevantBookings.append(booking)

    if len(relevantBookings) == 0:
        lNoBookings = ctk.CTkLabel(frame, text="No bookings to view.")
        lNoBookings.grid(row=6, column=0, pady=10)
    else:
        for i in range(len(relevantBookings)):
            if (i % 2 == 0):
                bookingFrame = ctk.CTkFrame(frame, width=175, height=175)
                bookingFrame.grid_propagate(False)
                bookingFrame.grid(column=(i % 2), row=7+i, pady=20)
            else:
                bookingFrame = ctk.CTkFrame(frame, width=175, height=175)
                bookingFrame.grid_propagate(False)
                bookingFrame.grid(column=(i % 2), row=6+i, pady=20)

            # Info
            if relevantBookings[i].isMentoring == True:
                sessionType = "Mentoring"
            else:
                sessionType = "Reading"

            # Labels
            lType = ctk.CTkLabel(bookingFrame, text=f"Type: {sessionType}")
            lType.grid(row=0, column=0, padx=10)
            lHost = ctk.CTkLabel(bookingFrame, text=f"Host: {relevantBookings[i].staff}")
            lHost.grid(row=1, column=0, padx=10)
            lDatetime = ctk.CTkLabel(bookingFrame, text=f"When: {relevantBookings[i].bookingTime}")
            lDatetime.grid(row=2, column=0, padx=10)

            # Button
            bCancelBooking = ctk.CTkButton(bookingFrame, text="Cancel Booking", command=lambda booking=relevantBookings[i], frame=bookingFrame: DeleteBooking(booking, frame, True))
            bCancelBooking.grid(row=3, column=0)
            bEditBooking = ctk.CTkButton(bookingFrame, text="Edit Booking", command=lambda booking=relevantBookings[i]: EditBookingScreen(screen, booking, account, adminsAccount, False))
            bEditBooking.grid(row=4, column=0, pady=10)

    # Buttons
    bSave = ctk.CTkButton(screen, text="Save", command=lambda:EditClientDetails(account, eFirstName.get(), eSurname.get(), eEmail.get(), ePhone.get(), calCalendar.get_date(), screen, False, adminsAccount))
    bSave.place(relx=0.3, rely=0.8, anchor="center")
    bDelete = ctk.CTkButton(screen, text="Delete Account", command=lambda:DeleteClient(account))
    bDelete.place(relx=0.7, rely=0.8, anchor="center")
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:AccountSearchScreen(screen, adminsAccount))
    bBack.place(relx=0.1, rely=0.9, anchor="e")

    screen.mainloop()

# Edit staff details, accessible from searching for the account or from staff/admin home screen
def EditStaffScreen(screenToDestroy, account, cameFromSearch, cameFromAdmin, adminsAccount):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Edit Details")
    screen.geometry("450x350+0+0")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="Account Manager", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lFullName = ctk.CTkLabel(screen, text="Full Name:")
    lFullName.place(relx=0.3, rely=0.3, anchor="e")
    lEmail = ctk.CTkLabel(screen, text="Email:")
    lEmail.place(relx=0.3, rely=0.42, anchor="e")
    lPhone = ctk.CTkLabel(screen, text="Phone Number:")
    lPhone.place(relx=0.3, rely=0.54, anchor="e")
    if (account.isHigherAdmin):
        lIsAdmin = ctk.CTkLabel(screen, text="Admin?:")
        lIsAdmin.place(relx=0.3, rely=0.66, anchor="e")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Entries
    eFirstName = ctk.CTkEntry(screen, width=100, placeholder_text="First Name")
    eFirstName.place(relx=0.4, rely=0.3, anchor="w")
    eFirstName.insert(0, account.firstName)
    eSurname = ctk.CTkEntry(screen, width=100, placeholder_text="Surname")
    eSurname.place(relx=0.67, rely=0.3, anchor="w")
    eSurname.insert(0, account.surname)
    eEmail = ctk.CTkEntry(screen, width=220, placeholder_text="Email")
    eEmail.place(relx=0.4, rely=0.42, anchor="w")
    eEmail.insert(0, account.email)
    ePhone = ctk.CTkEntry(screen, width=220, placeholder_text="Phone Number")
    ePhone.place(relx=0.4, rely=0.54, anchor="w")
    ePhone.insert(0, account.phoneNumber)

    # Tickbox
    isAdmin = BooleanVar(value=account.isHigherAdmin)
    if (account.isHigherAdmin):
        tbAdmin = ctk.CTkCheckBox(screen, text="", variable=isAdmin)
        tbAdmin.place(relx=0.4, rely=0.66, anchor="w")

    # Buttons
    bSave = ctk.CTkButton(screen, text="Save", command=lambda:EditStaffDetails(account, eFirstName.get(), eSurname.get(), eEmail.get(), ePhone.get(), isAdmin.get(), screen))
    bSave.place(relx=0.3, rely=0.78, anchor="center")
    if cameFromSearch:
        bDelete = ctk.CTkButton(screen, text="Delete Account", command=lambda:DeleteStaff(account, screen, False, adminsAccount))
    else:
        bDelete = ctk.CTkButton(screen, text="Delete Account", command=lambda:DeleteStaff(account, screen, True, None))
    bDelete.place(relx=0.7, rely=0.78, anchor="center")
    if cameFromSearch == False and cameFromAdmin == False:
        bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:StaffHomeScreen(screen, account))
        bBack.place(relx=0.1, rely=0.9, anchor="e")
    elif cameFromSearch:
        bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:AccountSearchScreen(screen, adminsAccount))
        bBack.place(relx=0.1, rely=0.9, anchor="e")
    elif cameFromAdmin:
        bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:AdminHomeScreen(screen, adminsAccount))
        bBack.place(relx=0.1, rely=0.9, anchor="e")

    screen.mainloop()

# View your bookings as a client
def ClientViewBookingsScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Your Bookings")
    screen.geometry("450x350+0+0")

    with open("bookingsFile.pkl", "rb") as file:
        dictionary = pickle.load(file)
        relevantBookings = []
        for booking in dictionary.values():
            if booking.client.clientID == account.clientID:
                relevantBookings.append(booking)
        
    # Frame
    frame = ctk.CTkScrollableFrame(screen, width=400, height=200, fg_color="#242424")
    frame.place(relx=0.5, rely=0.55, anchor="center")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Bookings
    if len(relevantBookings) == 0:
        lNoBookings = ctk.CTkLabel(screen, text="No bookings to view.")
        lNoBookings.place(relx=0.5, rely=0.2, anchor="center")
    else:
        for i in range(len(relevantBookings)):
            bookingFrame = ctk.CTkFrame(frame, width=400, height=90)
            bookingFrame.grid_propagate(False)
            bookingFrame.grid(column=0, row=i, pady=10)

            # Info
            if relevantBookings[i].isMentoring == True:
                sessionType = "Mentoring"
            else:
                sessionType = "Reading"

            # Labels
            lType = ctk.CTkLabel(bookingFrame, text=f"Type: {sessionType}")
            lType.grid(row=0, column=0, padx=10)
            lHost = ctk.CTkLabel(bookingFrame, text=f"Host: {relevantBookings[i].staff}")
            lHost.grid(row=1, column=0, padx=10)
            lDatetime = ctk.CTkLabel(bookingFrame, text=f"When: {relevantBookings[i].bookingTime}")
            lDatetime.grid(row=2, column=0, padx=10)

            # Button
            bCancelBooking = ctk.CTkButton(bookingFrame, text="Cancel Booking", command=lambda booking=relevantBookings[i], frame=bookingFrame: DeleteBooking(booking, frame, True))
            bCancelBooking.grid(row=0, column=2, padx=80)
            bEditBooking = ctk.CTkButton(bookingFrame, text="Edit Booking", command=lambda booking=relevantBookings[i]: EditBookingScreen(screen, booking, account, None, True))
            bEditBooking.grid(row=2, column=2, padx=80)
    
    # Labels
    lTitle = ctk.CTkLabel(screen, text="Manage Bookings", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Button
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:CustomerHomeScreen(screen, account))
    bBack.place(relx=0.1, rely=0.9, anchor="e")

    screen.mainloop()

# View your bookings as a staff member
def StaffViewBookingsScreen(screenToDestroy, account, returnToAdmin):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Your Bookings")
    screen.geometry("450x350+0+0")
    with open("bookingsFile.pkl", "rb") as file:
            dictionary = pickle.load(file)
            relevantBookings = []
            for booking in dictionary.values():
                if booking.staff.staffID == account.staffID:
                    relevantBookings.append(booking)
        
    # Frame
    frame = ctk.CTkScrollableFrame(screen, width=400, height=200, fg_color="#242424")
    frame.place(relx=0.5, rely=0.55, anchor="center")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Bookings
    if len(relevantBookings) == 0:
        lNoBookings = ctk.CTkLabel(screen, text="No bookings to view.")
        lNoBookings.place(relx=0.5, rely=0.2, anchor="center")
    else:
        for i in range(len(relevantBookings)):
            bookingFrame = ctk.CTkFrame(frame, width=400, height=90)
            bookingFrame.grid_propagate(False)
            bookingFrame.grid(column=0, row=i, pady=10)

            # Info
            if relevantBookings[i].isMentoring == True:
                sessionType = "Mentoring"
            else:
                sessionType = "Reading"

            # Labels
            lType = ctk.CTkLabel(bookingFrame, text=f"Type: {sessionType}")
            lType.grid(row=0, column=0, padx=10)
            lCustomer = ctk.CTkLabel(bookingFrame, text=f"Host: {relevantBookings[i].client.firstName} {relevantBookings[i].client.surname}")
            lCustomer.grid(row=1, column=0, padx=10)
            lDatetime = ctk.CTkLabel(bookingFrame, text=f"When: {relevantBookings[i].bookingTime}")
            lDatetime.grid(row=2, column=0, padx=10)

            # Button
            bCancelBooking = ctk.CTkButton(bookingFrame, text="Cancel Booking", command=lambda booking=relevantBookings[i], frame=bookingFrame: DeleteBooking(booking, frame, True))
            bCancelBooking.grid(row=1, column=2, padx=80)
    
    # Labels
    lTitle = ctk.CTkLabel(screen, text="Manage Bookings", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Button
    if (returnToAdmin == False):
        bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:StaffHomeScreen(screen, account))
        bBack.place(relx=0.1, rely=0.9, anchor="e")
    else:
        bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:AdminHomeScreen(screen, account))
        bBack.place(relx=0.1, rely=0.9, anchor="e")

    screen.mainloop()

# Edit your bookings as a client
def EditBookingScreen(screenToDestroy, booking, account, adminsAccount, returnToClientVersion):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Your Bookings")
    screen.geometry("450x350+0+0")

    # Set current staff member in case hosts change for the sake of changing available dates
    oldStaff = booking.staff

    # List of all staff names for "Hosts" combobox
    with open("staffAccountsFile.pkl", "rb") as file:
        dictionary = pickle.load(file)
        listOfNames = []
        for user in dictionary.values():
            listOfNames.append(str(user))

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="Make A Booking", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lChooseDate = ctk.CTkLabel(screen, text="Pick A Date:")
    lChooseDate.place(relx=0.3, rely=0.27, anchor="center")
    lTime = ctk.CTkLabel(screen, text="Time:")
    lTime.place(relx=0.6, rely=0.36, anchor="w")
    lHost = ctk.CTkLabel(screen, text="Host:")
    lHost.place(relx=0.6, rely=0.5, anchor="w")
    lType = ctk.CTkLabel(screen, text="Type:")
    lType.place(relx=0.6, rely=0.64, anchor="w")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Dropdowns
    selectedStaff = StringVar()
    cbTime = ctk.CTkComboBox(screen, values=["09.00", "09.30", "10.00", "10.30", "11.00", "11.30", "12.00", "12.30", "13.00", "13.30", "14.00", "14.30", "15.00", "15.30", "16.00", "16.30"], width=120)
    cbTime.place(relx=0.7, rely=0.36, anchor="w")
    cbTime.set(booking.bookingTime[-5:])
    cbHosts = ctk.CTkComboBox(screen, values=listOfNames, width=120, variable=selectedStaff)
    cbHosts.place(relx=0.7, rely=0.5, anchor="w")
    cbHosts.set(booking.staff.firstName + " " + booking.staff.surname)

    # Radio Buttons
    typeVar = ctk.BooleanVar(value=booking.isMentoring)     # For checking which type of session has been picked
    rbReading = ctk.CTkRadioButton(screen, text="Reading", variable=typeVar, value=False)
    rbReading.place(relx=0.7, rely=0.64, anchor="w")
    rbMentor = ctk.CTkRadioButton(screen, text="Mentoring", variable=typeVar, value=True)
    rbMentor.place(relx=0.7, rely=0.7)

    # Buttons
    bSave = ctk.CTkButton(screen, text="Save", command=lambda:EditBooking(booking.bookingID, booking.client, SelectStaff(selectedStaff.get()), oldStaff, cbTime.get(), calCalendar.get_date(), typeVar.get(), screen, account, adminsAccount, returnToClientVersion))
    bSave.place(relx=0.5, rely=0.85, anchor="center")
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:CustomerHomeScreen(screen, account))
    bBack.place(relx=0.1, rely=0.9, anchor="e")

    # Calendar
    rightNow = datetime.datetime.now()
    calCalendar = Calendar(screen, selectmode="day", font=("Arial", 18), date_pattern="dd/mm/yyyy", year=int(booking.bookingTime[6:10]), month=int(booking.bookingTime[3:5]), day=int(booking.bookingTime[:2]), mindate=rightNow)
    calCalendar.place(relx=0.3, rely=0.55, anchor="center")

    screen.mainloop()

# View reviews of a chosen staff member (all have access)
def ViewReviewsScreen(screenToDestroy, account, presetName, screenToGoTo):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Reviews")
    screen.geometry("450x350+0+0")

    # List of all staff names for "Hosts" combobox
    with open("staffAccountsFile.pkl", "rb") as file:
        dictionary = pickle.load(file)
        listOfNames = []
        for user in dictionary.values():
            listOfNames.append(str(user))

    # Frame
    frame = ctk.CTkScrollableFrame(screen, width=400, height=160, fg_color="#242424")
    frame._scrollbar.configure(height=0)
    frame.place(relx=0.5, rely=0.6, anchor="center")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Labels
    lTitle = ctk.CTkLabel(screen, text="View Reviews", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lChoose = ctk.CTkLabel(screen, text="Choose Staff Member:")
    lChoose.place(relx=0.22, rely=0.3, anchor="center")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Buttons
    bSearch = ctk.CTkButton(screen, text="Search", width=100, command=lambda:SearchReviews(SelectStaff(selectedStaff.get()), frame))
    bSearch.place(relx=0.8, rely=0.3, anchor="center")
    if screenToGoTo == "client":
        bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:CustomerHomeScreen(screen, account))
    elif screenToGoTo == "staff":
        bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:StaffHomeScreen(screen, account))
    elif screenToGoTo == "admin":
        bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:AdminHomeScreen(screen, account))
    bBack.place(relx=0.1, rely=0.9, anchor="e")

    # Combobox
    selectedStaff = StringVar()
    cbHosts = ctk.CTkComboBox(screen, values=listOfNames, width=135, variable=selectedStaff)
    cbHosts.place(relx=0.53, rely=0.3, anchor="center")
    if presetName != None:
        cbHosts.set(presetName)
    else:
        cbHosts.set(listOfNames[0])

    screen.mainloop()

# Search through all accounts
def AccountSearchScreen(screenToDestroy, account):
    if (screenToDestroy != None):
        screenToDestroy.destroy()
    screen = ctk.CTk()
    screen.title("Reviews")
    screen.geometry("450x350+0+0")

    # Frame
    searchFrame = ctk.CTkScrollableFrame(screen, width=400, height=120)
    searchFrame._scrollbar.configure(height=0)
    searchFrame.place(relx=0.5, rely=0.62, anchor="center")

    # Logo
    img = Image.open("V4/logo.png")
    logoImage = ctk.CTkImage(dark_image=img, size=[50, 50])
    lLogo = ctk.CTkLabel(screen, text="", image=logoImage)
    lLogo.place(relx=0.1, rely=0.1, anchor="center")

    # Label
    lTitle = ctk.CTkLabel(screen, text="Search Accounts", font=("Arial", 35))
    lTitle.place(relx=0.5, rely=0.1, anchor="center")
    lBack = ctk.CTkLabel(screen, text="Back")
    lBack.place(relx=0.11, rely=0.9, anchor="w")

    # Entries
    eFirstName = ctk.CTkEntry(screen, placeholder_text="First Name", width=100)
    eFirstName.place(relx=0.28, rely=0.25, anchor="e")
    eSurname = ctk.CTkEntry(screen, placeholder_text="Surname", width=100)
    eSurname.place(relx=0.3, rely=0.25, anchor="w")
    eEmail = ctk.CTkEntry(screen, placeholder_text="Email", width=100)
    eEmail.place(relx=0.28, rely=0.35, anchor="e")
    ePhone = ctk.CTkEntry(screen, placeholder_text="Phone Number", width=100)
    ePhone.place(relx=0.3, rely=0.35, anchor="w")

    # Buttons
    bSearch = ctk.CTkButton(screen, text="Search Accounts", command=lambda:SearchAccounts(eFirstName.get(), eSurname.get(), eEmail.get(), ePhone.get(), searchFrame, screen, account))
    bSearch.place(relx=0.78, rely=0.3, anchor="center")
    bBack = ctk.CTkButton(screen, text="[]", width=20, command=lambda:AdminHomeScreen(screen, account))
    bBack.place(relx=0.1, rely=0.9, anchor="e")

    screen.mainloop()

#############
# FUNCTIONS #
#############

# Login to the application
def Login(email, password, screenToDestroy):
    loggedIn = False

    # Check customer file, if email and password match then log in, passing through the associated account object
    try:
        with open("clientAccountsFile.pkl", "rb") as clientLoginFile:
            dictionary = pickle.load(clientLoginFile)
            for account in dictionary.values():
                if account.email == email and account.password == password:
                    loggedIn = True
                    CustomerHomeScreen(screenToDestroy, account)
                    clientLoginFile.close()
                    return
    except FileNotFoundError:
        pass
    
    # If it doesnt log in with customer accounts, try staff accounts and do the same
    try:
        with open("staffAccountsFile.pkl", "rb") as staffLoginFile:
            dictionary = pickle.load(staffLoginFile)
            for account in dictionary.values():
                if account.email == email and account.password == password:
                    loggedIn = True
                    if account.isHigherAdmin == False:
                        StaffHomeScreen(screenToDestroy, account)
                        staffLoginFile.close()
                    else:
                        AdminHomeScreen(screenToDestroy, account)
                        staffLoginFile.close()
                    return
    except FileNotFoundError:
        pass
    
    # If it fails, either email and/or password are incorrect
    if loggedIn == False:
        messagebox.showwarning("Incorrect email or password", "Incorrect email or password")

# Register a customer
def RegisterCustomer(screen, email, password, repeatedPassword, firstName, surname, phoneNumber, dateOfBirth):
    passed = True
    errorMessages = []

    # Validation
    if '@' not in email or email == "":
        passed = False
        errorMessages.append("Email is required, and must contain an '@' symbol")
    if password != repeatedPassword:
        passed = False
        errorMessages.append("Passwords do not match")
    if len(password) < 8:
        passed = False
        errorMessages.append("Password must be at least 8 characters")
    if firstName == "":
        passed = False
        errorMessages.append("First name is reqiured")
    if surname == "":
        passed = False
        errorMessages.append("Surname is required")
    if phoneNumber.isnumeric() == False or len(phoneNumber) != 11:
        passed = False
        errorMessages.append("Phone number must be 11 numbers")
    if dateOfBirth == "":
        passed = False
        errorMessages.append("You must be 18+, so date of birth is required")

    # If any information is invalid, do not continue and show what is wrong in a popup
    if passed == False:
        for error in range(len(errorMessages)):
            messagebox.showwarning("Incorrect Information", errorMessages[error])
    # If all info is valid, create a client object and add it to the file, then return to the login screen
    else:
        response = messagebox.askyesno("Verification", "Are you sure you're data is correct?")
        if response:    
            newClient = Client(GenerateClientID(), password, firstName, surname, email, phoneNumber, dateOfBirth)
            try:
                with open("clientAccountsFile.pkl", "rb") as file:
                    clientDict = pickle.load(file)
                    file.close()
                clientDict[newClient.clientID] = newClient
                with open("clientAccountsFile.pkl", "wb") as file:
                    pickle.dump(clientDict, file)
            except:
                newClient.AddToDictionary()
                with open("clientAccountsFile.pkl", "wb+") as file:
                    pickle.dump(clientDictionary, file)
            
            LoginScreen(screen)
        

# Register staff
def RegisterStaff(screenToDestroy, adminAccount, email, password, repeatedPassword, firstName, surname, phoneNumber, isAdmin):
    passed = True
    errorMessages = []

    # Validation
    if '@' not in email or email == "":
        passed = False
        errorMessages.append("Email is required, and must contain an '@' symbol")
    if password != repeatedPassword:
        passed = False
        errorMessages.append("Passwords do not match")
    if len(password) < 8:
        passed = False
        errorMessages.append("Password must be at least 8 characters")
    if firstName == "":
        passed = False
        errorMessages.append("First name is reqiured")
    if surname == "":
        passed = False
        errorMessages.append("Surname is required")
    if phoneNumber.isnumeric() == False or len(phoneNumber) != 11:
        passed = False
        errorMessages.append("Phone number must be 11 numbers")

    # If any information is invalid, do not continue and show what is wrong in a popup
    if passed == False:
        for error in range(len(errorMessages)):
            messagebox.showwarning("Incorrect Information", errorMessages[error])
    # If all info is valid, create a client object and add it to the file, then return to the login screen
    else:
        response = messagebox.askyesno("Verification", "Are you sure you're data is correct?")
        if response:
            newStaff = Staff(GenerateStaffID(), password, firstName, surname, email, phoneNumber, [], isAdmin)
            try:
                with open("staffAccountsFile.pkl", "rb") as file:
                    staffDict = pickle.load(file)
                    file.close()
                staffDict[newStaff.staffID] = newStaff
                with open("staffAccountsFile.pkl", "wb") as file:
                    pickle.dump(staffDict, file)
            except:
                newStaff.AddToDictionary()
                with open("staffAccountsFile.pkl", "wb+") as file:
                    pickle.dump(staffDictionary, file)
            
            AdminHomeScreen(screenToDestroy, adminAccount)

# Make a booking
def MakeBooking(client, staff, time, date, isMentoring):
    staffFound = False
    dateIsUnavailable = False

    # Check if the staff member exists, and if they do check if the date/time is available
    with open("staffAccountsFile.pkl", "rb") as staffFile:
        staffDict = pickle.load(staffFile)
        if staff.staffID in staffDict:
            account = staffDict[staff.staffID]
            staffFound = True
            if (date + " " + time) in account.unavailableDates:
                dateIsUnavailable = True

    # If staff isnt found, or the date is unavailable return a messagebox and allow the user to continue
    if staffFound == False:
        messagebox.showerror("Error", "Staff not found")
        return
    elif dateIsUnavailable:
        messagebox.showwarning("Date is unavailable", f"{staff} is unavailable at this time. Please choose a new date and/or time")
        return
    else:
        response = messagebox.askyesno("Verification", "Are you sure the data is correct?")
        if response:
        # Otherwise make the booking object and add it to the file (creating the file if need be)
            booking = Booking(client, staff, GenerateBookingID(), date + " " + time, isMentoring)
            booking.AddToDictionary()

            try:
                with open("bookingsFile.pkl", "rb") as file:
                    theDictionary = pickle.load(file)

                with open("bookingsFile.pkl", "wb") as file:
                    theDictionary[booking.bookingID] = booking
                    pickle.dump(theDictionary, file)
                    messagebox.showinfo("Booking Made", f"Booking with {staff} on {date} at {time} has been made! Thank you!")
            except FileNotFoundError:
                with open("bookingsFile.pkl", "wb") as file:
                    pickle.dump(bookingDictionary, file)

            with open("staffAccountsFile.pkl", "rb+") as staffFile:
                if staff.staffID in staffDict:
                    account = staffDict[staff.staffID]
                    account.unavailableDates.append(date + " " + time)

                staffFile.seek(0)
                pickle.dump(staffDict, staffFile)
                staffFile.truncate()


# Make a review
def MakeReview(staff, review, client, screenToDestroy):
    # Validate staff exists
    with open("staffAccountsFile.pkl", "rb") as file:
        staffDict = pickle.load(file)
    
    if staff.staffID not in staffDict:
        messagebox.showerror("Error", "Error: Staff Not Found")
    else:
        response = messagebox.askyesno("Verification", "Are you sure you're review is correct?")
        if response:
            # Validate review
            if review != "" and len(review) <= 150:
                newReview = Review(staff, GenerateReviewID(), review)
                try:
                    # Add it to the existing file or....
                    with open("reviewsFile.pkl", "rb") as reviewFile:
                        allReviews = pickle.load(reviewFile)
                        allReviews[newReview.reviewID] = newReview
                        reviewFile.close()
                    with open("reviewsFile.pkl", "wb") as reviewFile:
                        pickle.dump(allReviews, reviewFile)
                except:
                    # .... make a new file and add it to that
                    newReview.AddToDictionary()
                    with open("reviewsFile.pkl", "wb+") as newReviewFile:
                        pickle.dump(reviewDictionary, newReviewFile)
                
                messagebox.showinfo("Success", "Review successfully submitted. Thank you!")
                CustomerHomeScreen(screenToDestroy, client)

# Get all reviews for a staff member
def SearchReviews(staff, frame):
    relevantReviews = []
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Get all reviews to do with the selected staff member
    try:
        with open("reviewsFile.pkl", "rb") as reviewsFile:
            reviewDict = pickle.load(reviewsFile)
            for review in reviewDict.values():
                if review.staff.staffID == staff.staffID:
                    relevantReviews.append(review.review)
    except:
        relevantReviews = []
    
    # Display all relevant reviews
    if len(relevantReviews) == 0:
        lNoReviews = ctk.CTkLabel(frame, text="This staff member has no reviews. Book with them and make one!")
        lNoReviews.grid(row=0, column=0, padx=10)
    else:
        for i in range(len(relevantReviews)):
            reviewFrame = ctk.CTkFrame(frame, width=400, height=90)
            reviewFrame.grid_propagate(False)
            reviewFrame.grid(column=0, row=i, pady=10)

            # Label
            lReview = ctk.CTkLabel(reviewFrame, text=f"{relevantReviews[i]}", width=400, height=90, wraplength=380)
            lReview.grid_propagate(False)
            lReview.grid(row=0, column=0)


# Edit client details (customer version)
def EditClientDetails(account, firstName, surname, email, phone, dob, screenToDestroy, returnToClientHome, adminsAccount):
    with open("clientAccountsFile.pkl", "rb") as fileToEdit:
        clientDict = pickle.load(fileToEdit)
        for profile in clientDict.values():
            if profile.clientID == account.clientID:
                clientToEdit = profile
    
    # Validation
    errorMessages = []
    passed = True

    if '@' not in email or email == "":
        passed = False
        errorMessages.append("Email is required, and must contain an '@' symbol")
    if firstName == "" or len(firstName) > 20:
        passed = False
        errorMessages.append("First name is reqiured, and must be less than 20 characters long")
    if surname == "" or len(surname) > 20:
        passed = False
        errorMessages.append("Surname is required, and must be less than 20 characters long")
    if phone.isnumeric() == False or len(phone) != 11:
        passed = False
        errorMessages.append("Phone number must be 11 numbers")
    if dob != None and dob == "":
        passed = False
        errorMessages.append("Date of birth is required, you must be 18+")

    # If any information is invalid, do not continue and show what is wrong in a popup
    if passed == False:
        for error in range(len(errorMessages)):
            messagebox.showwarning("Incorrect Information", errorMessages[error])
    # If all info is valid, edit the client object and add it to the file, then return to the client home screen
    else:
        response = messagebox.askyesno("Verification", "Are you sure you're data is correct?")
        if response:
            if dob == None:
                clientToEdit = Client(clientToEdit.clientID, clientToEdit.password, firstName, surname, email, phone, clientToEdit.dob)
                clientDict[clientToEdit.clientID] = clientToEdit
            else:
                clientToEdit = Client(clientToEdit.clientID, clientToEdit.password, firstName, surname, email, phone, dob)
                clientDict[clientToEdit.clientID] = clientToEdit

            with open("clientAccountsFile.pkl", "wb") as editedFile:
                pickle.dump(clientDict, editedFile)
                messagebox.showinfo("Success", "Account successfully edited")

            if returnToClientHome:    
                CustomerHomeScreen(screenToDestroy, clientToEdit)
            else:
                AccountSearchScreen(screenToDestroy, adminsAccount)


# Edit staff details (admin + staff)
def EditStaffDetails(account, firstName, surname, email, phone, isAdmin, screenToDestroy):
    with open("staffAccountsFile.pkl", "rb") as fileToEdit:
        staffDict = pickle.load(fileToEdit)
        for profile in staffDict.values():
            if profile.staffID == account.staffID:
                staffToEdit = profile
    
    # Validation
    errorMessages = []
    passed = True
    if '@' not in email or email == "":
        passed = False
        errorMessages.append("Email is required, and must contain an '@' symbol")
    if firstName == "" or len(firstName) > 20:
        passed = False
        errorMessages.append("First name is reqiured, and must be less than 20 characters long")
    if surname == "" or len(surname) > 20:
        passed = False
        errorMessages.append("Surname is required, and must be less than 20 characters long")
    if phone.isnumeric() == False or len(phone) != 11:
        passed = False
        errorMessages.append("Phone number must be 11 numbers")

    # If any information is invalid, do not continue and show what is wrong in a popup
    if passed == False:
        for error in range(len(errorMessages)):
            messagebox.showwarning("Incorrect Information", errorMessages[error])
    # If all info is valid, edit the staff object and add it to the file, then return to the staff home screen
    else:
        response = messagebox.askyesno("Verification", "Are you sure you're data is correct?")
        if response:
            staffToEdit = Staff(staffToEdit.staffID, staffToEdit.password, firstName, surname, email, phone, [], isAdmin)
            staffDict[staffToEdit.staffID] = staffToEdit

            with open("staffAccountsFile.pkl", "wb") as editedFile:
                pickle.dump(staffDict, editedFile)
                messagebox.showinfo("Success", "Account successfully edited")
            
            if(staffToEdit.isHigherAdmin):
                AdminHomeScreen(screenToDestroy, staffToEdit)
            else:
                StaffHomeScreen(screenToDestroy, staffToEdit)

# Delete client account (admin + customers)
def DeleteClient(accountToDelete, screenToDestroy):
    response = messagebox.askyesno("Verification", "Are you sure?")
    if response:
        with open("clientAccountsFile.pkl", "rb") as findClientFile:
            allClients = pickle.load(findClientFile)
        
        relevantBookings = []

        if accountToDelete.clientID in allClients:
            allClients.pop(accountToDelete.clientID) 
            messagebox.showinfo("Account deleted", "Your account has been officially deleted")

            try:
                with open("bookingsFile.pkl", "rb") as bookingFile:
                    bookingDict = pickle.load(bookingFile)
                    for booking in bookingDict.values():
                        if booking.client.clientID == accountToDelete.clientID:
                            relevantBookings.append(booking)
                
                for i in range(len(relevantBookings)):
                    DeleteBooking(relevantBookings[i], None, False)
            except:
                pass
        
        with open("clientAccountsFile.pkl", "wb") as clientFile:
            pickle.dump(allClients, clientFile)
        
        LoginScreen(screenToDestroy)

# Delete staff account (admin only)
def DeleteStaff(accountToDelete, screenToDestroy, returnToLogin, adminsAccount):
    response = messagebox.askyesno("Verification", "Are you sure?")
    if response:
        with open("staffAccountsFile.pkl", "rb") as findStaffFile:
            allStaff = pickle.load(findStaffFile)
        
        relevantBookings = []

        if accountToDelete.staffID in allStaff:
            allStaff.pop(accountToDelete.staffID)
            messagebox.showinfo("Account deleted", "Your account has been officially deleted")

            try:
                with open("bookingsFile.pkl", "rb") as bookingFile:
                    bookingDict = pickle.load(bookingFile)
                    for booking in bookingDict.values():
                        if booking.staff.staffID == accountToDelete.staffID:
                            relevantBookings.append(booking)
                
                for i in range(len(relevantBookings)):
                    DeleteBooking(relevantBookings[i], None, False)
            except FileNotFoundError:
                pass
        
        with open("staffAccountsFile.pkl", "wb") as staffFile:
            pickle.dump(allStaff, staffFile)
        
        if returnToLogin:
            LoginScreen(screenToDestroy)
        else:
            AccountSearchScreen(screenToDestroy, adminsAccount)

# Cancel a booking (admin + customers)
def DeleteBooking(bookingToDelete, frameToDestroy, notification):
    if(notification):
        response = messagebox.askyesno("Verification", "Are you sure?")
    else:
        response = True
    if response:
        # Get all bookings
        with open("bookingsFile.pkl", "rb") as file:
            bookings = pickle.load(file)
            
        # If the booking exists, delete it
        if bookingToDelete.bookingID in bookings:
            bookings.pop(bookingToDelete.bookingID)
            if (notification == True):
                messagebox.showinfo("Booking Cancelled", "Booking has been cancelled")
            if frameToDestroy != None:
                frameToDestroy.destroy()
        else:
            if (notification == True):
                messagebox.showerror("Error", "Booking not found")

        with open("staffAccountsFile.pkl", "rb") as file:
            staffDict = pickle.load(file)
            for staff in staffDict.values():
                if staff.staffID == bookingToDelete.staff.staffID:
                    if bookingToDelete.bookingTime in staff.unavailableDates:
                        staff.unavailableDates.remove(bookingToDelete.bookingTime)
                        break

        # Save
        with open("bookingsFile.pkl", "wb") as file:
            pickle.dump(bookings, file)
        with open("staffAccountsFile.pkl", "wb") as file:
            pickle.dump(staffDict, file)

# Edit a booking
def EditBooking(id, client, staff, oldStaff, time, date, isMentoring, screenToDestroy, account, adminsAccount, returnToClientsVer):
    # Load staff data
    with open("staffAccountsFile.pkl", "rb") as staffFile:
        staffDict = pickle.load(staffFile)
    
    with open("bookingsFile.pkl", "rb") as bookingsFile:
        bookings = pickle.load(bookingsFile)

    staffAccount = staffDict[staff.staffID]
    oldStaffAccount = staffDict[oldStaff.staffID]

    if (date + " " + time) in staffAccount.unavailableDates:
        messagebox.showerror("Date Unavailable", f"Sorry, {staff} is unavailable at that time. Please select a new date/time")
    else:
        response = messagebox.askyesno("Verification", "Are you sure you're data is correct?")
        if response:
            oldStaffAccount.unavailableDates.remove(bookings[id].bookingTime)
            staffAccount.unavailableDates.append(date + " " + time)

            # Locate the booking and replace it with the updated booking
            bookingToEdit = bookings[id]
            newBooking = Booking(client, staff, id, date + " " + time, isMentoring)
            bookings[bookingToEdit.bookingID] = newBooking
            messagebox.showinfo("Success", "Booking successfully edited")

            # Save the updated staff data
            with open("staffAccountsFile.pkl", "wb") as staffFile:
                pickle.dump(staffDict, staffFile)

            # Save the updated bookings data
            with open("bookingsFile.pkl", "wb") as file:
                pickle.dump(bookings, file)

            # Navigate to the appropriate screen
            if returnToClientsVer:
                ClientViewBookingsScreen(screenToDestroy, account)
            else:
                AccountSearchScreen(screenToDestroy, adminsAccount)


# Search all accounts (admins only)
def SearchAccounts(firstName, surname, email, phone, frameToAddTo, screenToDestroy, adminsAccount):
    results = []
    for widget in frameToAddTo.winfo_children():
        widget.destroy()

    # Get all accounts
    with open("clientAccountsFile.pkl", "rb") as clientFile:
        clientDict = pickle.load(clientFile)
    with open("staffAccountsFile.pkl", "rb") as staffFile:
        staffDict = pickle.load(staffFile)

    # Remove item from "match" list if it doesnt match any non blank fields
    for client in clientDict.values():
        match = True
        if firstName != "" and client.firstName != firstName:
            match = False
            continue
        if surname != "" and client.surname != surname:
            match = False
            continue
        if email != "" and client.email != email:
            match = False
            continue
        if phone != "" and client.phoneNumber != phone:
            match = False
            continue

        if match:
            results.append(client)
    
    # Do not add item to "match" list if it doesnt match any non blank fields
    for staff in staffDict.values():
        match = True
        if firstName != "" and staff.firstName != firstName:
            match = False
            continue
        if surname != "" and staff.surname != surname:
            match = False
            continue
        if email != "" and staff.email != email:
            match = False
            continue
        if phone != "" and staff.phoneNumber != phone:
            match = False
            continue

        if match:
            results.append(staff)
    
    # Display them all
    for i in range(len(results)):
        accountFrame = ctk.CTkFrame(frameToAddTo, width=400, height=30)
        accountFrame.grid_propagate(False)
        accountFrame.grid(row=i, column=0, pady=10)

        # Info
        if type(results[i]) is Client:
            accountType = "Client"
            isClient = True
        if type(results[i]) is Staff:
            if results[i].isHigherAdmin == True:
                accountType = "Admin"
                isClient = False
            else:
                accountType = "Staff"
                isClient = False
        
        # Labels
        lFullName = ctk.CTkLabel(accountFrame, text=f"{results[i].firstName} {results[i].surname}, ")
        lFullName.grid(row=0, column=0)
        lAccType = ctk.CTkLabel(accountFrame, text=f"{accountType} Account")
        lAccType.grid(row=0, column=1)

        # Button
        if isClient:
            bManage = ctk.CTkButton(accountFrame, text="Manage", command=lambda account=results[i]: (print(account.dob), MoreDetailEditClientsScreen(screenToDestroy, account, adminsAccount)))
            bManage.grid(row=0, column=2, padx=30)
        else:
            bManage = ctk.CTkButton(accountFrame, text="Manage", command=lambda account=results[i]: EditStaffScreen(screenToDestroy, account, True, False, adminsAccount))
            bManage.grid(row=0, column=2, padx=30)

# Generate a client id based on dictionary
def GenerateClientID():
    try:
        with open("clientAccountsFile.pkl", "rb") as file:
            dictionary = pickle.load(file)
            return len(dictionary) + 1
    except:
        with open("clientAccountsFile.pkl", "wb") as file:
            pickle.dump({}, file)
        return 1

# Generate a staff id based on dictionary
def GenerateStaffID():
    try:
        with open("staffAccountsFile.pkl", "rb") as file:
            dictionary = pickle.load(file)
            return len(dictionary) + 1
    except:
        with open("staffAccountsFile.pkl", "wb") as file:
            pickle.dump({}, file)
        return 1

# Generate a booking id based on dictionary
def GenerateBookingID():
    try:
        with open("bookingsFile.pkl", "rb") as file:
            dictionary = pickle.load(file)
            return len(dictionary) + 1
    except:
        with open("bookingsFile.pkl", "wb") as file:
            pickle.dump({}, file)
        return 1

# Generate a review id based on dictionary
def GenerateReviewID():
    try:
        with open("reviewsFile.pkl", "rb") as file:
            dictionary = pickle.load(file)
            return len(dictionary) + 1
    except:
        return 1

# Get all staff names using the Staff object's __str__, compare that to the name selected in the combobox, if it matches then the staff object is found
def SelectStaff(value):
    with open("staffAccountsFile.pkl", "rb") as file:
        dictionary = pickle.load(file)
        staffList = [(str(staff), staff) for staff in dictionary.values()]
        for name, staff in staffList:
            if name == value:
                return staff

################
# MAIN PROGRAM #
################

try:
    with open("staffAccountsFile.pkl", "rb") as file:
        dictionary = pickle.load(file)
        if (len(dictionary) == 0):
            newStaff = Staff(GenerateStaffID(), "adminpassword", "Andrea", "Bittencourt", "andrea@hte.com", "12345678900", [], True)
            newStaff.AddToDictionary()
            pickle.dump(staffDictionary, file)
except:
    with open("staffAccountsFile.pkl", "wb+") as file:
        newStaff = Staff(GenerateStaffID(), "adminpassword", "Andrea", "Bittencourt", "andrea@hte.com", "12345678900", [], True)
        newStaff.AddToDictionary()
        pickle.dump(staffDictionary, file)

LoginScreen(None)