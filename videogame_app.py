#imports
from helper import helper
from db_operations import db_operations

db_ops = db_operations()

#accepts a username and password to let the user sign in
def userSignIn():
    #get all usernames
    query = '''
    SELECT username
    FROM user;
    '''
    usernames = db_ops.select_query(query)
    #user must enter a valid username
    while True:
        username = input("Enter your username: ")
        if (username,) in usernames:
            break
        else:
            print("That username does not exist. Please enter a valid username.")

    #get correct password for the username
    query = '''
    SELECT password, userID
    FROM user
    WHERE username = %s;
    '''
    params = (username,)
    result = db_ops.select_query_params(query, params)
    userID = result[0][1]

    #user must enter a valid password
    while True:
        password = input("Enter your password: ")
        if password == result[0][0]:
            break
        else:
            print("That password is incorrect.")
    
    #confirm sign in
    print(f"Successfully signed in as {username}!")
    return userID

#create a new account with a new username
#creates a record
def createAccount():
    #get all usernames
    query = '''
    SELECT username
    FROM user;
    '''
    usernames = db_ops.select_query(query)
    #user must enter an unused username
    while True:
        username = input("Enter your username: ")
        if (username,) in usernames:
            print("That username is taken. Please enter a valid username.")
        else:
            break
    #get a password and other information
    password = input("Username is available. Enter a password: ")
    firstName = input("What is your first name? ")
    lastName = input("What is your last name? ")
    birthdate = input("What is your birthdate? (Enter as YYYY-MM-DD): ")
    #create record for new user
    query = '''
    INSERT INTO user (username, password, firstName, lastName, birthday)
    VALUES (%s, %s, %s, %s, %s);
    '''
    params = (username, password, firstName, lastName, birthdate)
    db_ops.modify_query_params(query, params)
    print("Your account has been created!")
    #return the new user's ID
    query = '''
    SELECT userID
    FROM user
    WHERE username = %s;
    '''
    params = (username,)
    result = db_ops.select_query_params(query, params)
    return result[0][0]
    
#change the password of the current user (username)
#updates a record
def changePassword(userID):
    #get current user's password
    query = '''
    SELECT password
    FROM user
    WHERE userID = %s;
    '''
    params = (userID,)
    result = db_ops.select_query_params(query, params)
    #check password before changing
    while True:
        password = input("Enter your current password: ")
        if password == result[0][0]:
            break
        else:
            print("That password is incorrect.")
    #get new password
    newPassword = input("Accepted. Enter your new password: ")
    query = '''
    UPDATE user
    SET password = %s
    WHERE userID = %s;
    '''
    params = (newPassword, userID)
    db_ops.modify_query_params(query, params)
    print("Password successfully changed.")

#display info for a selected game
#aggregate/GROUPBY, joining 3 tables
def displayGame(gameID):
    query = '''
    SELECT video_game.name, datePublished, minimumAge, genre, studio.name, AVG(review.rating) AS avg_rating
    FROM video_game
    INNER JOIN review
    ON video_game.gameID = review.gameID
    INNER JOIN studio
    ON studio.studioID = video_game.studioID
    WHERE video_game.gameID = %s
    GROUP BY video_game.gameID;
    '''
    params = (gameID,)
    results = db_ops.select_query_params(query, params)
    print("Game Details:")
    print(f"Name: {results[0][0]}")
    print(f"Date Published: {results[0][1]}")
    print(f"Minimum Age: {results[0][2]}")
    print(f"Genre: {results[0][3]}")
    print(f"Studio: {results[0][4]}")
    print(f"Average Rating: {results[0][5]}")

#display all games in the database
def displayAllGames():
    #get all games
    query = '''
    SELECT gameID, name
    FROM video_game;
    '''
    results = db_ops.select_query(query)
    options = []
    #print out all games 
    print("All Games:")
    for i in results:
        print(f"ID {i[0]}: {i[1]}")
        options.append(i[0])
    print("")
    #return IDs of games
    return options

#find games by title
def searchByName():
    #get a name from user
    user_search = input("Enter a game title to search for: ")
    search = f"%{user_search}%"
    #search for titles that include the user's search
    query = '''
    SELECT gameID, name
    FROM video_game
    WHERE name LIKE %s
    '''
    params = (search,)
    result = db_ops.select_query_params(query, params)
    options = []
    #print results
    print("Results:")
    for i in result:
        print(f"ID {i[0]}: {i[1]}")
        options.append(i[0])
    print("")
    if len(options) == 0:
        print(f"Database has no games with titles that include \"{user_search}\".")
    #return IDS of games found
    return options

