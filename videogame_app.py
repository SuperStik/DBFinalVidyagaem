#imports
from helper import helper
from db_operations import db_operations

db_ops = db_operations()

# def userSignIn():
#    global userID
#    global username
#    global password
#    username = input("Enter Username ")
#    password = input("Enter Password ")
#    query = '''SELECT username, password
#        FROM user
#        WHERE password = '%(password)s';
#        '''
#    params = {"password": password}
#    result = db_ops.select_query_params(query, params)
#    if result:
#        if result[0][0] == username and result[0][1] == password:
#            print("Successfully logged in\n")
#            return True
#        else:
#            print("\nUsername and password do not match. Try again.\n")
#            return False
#    else:
#            print("\nUsername and password do not match. Try again.\n")
#            return False

def createAccount():
   username = input("Enter a username.\n")
   query = '''SELECT COUNT(*)
   FROM user
   WHERE username = %s;
   '''
   params = (username,)
   result = db_ops.single_record_params(query, params)
   if (result != 0):
       print("That username is taken. Please try again.")
       createAccount()
   else:
       password = input("Username is available. Enter a password.\n")
       firstName = input("What is your first name?\n")
       lastName = input("What is your last name?\n")
       birthdate = input("What is your birthdate? (Enter as YYYY-MM-DD)\n")
       query = '''INSERT INTO user (username, password, firstName, lastName, birthday)
       VALUES (%s, %s, %s, %s, %s);
       '''
       params = (username, password, firstName, lastName, birthdate)
       db_ops.modify_query_params(query, params)
       print("Your account has been created!\n")

# def changePassword():
#    username = input("Enter Username ")
#    password = input("Enter Password ")
#    query = '''SELECT username, password
#        FROM user
#        WHERE password = '%(password)s';
#        '''
#    params = {"password": password}
#    result = db_ops.select_query_params(query, params)
#    if result:
#        if result[0][0] == username and result[0][1] == password:
#            password = input("Enter New Password ")
#            query = '''UPDATE user
#                SET password = '%(password)s'
#                WHERE user = '%(username)s';
#                '''
#            params = {"username": username, "password": password}
#            db_ops.modify_query_params(query, params)
#        else:
#            print("\nUsername and password do not match. Try again.\n")
#    else:
#            print("\nUsername and password do not match. Try again.\n")

# def displayGame(gameID):
#    query = '''SELECT video_game.name, datePublished, minimumAge, genre, studio.name AS studio, AVG(review.rating) AS average rating
#    FROM video_game
#    INNER JOIN review
#    ON video_game.gameID = review.gameID
#    INNER JOIN studio
#    ON studio.studioID = game.studioID
#    WHERE video_game.gameID = %(gameID)s
#    GROUP BY video_game.gameID;
#    '''
#    params = {"gameID": gameID}
#    results = db_ops.select_query_params(query, params)

# def searchByName():
#    search = input("Search for a game by name")
#    query = '''SELECT gameID FROM video_game
#    WHERE name = %(name)s
#    '''
#    params = {"name": search}
#    result = db_ops.single_attribute_params(query, params)
  
#    displayGame(result)


# def searchByPlatform():
#    search = input("Search for a game by platform")
#    query = '''SELECT gameID FROM video_game
#    WHERE platform = %(platform)s
#    '''
#    params = {"platform": search}
#    result = db_ops.single_attribute_params(query, params)
  
#    displayGame(result)

# def searchByAge():
#    search = input("Search for a game by age rating")
#    query = '''SELECT gameID FROM video_game
#    WHERE minimumAge = %(age)s
#    '''
#    params = {"age": search}
#    result = db_ops.single_attribute_params(query, params)
  
#    displayGame(result)

# def searchByDev():
#    search = input("Search for a game by developer")
#    query = '''SELECT gameID
#    FROM video_game
#    INNER JOIN studio
#    ON video_game.studioID = studio.studioID
#    WHERE studio.name = %(dev)s
#    '''
#    params = {"dev": search}
#    result = db_ops.select_query_params(query, params)


#    displayGame(result)

# def addToWishlist(gameID):
#    query = '''INSERT INTO wishlists (userID, gameID)
#    VALUES (%(userID)s, %(gameID)s);
#    '''
#    params = {"userID": userID, "gameID": gameID}
#    db_ops.select_query_params(query, params)

# def viewWishlist():
#    query = '''SELECT *
#    FROM wishlist
#    WHERE userID = %(userID)s;
#    COMMIT;
#    '''
#    params = {"userID": userID}
#    db_ops.select_query_params(query, params)

# def removeFromWishlist(gameID):
#    query = '''DELETE wishlists
#    FROM wishlists
#    WHERE userID = %(userID)s AND gameID = %(gameID)s;
#    '''
#    params = {"userID": userID, "gameID": gameID}
#    db_ops.select_query_params(query, params)

# def addToLibrary(gameID):
#    query = '''INSERT INTO games_owned (userID, gameID)
#    VALUES (%(userID)s, %(gameID)s);
#    '''
#    params = {"userID": userID, "gameID": gameID}
#    db_ops.select_query_params(query, params)

# def addToLibraryFromWishlist(gameID):
#    query = '''
#    START TRANSACTION;
#    INSERT INTO games_owned (userID, gameID)
#    VALUES (%(userID)s, %(gameID)s);
#    SAVEPOINT actor_savepoint;
#    DELETE wishlists
#    FROM wishlists
#    WHERE userID = %(userID)s AND gameID = %(gameID)s;
#    COMMIT;
#    '''
#    params = {"userID": userID, "gameID": gameID}
#    db_ops.select_query_params(query, params)

# def writeReview(rating, description, gameID):
#    query = '''INSERT INTO review (userID, date, rating, description, gameID)
#    VALUES (%(userID)s, NOW(), %(rating)s, '\'%(description)s\'', %(gameID)s);
#    '''
#    params = {"userID": userID, "rating": rating, "description": description, "gameID": gameID}
#    db_ops.select_query_params(query, params)


#main method
createAccount()

db_ops.destructor()