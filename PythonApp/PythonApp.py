# Import modules - in order for script to run as intended 
import pymysql
import pymongo

# Import files that make connections to the mongo and sql databases
import sqlDBconn
import mongoDBconn

# Creation of main function
def main():

    # Creation of function
    def film_actor_menu():
        print("Films")
        print("-" * 5)
        # Utilise function within the sql connection file
        cursor = sqlDBconn.get_films_cursor()
        # Set size for how many entries to display
        fetch_size = 5
        # Creation of while loop i.e., iterate through the database
        while True:
            filmactors = cursor.fetchmany(size=fetch_size)
            # Conditional statement when no more entires can be displayed
            if (len(filmactors) < 1):
                print("No more records, returning to the main menu")
                break
            # Iterate through database and print each filmname and actorname
            for filmactor in filmactors:
                print(filmactor["filmname"],  "|", filmactor["actorname"])
            # Creation of option for user to quit i.e., break out of loop
            choice = input("-- Quit (q) --")
            if (choice == "q" or choice == "Q"):
                break
    # Create function
    def actors_dob_gender():
        # variable: prompts user to make a selection
        gender_select = "Please select male or female"

        print("")
        print("Actors")
        print("-" * 6)

        # Prompt user to enter year of birth
        while True:
            try:
                dob = int(input("Year of Birth :"))
                break
            # must be an integer
            except ValueError:
                print("")
                print("Please Enter a Valid Year")

        # prompt user to select gender
        gender = str(input("Gender (Male/Female):"))
        while True:
            # conditional statements for either male or female
            if (gender == "male" or gender == "Male" or gender == "female" or gender == "Female"):
                # connect to the sql database and make query
                actors = sqlDBconn.actors_dob_gen(dob, gender)
                print("")
                print("Actors")
                print("-" * 6)
                # iterate through the database and print actor name, dob, and gender
                for actor in actors:
                    print(actor["actorname"], "|", actor["month"],
                          "|", actor["actorgender"])
                break
            # conditional statement for when no gender is selected i.e., blank
            elif (gender == ""):
                print("No Gender Selected")
                # connect to sql database
                actors_gen = sqlDBconn.actors_dob(dob)
                print("")
                print("Actors")
                print("-" * 6)
                 # iterate through the database and print actor name, dob, and gender i.e., both male and female are printed
                for actor in actors_gen:
                    print(actor["actorname"], "|", actor["month"],
                          "|", actor["actorgender"])
                break
            # Creation of conditional statement that prompts user to enter a gender when above conditions are not satisfied        
            else:
                print(gender_select)
                gender = str(input("Gender (Male/Female):"))

    def movie_studio():
        while True:
            # connect to db
            studios = sqlDBconn.movie_studio()
            print("Studios")
            print("-" * 7)
            # iterate through database and print StudioID and StudioName
            for studio in studios:
                print(studio["StudioID"], "|", studio["StudioName"], "\n")
            break

    def view_countries_table():
        while True:
            # connect to database
            print("")
            countries = sqlDBconn.view_countries_table()
            print("Country Table")
            print("-" * 13)
            # iterate through database and print countryid and countryname
            for country in countries:
                print(country["CountryID"], "|", country["CountryName"])
            print("-" * 13)
            break

    def add_country():
        print("Add New Country")
        print("-" * 15)
        # prompt user to enter a countryid
        while True:
            try:
                cid = int(input("ID :"))
                break
            # must be an integer
            except ValueError:
                print("\n" "Please Enter an ID Number" "\n")
        # prompt user to enter country name
        while True:
            cname = str(input("Name :"))
            break
        # add the countryid and country name to the database        
        while True:
            try:
                if cname != "":
                    sqlDBconn.add_country(cid, cname)
                    print("\n" "CountryID and Name successfully added" "\n")
                    break
            # duplicate entries cannot be made    
            except pymysql.err.IntegrityError:
                print("\n" "*** Error ***: ID and/or Name" " " "(" ' ' "%d" %
                      cid + ',' + ' ' + cname + ' ' ")"  ' '  "already exists" "\n")
                break
            # when the above conditons are not satisfied, prompt user to enter a country name
            else:
                print("\n" "Please Enter a Country Name" "\n")
                cname = str(input("Name :"))


    def delete_country():
        varx = "Delete Table Entry via Country ID Reference"
        print(varx)
        print("-" * len(varx))
        # prompt user to entry country id
        cid = int(input("ID :"))
        # sql query that checks whether a country id exists
        check_id = sqlDBconn.check_country(cid)
        while True:
            # iterate through the database
            for check in check_id:
                check["CheckExists"]
            # if the country ID does not exist i.e., a value of 0 is returned
            if check["CheckExists"] == 0:
                # provide user with an error
                sqlDBconn.check_country(cid)
                print("\n" "*** ERROR ***: Country with id:",
                        cid, "does not exist within the country table" "\n")
                break
            else:
                # country is deleted from database, based on the id entered
                sqlDBconn.delete_country(cid)
                print("Selected CountryID deleted" "\n")
                break

    def movie_sub():
        print("Movies with Subtitles")
        print("-" * 21)
        # prompt user to enter subtitle language
        while True:
            sub_lang = str(input("Enter Subtitle Language:"))
            break

        while True:
            # when user has entered a subtitle language
            if sub_lang != "":
                print("")
                line = "Movies with" " " + sub_lang + " " "subtitles"
                print(line)
                print("-" * len(line))
                ids = mongoDBconn.movie_subtitle(sub_lang)
                # check whether the id is greater than 1
                if len(ids) > 0:
                    subtitles = sqlDBconn.movie_sub(ids)
                    # iterate through the database
                    for movie in subtitles:
                        # print the film name and its synopsis
                        print(movie["FilmName"], "|", movie["FilmSynopsis"])
                    print("")
                break
            # if the above condition is not satisfied prompt user to enter a subtitle language    
            else:
                sub_lang = str(input("Enter Subtitle Language:"))
    
    def view_collections():
        while True: 
            line4 = ("Collections Displayed from Movie Scripts database (MongoDB)")
            print(line4)
            print("-" * len(line4))

            print("")
            # connect to database and view the collections
            mongoDBconn.view_collections()
            print("")
            break


    def add_moviescript():
        line2 = ("Add new Movie Script")
        print(line2)
        print("-" * len(line2))
        # prompt user to enter a film id, must be an integer
        while True:
            try:
                film_id = int(input("ID :"))
                break
            except ValueError:
                print("Please Enter an ID Number" "\n")
        # store keywords in a list
        keywords = []
        # prompt the user to enter keywords
        while True:
            try:
                keyword = str(input("Keyword (-1 to end):"))
                # stop asking if the user enters -1 i.e., break
                if keyword == "-1":
                    break
                # add user input to the created list
                keywords.append(keyword)
            except:
                continue
        # store subtitle languages in a list        
        sub_langs = []
        # prompt user to enter subtitle languages
        while True:
            try:
                subtitle_lang = str(input("Subtitle Language (-1 to end):"))
                # stop asking if the user enters -1 i.e., break
                if subtitle_lang == "-1":
                    break
                # add user input to the created list
                sub_langs.append(subtitle_lang)
            except:
                continue
        # setup condition to check whether the film id entered exists within the sql database        
        check_id = sqlDBconn.no_movieid(film_id)
        while True:
            try:
                # iterate through the database
                for check in check_id:
                    check["CheckExists"]
                # if the film ID does not exist i.e., a value of 0 is returned
                if check["CheckExists"] == 0:
                    # provide user with an error
                    sqlDBconn.no_movieid(film_id)
                    print("\n" "*** ERROR ***: Film with id:",
                          film_id, "does not exist in moviesDB" "\n")
                    break
                # if movie id exists within sql database add to the mongo database        
                else:
                    mongoDBconn.movie_script(film_id, keywords, sub_langs)
                    print("\n" "MovieScript:", film_id,
                          "added to database" "\n")
                    break
            # provide error when duplicate entires are made to the mongo database        
            except pymongo.errors.DuplicateKeyError:
                print("\n" "*** ERROR ***: Movie Script with id:",
                      film_id, "already exists" "\n")
                break

    def delete_collection_entry():
        deleteline = ("Delete Collection via ID Reference")
        print(deleteline)
        print("-" * len(deleteline))
        # prompt user to enter a film id
        film_id = int(input("ID :"))
        # connect to database and delete the film based on id i.e., user input
        mongoDBconn.delete_db_entry(film_id)
        var1 = ("Selected ID deleted")
        print(var1)
        print("-" * len(var1), "\n")

    # conditional statements for app behaviour based on user input
    while True:
        # execute display menu function
        display_menu()
        # prompt user to make a selection
        print("")
        choice = input("Choice:")

        if (choice == "x" or choice == "X"):
            break
        elif (choice == "1"):
            film_actor_menu()
        elif (choice == "2"):
            actors_dob_gender()
        elif (choice == "3"):
            movie_studio()
        elif (choice == "4"):
            view_countries_table()
        elif (choice == "5"):
            add_country()
        elif (choice == "6"):
            delete_country()
        elif (choice == "7"):
            movie_sub()
        elif (choice == "8"):
            view_collections()           
        elif (choice == "9"):
            add_moviescript()        
        elif (choice == "10"):
            delete_collection_entry()

# Create main menu for user
def display_menu():
    print("Movies DB")
    print("-" * 9)
    print("")
    print("MENU")
    print("=" * 4)
    print("1 - View Films")
    print("2 - View Actors by Year of Birth & Gender")
    print("3 - View Studios")
    print("4 - View Countries Table")
    print("5 - Add New Country")
    print("6 - Delete Country via Country ID")
    print("7 - View Movie with Subtitles")
    print("8 - View Collections")
    print("9 - Add New MovieScript")
    print("10 - Delete Collection via ID")
    print("x - Exit application")

if __name__ == "__main__":
    # execute only if run as a script
    main()