#find games by age rating
def searchByAge():
    #get an age from user
    age = input("Enter an age to search for: ")
    #find games that are approved for that age (minimum age is less than or equal to the input age)
    query = '''
    SELECT gameID, name
    FROM video_game
    WHERE minimumAge <= %s
    '''
    params = (age,)
    result = db_ops.select_query_params(query, params)
    options = []
    #print results
    print("Results:")
    for i in result:
        print(f"ID {i[0]}: {i[1]}")
        options.append(i[0])
    print("")
    if len(options) == 0:
        print(f"Database has no games with minimum age rating less than or equal to {age}.")
    #return IDS of games found
    return options

#find all games available on a specific platform
#uses a subquery
def searchByPlatform():
    #get all platforms and print out options
    query = '''
    SELECT platformID, name
    FROM platform;
    '''
    platforms = db_ops.select_query(query)
    platform_options = []
    print("Search for games on one of the following platforms:")
    for i in platforms:
        print(f"Enter {i[0]} for {i[1]}")
        platform_options.append(i[0])
    print("")
    #have user choose a platform to filter by
    pID = helper.get_choice(platform_options)
    #display all games on that platform
    query = '''
    SELECT gameID, name
    FROM video_game
    WHERE gameID IN(
        SELECT gameID
        FROM game_platform
        WHERE platformID = %s);
    '''
    params = (pID,)
    result = db_ops.select_query_params(query, params)
    options = []
    print("Games available on that platform:")
    for i in result:
        print(f"ID {i[0]}: {i[1]}")
        options.append(i[0])
    print("")
    #return IDS of games found
    return options

#display all reviews in the database
#joins 3 tables
def displayAllReviews():
    query = '''
    SELECT video_game.name, user.username, review.date, review.rating, review.description
    FROM review
    INNER JOIN video_game
    ON review.gameID = video_game.gameID
    INNER JOIN user
    ON review.userID = user.userID;
    '''
    results = db_ops.select_query(query)
    print("All Reviews:")
    for i in results:
        print(f"User {i[1]} reviewed {i[0]} on {i[2]}")
        print(f"Rating: {i[3]}. Description: {i[4]}")
        print("")

#display reviews for a specific game
#joins 3 tables
def displayGameReviews(gameID):
    query = '''
    SELECT video_game.name, user.username, review.date, review.rating, review.description
    FROM review
    INNER JOIN video_game
    ON review.gameID = video_game.gameID
    INNER JOIN user
    ON review.userID = user.userID
    WHERE video_game.gameID = %s;
    '''
    params = (gameID,)
    results = db_ops.select_query_params(query, params)
    print(f"User reviews for {results[0][0]}:")
    for i in results:
        print(f"Written by user {i[1]} on {i[2]}:")
        print(f"Rating: {i[3]}. Description: {i[4]}")
        print("")

#add a game to the user's wishlist
def addToWishlist(userID, gameID):
    #first, check if the game is already in the wishlist
    query = '''
    SELECT COUNT(*)
    FROM wishlists
    WHERE userID = %s AND gameID = %s;
    '''
    params = (userID, gameID)
    result = db_ops.select_query_params(query, params)
    #don't add if the game is already in the wishlist
    if result[0][0] > 0:
        print("This game is already on your wishlist.")
        return
    #otherwise, add the game to the wishlist
    query = '''
    INSERT INTO wishlists (userID, gameID)
    VALUES (%s, %s);
    '''
    params = (userID, gameID)
    db_ops.modify_query_params(query, params)
    print("Game successfully added to your wishlist.")

#display the games in the user's wishlist
def viewWishlist(userID):
    query = '''
    SELECT video_game.gameID, video_game.name
    FROM video_game
    INNER JOIN wishlists
    ON video_game.gameID = wishlists.gameID
    WHERE wishlists.userID = %s;
    '''
    params = (userID,)
    result = db_ops.select_query_params(query, params)
    options = []
    print("Your Wishlist:")
    for i in result:
        print(f"ID {i[0]}: {i[1]}")
        options.append(i[0])
    print("")
    if len(options) == 0:
        print("Your wishlist is empty.")
    #return IDS of games in the wishlist
    return options

#remove a game from the user's wishlist
#deletes a record
def removeFromWishlist(userID, gameID):
    query = '''
    DELETE FROM wishlists
    WHERE userID = %s AND gameID = %s;
    '''
    params = (userID, gameID)
    db_ops.modify_query_params(query, params)
    print("Game successfully removed from your wishlist.")

#add a game to the user's library from their wishlist
#transaction - deletes a record from the wishlist and adds a record to the library
def addToLibraryFromWishlist(userID, gameID):
    try:
        #add the game to the user's library
        query1 = '''
        INSERT INTO games_owned (userID, gameID)
        VALUES (%s, %s);
        '''
        params = (userID, gameID)
        db_ops.cursor.execute(query1, params)
        #delete the game from the user's wishlist
        query2 = '''
        DELETE FROM wishlists
        WHERE userID = %s AND gameID = %s;
        '''
        db_ops.cursor.execute(query2, params)
        db_ops.connection.commit()
        print("Game successfully added to your library.")
    except db_ops.connection.Error as error:
        #rollback the transaction if an error occurs
        print("Failed to update record to database rollback: {}".format(error))
        db_ops.connection.rollback()

#displays the games in the user's library
def viewLibrary(userID):
    query = '''
    SELECT video_game.gameID, video_game.name
    FROM video_game
    INNER JOIN games_owned
    ON video_game.gameID = games_owned.gameID
    WHERE games_owned.userID = %s;
    '''
    params = (userID,)
    result = db_ops.select_query_params(query, params)
    options = []
    print("Your Library:")
    for i in result:
        print(f"ID {i[0]}: {i[1]}")
        options.append(i[0])
    print("")
    if len(options) == 0:
        print("Your library is empty.")
    #return IDS of games in the library
    return options

#method for the user's options after a search
def afterSearch(options):
    print("To select a game, enter its ID. Enter 0 to return to the menu.")
    gameID = helper.get_choice(options)
    if gameID == 0:
        print("Returning to menu.")
    else:
        #display the user's selection
        displayGame(gameID)
        print("")
        print("Select from the following options:")
        print("1. See the reviews for this game.")
        print("2. Add this game to your wishlist.")
        print("3. Return to the menu.")
        choice = helper.get_choice([1,2,3])
        if choice == 1:
            displayGameReviews(gameID)
            input("Press enter to continue.")
        elif choice == 2:
            addToWishlist(currentUser, gameID)
            print("Returning to menu.")
        else:
            print("Returning to menu.")


#main method
print("Welcome to the Video Game Database!")
print("Enter 1 to sign in. Enter 2 to create a new account.")
choice = helper.get_choice([1,2])
if choice == 1:
    currentUser = userSignIn()
else:
    currentUser = createAccount()
print("")
#menu
while True:
    print("MENU:\nChoose from the following options:")
    print("1. View all games in database")
    print("2. Search for games by title")
    print("3. Search for games by age rating")
    print("4. Search for games by platform")
    print("5. View all reviews in database")
    print("6. View your wishlist")
    print("7. View your library")
    print("8. Change your password")
    print("9. Exit")
    choice = helper.get_choice([1,2,3,4,5,6,7,8,9])
    if choice == 1:
        #view all games
        options = displayAllGames()
        options.append(0)
        afterSearch(options)
    if choice == 2:
        #search by name
        options = searchByName()
        options.append(0)
        afterSearch(options)
    if choice == 3:
        #search by age
        options = searchByAge()
        options.append(0)
        afterSearch(options)
    if choice == 4:
        #search by platform
        options = searchByPlatform()
        options.append(0)
        afterSearch(options)
    if choice == 5:
        #view all reviews
        displayAllReviews()
        input("Press enter to continue.")
    if choice == 6:
        #view user wishlist
        options = viewWishlist(currentUser)
        options.append(0)
        print("To select a game, enter its ID. Enter 0 to return to the menu.")
        gameID = helper.get_choice(options)
        if gameID == 0:
            print("Returning to menu.")
        else:
            #display the user's selection
            displayGame(gameID)
            print("")
            print("Select from the following options:")
            print("1. See the reviews for this game.")
            print("2. Remove this game from your wishlist.")
            print("3. Add this game to your library.")
            print("4. Return to the menu.")
            choice = helper.get_choice([1,2,3,4])
            if choice == 1:
                displayGameReviews(gameID)
                input("Press enter to continue.")
            elif choice == 2:
                removeFromWishlist(currentUser, gameID)
                print("Returning to menu.")
            elif choice == 3:
                addToLibraryFromWishlist(currentUser, gameID)
                print("Returning to menu.")
            else:
                print("Returning to menu.")
    if choice == 7:
        #view user library
        options = viewLibrary(currentUser)
        options.append(0)
        print("To select a game, enter its ID. Enter 0 to return to the menu.")
        gameID = helper.get_choice(options)
        if gameID == 0:
            print("Returning to menu.")
        else:
            #display the user's selection
            displayGame(gameID)
            print("")
            print("Select from the following options:")
            print("1. See the reviews for this game.")
            print("2. Return to the menu.")
            choice = helper.get_choice([1,2])
            if choice == 1:
                displayGameReviews(gameID)
                input("Press enter to continue.")
            else:
                print("Returning to menu.")
    if choice == 8:
        #change password
        changePassword(currentUser)
        print("Returning to menu.")
    if choice == 9:
        #exit
        print("Exiting")
        break

db_ops.destructor()